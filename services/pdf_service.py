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

    # Logo
    logo_width = 150
    logo_height = 80
    x_logo = (width - logo_width) / 2
    y_logo = height - logo_height - 20
    BASE_DIR = os.path.dirname(__file__)
    LOGO_PATH = os.path.join(BASE_DIR, "..", "assets", "heineken_logo.png")

   if os.path.exists(LOGO_PATH):
    c.drawImage(LOGO_PATH, x_logo, y_logo, width=logo_width, height=logo_height, mask="auto")

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y_logo - 20,
                        "CARTA DE RESPONSABILIDAD DE EQUIPO Y SEGURIDAD DE INFORMACION")
    c.line(50, y_logo - 30, width - 50, y_logo - 30)

    # Texto inicial
    c.setFont("Helvetica", 12)
    texto_parte1 = f"""
CARTA DE RESPONSABILIDAD DE EQUIPO Y SEGURIDAD DE INFORMACION QUE CELEBRAN 
POR UNA PARTE Cuauhtémoc Moctezuma, A QUIEN EN LO SUCESIVO SE LE DENOMINARA
"EL COMODANTE" Y POR OTRA {nuevo.get('Usuario', '')} A QUIEN EN LO SUCESIVO SE LE 
DENOMINARA "EL COMODATARIO" EL CUAL CELEBRAN BAJO LAS SIGUIENTES DECLARACIO
NES Y CLAUSULAS:

DECLARACIONES
I.- Declara EL COMODANTE ser propietario y por tal razón, estar legalmente facultado para dar en 
comodato el o los siguientes bienes muebles, mismos que en "Anexo I", se agregan al presente 
contrato para formar parte integral del mismo.II.- Declara EL COMODATARIO ser {nuevo.get('Usuario', '')}
en la empresa Cuauhtémoc Moctezuma y que requiere utilizar de los bienes citados en esta carta
de responsabilidad de equipo y seguridad de información a fin de desempeñar de la mejor manera y 
en forma eficiente las funciones inherentes a su puesto.

CLAUSULAS
PRIMERA.- EL COMODANTE entrega en comodato el o los Bienes descritos en el Anexo I de este 
Contrato a EL COMODATARIO para el uso y desempeño de sus labores.SEGUNDA.- EL COMODATA
RIO manifiesta que recibe en este acto los Bienes señalados en la declaración primera de este 
contrato (Anexo I) en comodato,y manifiesta que se encuentran en perfectas condiciones de 
uso y funcionamiento y que se obliga a utilizarlos de manera personal y exclusivamente para 
el desempeño de sus labores para El Comodante. De igual modo EL  COMODATARIO, como usuario 
de dichos bienes comodatados asume bajo su riesgo para con EL COMODANTE las  siguientes 
responsabilidades generales y específicas (uso de activos, confidencialidad, respaldo de 
información,antivirus, etc.).

TERCERA.- EL COMODATARIO se obliga a cuidar y conservar los bienes que ha recibido en comodato 
y a efectuar por su cuenta las reparaciones necesarias que por su culpa o negligencia se 
ocasionaran a los mismos.CUARTA.- Este Contrato inicia a partir de la firma del mismo y será 
por tiempo indefinido, pudiendo concluir en cualquier tiempo cuando así lo determine.El 
Comodante, procediendo a requerirle a El Comodatario la entrega de los mismos, bajo pena de 
proceder en su contra si se negare, por configurarse delito de abuso de confianza y/o cualquier 
otro que se derivare de la indebida retención del mismo.
"""
    y = y_logo - 60
    for linea in texto_parte1.split("\n"):
        c.drawString(50, y, linea.strip())
        y -= 12

    # Nueva página
    c.showPage()

    # Continuación del contrato
    c.setFont("Helvetica", 14)
    texto_parte2 = f"""
QUINTA.- EL COMODATARIO independientemente de las obligaciones que asume en la
cláusula segunda, se obliga:
a).- Cuidar los Bienes;
b).- Restituirlos en las condiciones en que los recibiera salvo el deterioro normal;
c).- No transferir su uso o propiedad a terceros;
d).- Pagar daños y perjuicios que por su culpa o negligencia sufrieran estos;
e).- Avisar a EL COMODANTE en caso de embargo o cualquier acto que le prive 
de su uso;
f).- Cumplir demás obligaciones que señale el Contrato o la Ley.

SEXTA.- En caso que EL COMODATARIO no restituya los bienes en el tiempo pactado o 
antes en caso de concluir el Contrato por otra causa imputable a este,
EL COMODATARIO restituirá a EL COMODANTE el valor de los Bienes que recibió en 
comodato, tomando como base el valor factura del activo o restituyendo otros
Bienes de la misma calidad, marca y especie.

SEPTIMA.- COMPETENCIA.- Para resolver las controversias que se susciten con motivo
de la aplicación e interpretación del Contrato,las partes se someten a la jurisdic
ción de los Jueces y Tribunales del fuero común competentes en la ciudad local,renun
ciando expresamente al fuero por cualquier otro concepto.

Enteradas las partes del alcance y contenido legal de lo aquí establecido, EL 
COMODATARIO acepta que entiende el contenido,alcance y responsabilidades conte
nidas en este contrato y firma juntamente con EL COMODANTE para constancia.

NOTA.- La firma del presente documento, anula cualquier comodato que pudiera existir 
anterior a este.
Ticket: {nuevo.get('RITM', 'N/A')}
"""
    y = height - 100
    for linea in texto_parte2.split("\n"):
        c.drawString(50, y, linea.strip())
        y -= 12

    # Estilos
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]

    # Tabla principal
    encabezados = ["Modelo", "Serie", "Marca", "Tipo", "IMEI/Host",
                   "Línea", "Localidad"]
    valores = [
        nuevo.get("Modelo", ""),
        nuevo.get("Serie", ""),
        nuevo.get("Marca", ""),
        nuevo.get("Tipo", ""),
        nuevo.get("IMEI_HOST", ""),
        nuevo.get("LINEA", ""),
        nuevo.get("LOCALIDAD", "")
    ]
    valores_paragraphs = [Paragraph(str(v), styleN) for v in valores]
    data = [encabezados, valores_paragraphs]
    colWidths = [70, 70, 70, 60, 100, 70, 90]

    tabla = Table(data, colWidths=colWidths)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ]))
    tabla.wrapOn(c, width, height)
    tabla.drawOn(c, 50, 300)

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

    # Estado y firmas
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 280, f"Estado del equipo: {nuevo.get('Estado', '')}")
    c.drawString(300, 280, f"Ticket Refresh: {nuevo.get('RITM', 'N/A')}")

    firmas_y = 100
    c.setFont("Helvetica", 10)
    c.drawString(50, firmas_y, "______________________________")
    c.drawString(50, firmas_y - 15, "Nombre de quien entrega el equipo")
    c.drawString(300, firmas_y, "______________________________")
    c.drawString(300, firmas_y - 15, f"{nuevo.get('Usuario', '')} (EL COMODATARIO)")

    # Pie de página
    fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 30,
                        f"Cuauhtémoc Moctezuma Heineken México | Generado el {fecha_generacion}")

    c.save()
    buffer.seek(0)
    return buffer
