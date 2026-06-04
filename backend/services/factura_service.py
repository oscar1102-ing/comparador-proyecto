from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from datetime import datetime
import random
 
PLANES = {
    "basico": {
        "nombre": "Plan Básico",
        "precio": "COP $19.900 / mes",
        "precio_num": "19.900",
        "beneficios": [
            "20 comparaciones de precios por mes",
            "Hasta 50 productos favoritos",
            "Historial de búsquedas completo",
            "Alertas de precio para 3 productos",
        ]
    },
    "pro": {
        "nombre": "Plan Pro",
        "precio": "COP $39.900 / mes",
        "precio_num": "39.900",
        "beneficios": [
            "Comparaciones ilimitadas",
            "Favoritos ilimitados",
            "Historial ilimitado",
            "Alertas ilimitadas",
            "Historial de precios del producto",
        ]
    },
    
        "usuario": {
        "nombre": "Gratuito",
        "precio": "$0",
        "beneficios": [
            "Ver productos y precios",
            "5 comparaciones por mes",
            "5 productos favoritos",
            "Historial últimas 10 búsquedas",
        ]
    }
}
 
def generar_factura_pdf(nombre: str, email: str, plan: str) -> bytes:
    info_plan = PLANES.get(plan)
    if not info_plan:
        raise ValueError(f"Plan inválido: {plan}")
 
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )
 
    styles = getSampleStyleSheet()
    NARANJA = colors.HexColor("#ff6b00")
    GRIS_OSCURO = colors.HexColor("#1e293b")
    GRIS_MEDIO = colors.HexColor("#64748b")
    GRIS_CLARO = colors.HexColor("#f8fafc")
 
    estilo_titulo = ParagraphStyle("titulo", fontSize=22, fontName="Helvetica-Bold",
                                   textColor=colors.white, alignment=TA_CENTER, spaceAfter=4)
    estilo_subtitulo = ParagraphStyle("subtitulo", fontSize=11, fontName="Helvetica",
                                      textColor=colors.white, alignment=TA_CENTER)
    estilo_seccion = ParagraphStyle("seccion", fontSize=11, fontName="Helvetica-Bold",
                                    textColor=GRIS_OSCURO, spaceBefore=14, spaceAfter=6)
    estilo_normal = ParagraphStyle("normal", fontSize=10, fontName="Helvetica",
                                   textColor=GRIS_MEDIO, spaceAfter=3)
    estilo_bold = ParagraphStyle("bold", fontSize=10, fontName="Helvetica-Bold",
                                 textColor=GRIS_OSCURO)
    estilo_precio = ParagraphStyle("precio", fontSize=20, fontName="Helvetica-Bold",
                                   textColor=NARANJA, alignment=TA_CENTER, spaceBefore=6, spaceAfter=6)
    estilo_footer = ParagraphStyle("footer", fontSize=9, fontName="Helvetica",
                                   textColor=GRIS_MEDIO, alignment=TA_CENTER)
 
    numero_factura = f"PC-{datetime.now().strftime('%Y%m')}-{random.randint(1000, 9999)}"
    fecha = datetime.now().strftime("%d de %B de %Y").replace(
        "January","enero").replace("February","febrero").replace("March","marzo"
        ).replace("April","abril").replace("May","mayo").replace("June","junio"
        ).replace("July","julio").replace("August","agosto").replace("September","septiembre"
        ).replace("October","octubre").replace("November","noviembre").replace("December","diciembre")
 
    story = []
 
    # ── ENCABEZADO naranja ──
    encabezado = Table(
        [[Paragraph("PriceCompare", estilo_titulo)],
         [Paragraph("Comparador de precios inteligente", estilo_subtitulo)]],
        colWidths=[6.75 * inch]
    )
    encabezado.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NARANJA),
        ("ROUNDEDCORNERS", [8]),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
    ]))
    story.append(encabezado)
    story.append(Spacer(1, 20))
 
    # ── TÍTULO FACTURA ──
    story.append(Paragraph("COMPROBANTE DE SUSCRIPCIÓN", ParagraphStyle(
        "cf", fontSize=13, fontName="Helvetica-Bold", textColor=GRIS_OSCURO,
        alignment=TA_CENTER, spaceAfter=4)))
    story.append(HRFlowable(width="100%", thickness=1.5, color=NARANJA, spaceAfter=16))
 
    # ── DATOS FACTURA Y CLIENTE (dos columnas) ──
    datos_tabla = [
        [Paragraph("<b>Factura N°</b>", estilo_bold),
         Paragraph(numero_factura, estilo_normal),
         Paragraph("<b>Cliente</b>", estilo_bold),
         Paragraph(nombre, estilo_normal)],
        [Paragraph("<b>Fecha</b>", estilo_bold),
         Paragraph(fecha, estilo_normal),
         Paragraph("<b>Email</b>", estilo_bold),
         Paragraph(email, estilo_normal)],
        [Paragraph("<b>Estado</b>", estilo_bold),
         Paragraph("Pago confirmado ✓", ParagraphStyle("pend", fontSize=10,
             fontName="Helvetica-Bold", textColor=colors.HexColor("#f59e0b"))),
         Paragraph("<b>Plan</b>", estilo_bold),
         Paragraph(info_plan["nombre"], ParagraphStyle("planN", fontSize=10,
             fontName="Helvetica-Bold", textColor=NARANJA))],
    ]
    tabla_datos = Table(datos_tabla, colWidths=[1.2*inch, 2.2*inch, 1.2*inch, 2.15*inch])
    tabla_datos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRIS_CLARO),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, GRIS_CLARO, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(tabla_datos)
    story.append(Spacer(1, 20))
 
    # ── DETALLE DEL PLAN ──
    story.append(Paragraph("Detalle del plan contratado", estilo_seccion))
 
    filas_beneficios = [[Paragraph(f"✓  {b}", estilo_normal)] for b in info_plan["beneficios"]]
    tabla_beneficios = Table(filas_beneficios, colWidths=[6.75 * inch])
    tabla_beneficios.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, GRIS_CLARO]),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(tabla_beneficios)
    story.append(Spacer(1, 20))
 
    # ── TOTAL ──
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph(info_plan["precio"], estilo_precio))
    story.append(Paragraph("(precio mensual, renovación automática)", estilo_footer))
    story.append(Spacer(1, 20))
 

 
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph("PriceCompare © 2026 · Este documento es un comprobante de solicitud, no una factura fiscal.", estilo_footer))
    story.append(Paragraph("Generado automáticamente el " + datetime.now().strftime("%d/%m/%Y %H:%M"), estilo_footer))
 
    doc.build(story)
    buffer.seek(0)
    return buffer.read()
