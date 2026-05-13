import os
import io
import json
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

# ====== PDF ======
def generar_pdf_comodato(nuevo, accesorios_seleccionados):
    # --- Normalizar accesorios ---
    accesorios_normalizados = {}

    if isinstance(accesorios_seleccionados, dict):
        accesorios_normalizados = accesorios_seleccionados
    elif isinstance(accesorios_seleccionados, list):
        accesorios_normalizados = {"Accesorios": accesorios_seleccionados}
    elif isinstance(accesorios_seleccionados, str):
        try:
            accesorios_normalizados = json.loads(accesorios_seleccionados)
            if not isinstance(accesorios_normalizados, dict):
                accesorios_normalizados = {"Accesorios": [accesorios_normalizados]}
        except Exception:
            accesorios_normalizados = {
                "Accesorios": [a.strip() for a in accesorios_seleccionados.split(",") if a.strip()]
            }

    # --- Generación del PDF ---
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER

    # ... (todo tu código de logo, texto, tablas de encabezados) ...

    # ---- Tabla de accesorios seleccionados ----
    data_accesorios = [["Categoría", "Accesorios"]]
    for categoria, seleccionados in accesorios_normalizados.items():
        data_accesorios.append([
            categoria,
            ", ".join(seleccionados) if seleccionados else "-"
        ])

    tabla_accesorios = Table(data_accesorios, colWidths=[150, 300])
    tabla_accesorios.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
    ]))
    tabla_accesorios.wrapOn(c, width, height)
    tabla_accesorios.drawOn(c, 50, 150)

    # ---- Estado, firmas y pie de página ----
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 280, f"Estado del equipo: {nuevo.get('Estado', '')}")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(300, 280, f"Ticket Refresh: {nuevo.get('RITM', 'N/A')}")

    firmas_y = 100
    c.setFont("Helvetica", 10)
    c.drawString(50, firmas_y, "______________________________")
    c.drawString(50, firmas_y - 15, "Nombre de quien entrega el equipo")
    c.drawString(300, firmas_y, "______________________________")
    c.drawString(300, firmas_y - 15, f"{nuevo.get('Usuario', '')} (EL COMODATARIO)")

    fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30,
                        f"Cuauhtémoc Moctezuma Heineken México | Generado el {fecha_generacion}")

    c.save()
    buffer.seek(0)
    return buffer
