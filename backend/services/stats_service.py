from sqlalchemy.orm import Session
from typing import List
from backend.models import C5Incident, UserReport
from backend.schemas import TopZonaStats, HoraStats

class StatsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_top_zonas(self, tipo_zona: str, limit: int = 10) -> List[TopZonaStats]:
        print("=" * 60)
        print(f"STATS SERVICE LLAMADO: tipo={tipo_zona}, limit={limit}")
        
        zona_col = "colonia" if tipo_zona == "colonia" else "alcaldia"
        
        c5_data = self.db.query(C5Incident).all()
        user_data = self.db.query(UserReport).all()
        
        print(f"C5: {len(c5_data)}, Users: {len(user_data)}")
        
        c5_counts = {}
        for inc in c5_data:
            z = getattr(inc, zona_col, None)
            if z:
                z = z.strip()
                c5_counts[z] = c5_counts.get(z, 0) + 1
        
        user_counts = {}
        for rep in user_data:
            z = getattr(rep, zona_col, None)
            if z:
                z = z.strip()
                user_counts[z] = user_counts.get(z, 0) + 1
        
        print(f"Zonas C5: {len(c5_counts)}, Zonas users: {len(user_counts)}")
        
        all_zonas = set(c5_counts.keys()) | set(user_counts.keys())
        
        result = []
        for zona in all_zonas:
            result.append(TopZonaStats(
                zona=zona,
                tipo_zona=tipo_zona,
                total_incidentes=c5_counts.get(zona, 0) + user_counts.get(zona, 0),
                incidentes_c5=c5_counts.get(zona, 0),
                incidentes_usuarios=user_counts.get(zona, 0)
            ))
        
        result.sort(key=lambda x: x.total_incidentes, reverse=True)
        print(f"Retornando {len(result[:limit])} resultados")
        print("=" * 60)
        
        return result[:limit]
    
    def get_horas_peligrosas(self) -> List[HoraStats]:
        c5_data = self.db.query(C5Incident).all()
        user_data = self.db.query(UserReport).all()
        
        c5_hours = {}
        for inc in c5_data:
            if inc.hora is not None:
                c5_hours[inc.hora] = c5_hours.get(inc.hora, 0) + 1
        
        user_hours = {}
        for rep in user_data:
            if rep.created_at:
                h = rep.created_at.hour
                user_hours[h] = user_hours.get(h, 0) + 1
        
        result = []
        for hora in range(24):
            result.append(HoraStats(
                hora=hora,
                total_incidentes=c5_hours.get(hora, 0) + user_hours.get(hora, 0),
                incidentes_c5=c5_hours.get(hora, 0),
                incidentes_usuarios=user_hours.get(hora, 0)
            ))
        
        return result
    
    def get_opciones_filtros(self):
        try:
            print("=" * 60)
            print("Obteniendo opciones de filtros...")
            
            print("Consultando tipos...")
            tipos_raw = self.db.query(C5Incident.tipo_incidente).distinct().limit(50).all()
            print(f"Tipos raw obtenidos: {len(tipos_raw)}")
            
            tipos = []
            for t in tipos_raw:
                if t[0] and t[0].strip():
                    tipos.append(t[0].strip())
            tipos = sorted(list(set(tipos)))
            print(f"Tipos procesados: {len(tipos)}")
            if tipos:
                print(f"Ejemplos: {tipos[:3]}")
            
            print("Consultando alcaldias...")
            alcaldias_raw = self.db.query(C5Incident.alcaldia).distinct().all()
            print(f"Alcaldias raw obtenidas: {len(alcaldias_raw)}")
            
            alcaldias = []
            for a in alcaldias_raw:
                if a[0] and a[0].strip():
                    alcaldias.append(a[0].strip())
            alcaldias = sorted(list(set(alcaldias)))
            print(f"Alcaldias procesadas: {len(alcaldias)}")
            if alcaldias:
                print(f"Ejemplos: {alcaldias[:3]}")
            
            print(f"RESULTADO FINAL: {len(tipos)} tipos, {len(alcaldias)} alcaldias")
            print("=" * 60)
            
            return {
                "tipos_incidente": tipos[:30],
                "alcaldias": alcaldias,
                "colonias": []
            }
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            return {
                "tipos_incidente": [],
                "alcaldias": [],
                "colonias": []
            }
    
    def get_colonias_por_alcaldia(self, alcaldia: str):
        try:
            from sqlalchemy import func
            
            colonias = self.db.query(
                C5Incident.colonia,
                func.count(C5Incident.id).label('count')
            ).filter(
                C5Incident.alcaldia == alcaldia,
                C5Incident.colonia.isnot(None)
            ).group_by(C5Incident.colonia).order_by(
                func.count(C5Incident.id).desc()
            ).limit(50).all()
            
            return sorted([c[0] for c in colonias])
            
        except Exception as e:
            print(f"ERROR: {e}")
            return []
    
    def get_estadisticas_filtradas(self, tipo_incidente=None, alcaldia=None, colonia=None, limit=50):
        try:
            print("=" * 60)
            print(f"Filtros: tipo={tipo_incidente}, alcaldia={alcaldia}, colonia={colonia}, limit={limit}")
            
            query_c5 = self.db.query(C5Incident)
            if tipo_incidente:
                query_c5 = query_c5.filter(C5Incident.tipo_incidente == tipo_incidente)
            if alcaldia:
                query_c5 = query_c5.filter(C5Incident.alcaldia == alcaldia)
            if colonia:
                query_c5 = query_c5.filter(C5Incident.colonia == colonia)
            
            query_user = self.db.query(UserReport)
            if tipo_incidente:
                query_user = query_user.filter(UserReport.tipo == tipo_incidente)
            if alcaldia:
                query_user = query_user.filter(UserReport.alcaldia == alcaldia)
            if colonia:
                query_user = query_user.filter(UserReport.colonia == colonia)
            
            c5_data = query_c5.limit(10000).all()
            user_data = query_user.all()
            
            print(f"Resultados: {len(c5_data)} C5, {len(user_data)} usuarios")
            
            colonias_count = {}
            for inc in c5_data:
                col = inc.colonia
                if col:
                    colonias_count[col] = colonias_count.get(col, 0) + 1
            
            for rep in user_data:
                col = rep.colonia
                if col:
                    colonias_count[col] = colonias_count.get(col, 0) + 1
            
            top_colonias = sorted(colonias_count.items(), key=lambda x: x[1], reverse=True)[:limit]
            
            tipos_count = {}
            for inc in c5_data:
                tipo = inc.tipo_incidente
                if tipo:
                    tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
            
            for rep in user_data:
                tipo = rep.tipo
                if tipo:
                    tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
            
            top_tipos = sorted(tipos_count.items(), key=lambda x: x[1], reverse=True)[:20]
            
            horas_count = {}
            for inc in c5_data:
                if inc.hora is not None:
                    horas_count[inc.hora] = horas_count.get(inc.hora, 0) + 1
            
            for rep in user_data:
                if rep.created_at:
                    h = rep.created_at.hour
                    horas_count[h] = horas_count.get(h, 0) + 1
            
            print(f"Top colonias: {len(top_colonias)}, Top tipos: {len(top_tipos)}")
            print("=" * 60)
            
            return {
                "total_incidentes": len(c5_data) + len(user_data),
                "incidentes_c5": len(c5_data),
                "incidentes_usuarios": len(user_data),
                "top_colonias": [{"colonia": c, "total": t} for c, t in top_colonias],
                "top_tipos": [{"tipo": t, "total": cnt} for t, cnt in top_tipos],
                "por_hora": [{"hora": h, "total": horas_count.get(h, 0)} for h in range(24)],
                "filtros_aplicados": {
                    "tipo_incidente": tipo_incidente,
                    "alcaldia": alcaldia,
                    "colonia": colonia
                }
            }
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            return {"total_incidentes": 0, "error": str(e)}
