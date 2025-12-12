"""
Servicio para generar certificados PDF de riesgo vial.

Usa Jinja2 para renderizar HTML y WeasyPrint para convertir a PDF.
"""

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from typing import Dict, Any
import os
import tempfile
from pathlib import Path
from datetime import datetime


class CertificatesService:
    """Servicio para generar certificados PDF."""
    
    def __init__(self):
        # Obtener ruta del directorio de templates
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    def generate_certificate(
        self,
        tipo_zona: str,
        nombre_zona: str,
        stats: Dict[str, Any]
    ) -> str:
        """
        Genera un certificado PDF de riesgo vial para una zona.
        
        Args:
            tipo_zona: "colonia" o "alcaldia"
            nombre_zona: nombre de la zona
            stats: diccionario con estadísticas de la zona
            
        Returns:
            Ruta al archivo PDF generado
        """
        # Cargar plantilla
        template = self.env.get_template("certificado_zona.html")
        
        # Preparar contexto
        context = {
            "nombre_zona": nombre_zona,
            "tipo_zona": tipo_zona,
            "total_incidentes": stats.get("total_incidentes", 0),
            "total_c5": stats.get("total_c5", 0),
            "total_usuarios": stats.get("total_usuarios", 0),
            "promedio_mensual": round(stats.get("promedio_mensual", 0), 2),
            "tipos_c5": stats.get("tipos_c5", {}),
            "tipos_usuarios": stats.get("tipos_usuarios", {}),
            "horas_peligrosas_c5": stats.get("horas_peligrosas_c5", {}),
            "horas_peligrosas_usuarios": stats.get("horas_peligrosas_usuarios", {}),
            "fecha_generacion": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        # Renderizar HTML
        html_content = template.render(**context)
        
        # Crear archivo temporal para el PDF
        pdf_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
            dir=tempfile.gettempdir()
        )
        pdf_path = pdf_file.name
        pdf_file.close()
        
        # Convertir HTML a PDF
        HTML(string=html_content).write_pdf(pdf_path)
        
        return pdf_path

