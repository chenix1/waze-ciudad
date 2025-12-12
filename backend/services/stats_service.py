"""
Servicio de estadísticas usando pandas y numpy.

Calcula estadísticas sobre incidentes C5 y reportes ciudadanos.
"""

from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from backend.models import C5Incident, UserReport
from backend.schemas import TopZonaStats, HoraStats


class StatsService:
    """Servicio para calcular estadísticas de incidentes viales."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_top_zonas(self, tipo_zona: str, limit: int = 10) -> List[TopZonaStats]:
        """
        Obtiene las top N zonas con más incidentes.
        
        Args:
            tipo_zona: "colonia" o "alcaldia"
            limit: número de zonas a retornar
            
        Returns:
            Lista de TopZonaStats ordenada por total de incidentes descendente
        """
        # Cargar datos C5
        c5_query = self.db.query(C5Incident)
        if tipo_zona == "colonia":
            c5_query = c5_query.filter(C5Incident.colonia.isnot(None))
        else:
            c5_query = c5_query.filter(C5Incident.alcaldia.isnot(None))
        
        c5_df = pd.read_sql(c5_query.statement, self.db.bind)
        
        # Cargar datos de usuarios
        user_query = self.db.query(UserReport)
        if tipo_zona == "colonia":
            user_query = user_query.filter(UserReport.colonia.isnot(None))
        else:
            user_query = user_query.filter(UserReport.alcaldia.isnot(None))
        
        user_df = pd.read_sql(user_query.statement, self.db.bind)
        
        # Agrupar C5 por zona
        zona_col = "colonia" if tipo_zona == "colonia" else "alcaldia"
        c5_grouped = c5_df.groupby(zona_col).size().reset_index(name="count_c5")
        c5_grouped.columns = ["zona", "count_c5"]
        
        # Agrupar usuarios por zona
        user_grouped = user_df.groupby(zona_col).size().reset_index(name="count_user")
        user_grouped.columns = ["zona", "count_user"]
        
        # Combinar
        combined = pd.merge(
            c5_grouped, user_grouped, on="zona", how="outer"
        ).fillna(0)
        
        combined["total"] = combined["count_c5"] + combined["count_user"]
        combined = combined.sort_values("total", ascending=False).head(limit)
        
        # Convertir a lista de TopZonaStats
        result = []
        for _, row in combined.iterrows():
            result.append(TopZonaStats(
                zona=row["zona"],
                tipo_zona=tipo_zona,
                total_incidentes=int(row["total"]),
                incidentes_c5=int(row["count_c5"]),
                incidentes_usuarios=int(row["count_user"])
            ))
        
        return result
    
    def get_horas_peligrosas(self) -> List[HoraStats]:
        """
        Obtiene distribución de incidentes por hora del día.
        
        Returns:
            Lista de HoraStats con conteo por hora (0-23)
        """
        # Cargar datos C5
        c5_df = pd.read_sql(
            self.db.query(C5Incident).statement,
            self.db.bind
        )
        
        # Cargar datos de usuarios
        user_df = pd.read_sql(
            self.db.query(UserReport).statement,
            self.db.bind
        )
        
        # Extraer hora de usuarios (de created_at)
        if not user_df.empty and "created_at" in user_df.columns:
            user_df["hora"] = pd.to_datetime(user_df["created_at"]).dt.hour
        else:
            user_df["hora"] = 0
        
        # Agrupar C5 por hora
        c5_horas = c5_df.groupby("hora").size().reset_index(name="count_c5")
        c5_horas.columns = ["hora", "count_c5"]
        
        # Agrupar usuarios por hora
        user_horas = user_df.groupby("hora").size().reset_index(name="count_user")
        user_horas.columns = ["hora", "count_user"]
        
        # Combinar
        combined = pd.merge(
            c5_horas, user_horas, on="hora", how="outer"
        ).fillna(0)
        
        # Asegurar todas las horas (0-23)
        all_hours = pd.DataFrame({"hora": range(24)})
        combined = pd.merge(all_hours, combined, on="hora", how="left").fillna(0)
        
        combined["total"] = combined["count_c5"] + combined["count_user"]
        combined = combined.sort_values("hora")
        
        # Convertir a lista de HoraStats
        result = []
        for _, row in combined.iterrows():
            result.append(HoraStats(
                hora=int(row["hora"]),
                total_incidentes=int(row["total"]),
                incidentes_c5=int(row["count_c5"]),
                incidentes_usuarios=int(row["count_user"])
            ))
        
        return result
    
    def get_zona_stats(self, tipo_zona: str, nombre_zona: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas detalladas de una zona específica.
        
        Args:
            tipo_zona: "colonia" o "alcaldia"
            nombre_zona: nombre de la zona
            
        Returns:
            Diccionario con estadísticas de la zona
        """
        # Cargar datos C5 de la zona
        c5_query = self.db.query(C5Incident)
        if tipo_zona == "colonia":
            c5_query = c5_query.filter(C5Incident.colonia == nombre_zona)
        else:
            c5_query = c5_query.filter(C5Incident.alcaldia == nombre_zona)
        
        c5_df = pd.read_sql(c5_query.statement, self.db.bind)
        
        # Cargar datos de usuarios de la zona
        user_query = self.db.query(UserReport)
        if tipo_zona == "colonia":
            user_query = user_query.filter(UserReport.colonia == nombre_zona)
        else:
            user_query = user_query.filter(UserReport.alcaldia == nombre_zona)
        
        user_df = pd.read_sql(user_query.statement, self.db.bind)
        
        # Calcular estadísticas
        total_c5 = len(c5_df)
        total_user = len(user_df)
        total = total_c5 + total_user
        
        # Tipos de incidentes más comunes
        tipos_c5 = c5_df["tipo_incidente"].value_counts().head(5).to_dict() if not c5_df.empty else {}
        tipos_user = user_df["tipo"].value_counts().head(5).to_dict() if not user_df.empty else {}
        
        # Horas más peligrosas
        horas_c5 = c5_df["hora"].value_counts().head(5).to_dict() if not c5_df.empty and "hora" in c5_df.columns else {}
        if not user_df.empty and "created_at" in user_df.columns:
            user_df["hora"] = pd.to_datetime(user_df["created_at"]).dt.hour
            horas_user = user_df["hora"].value_counts().head(5).to_dict()
        else:
            horas_user = {}
        
        # Promedio mensual (si hay datos de fecha)
        if not c5_df.empty and "fecha_hora" in c5_df.columns:
            c5_df["fecha"] = pd.to_datetime(c5_df["fecha_hora"])
            meses_c5 = c5_df["fecha"].dt.to_period("M").value_counts()
            promedio_mensual_c5 = meses_c5.mean() if not meses_c5.empty else 0
        else:
            promedio_mensual_c5 = 0
        
        if not user_df.empty and "created_at" in user_df.columns:
            user_df["fecha"] = pd.to_datetime(user_df["created_at"])
            meses_user = user_df["fecha"].dt.to_period("M").value_counts()
            promedio_mensual_user = meses_user.mean() if not meses_user.empty else 0
        else:
            promedio_mensual_user = 0
        
        promedio_mensual = promedio_mensual_c5 + promedio_mensual_user
        
        return {
            "nombre_zona": nombre_zona,
            "tipo_zona": tipo_zona,
            "total_incidentes": int(total),
            "total_c5": int(total_c5),
            "total_usuarios": int(total_user),
            "promedio_mensual": float(promedio_mensual),
            "tipos_c5": tipos_c5,
            "tipos_usuarios": tipos_user,
            "horas_peligrosas_c5": horas_c5,
            "horas_peligrosas_usuarios": horas_user
        }

