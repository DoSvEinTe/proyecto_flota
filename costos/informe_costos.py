from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from .models import CostosViaje

def informe_costos_pdf(request, costos_pk):
    costos = get_object_or_404(CostosViaje, pk=costos_pk)
    viaje = costos.viaje
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_costos_viaje_{viaje.id}.pdf"'
    buffer = bytes()
    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=18
    )
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1e40af'), alignment=TA_CENTER, spaceAfter=25, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#0d47a1'), spaceAfter=14, fontName='Helvetica-Bold')
    info_style = ParagraphStyle('Info', parent=styles['Normal'], fontSize=11, spaceAfter=6)
    # Portada y datos generales
    elements.append(Paragraph("INFORME DE COSTOS DEL VIAJE", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("DATOS DEL BUS", subtitle_style))
    bus = viaje.bus
    datos_bus = [
        f"<b>Placa:</b> {bus.placa}",
        f"<b>Marca:</b> {bus.marca}",
        f"<b>Modelo:</b> {bus.modelo}",
        f"<b>Año:</b> {bus.año_fabricacion}",
        f"<b>Capacidad de pasajeros:</b> {bus.capacidad_pasajeros}",
        f"<b>Kilometraje inicial:</b> {bus.kilometraje_inicial} km",
    ]
    for linea in datos_bus:
        elements.append(Paragraph(linea, info_style))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph("DATOS DEL CONDUCTOR", subtitle_style))
    conductor = viaje.conductor
    datos_conductor = [
        f"<b>Nombre:</b> {conductor.nombre} {conductor.apellido}",
        f"<b>Correo:</b> {conductor.email}",
        f"<b>Teléfono:</b> {conductor.telefono}",
        f"<b>Licencia:</b> {conductor.licencias}",
        f"<b>Tiempo en la empresa:</b> {((datetime.now().date() - conductor.fecha_contratacion).days // 365)} años",
    ]
    for linea in datos_conductor:
        elements.append(Paragraph(linea, info_style))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph("DATOS DEL VIAJE", subtitle_style))
    datos_viaje = [
        f"<b>Origen:</b> {viaje.lugar_origen.nombre}",
        f"<b>Destino:</b> {viaje.lugar_destino.nombre}",
        f"<b>Fecha de salida:</b> {viaje.fecha_salida.strftime('%d/%m/%Y %H:%M')}",
        f"<b>Fecha llegada estimada:</b> {viaje.fecha_llegada_estimada.strftime('%d/%m/%Y %H:%M')}",
        f"<b>Estado:</b> {viaje.get_estado_display()}",
        f"<b>Distancia estimada:</b> {viaje.distancia_km or 'No calculada'} km",
        f"<b>Observaciones:</b> {viaje.observaciones or '-'}",
    ]
    for linea in datos_viaje:
        elements.append(Paragraph(linea, info_style))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph(f"<b>Pasajeros en el viaje:</b> {viaje.get_pasajeros_count()} / {bus.capacidad_pasajeros}", info_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("EXPLICACIÓN DEL CÁLCULO DE COSTOS", subtitle_style))
    explicacion = (
        "El cálculo del costo total del viaje se realiza sumando los siguientes componentes: <br/>"
        "<b>Combustible:</b> Suma de todos los puntos de recarga registrados.<br/>"
        "<b>Mantenimiento:</b> Suma de los costos de mantenimientos asociados al viaje.<br/>"
        "<b>Peajes:</b> Suma de todos los peajes pagados durante el viaje.<br/>"
        "<b>Otros costos:</b> Cualquier gasto adicional registrado.<br/>"
        "<b>Gastos totales:</b> Suma de todos los gastos anteriores."
    )
    elements.append(Paragraph(explicacion, info_style))
    elements.append(Paragraph("RESUMEN DE GASTOS", subtitle_style))
    resumen_data = [
        ["Combustible", f"CLP ${costos.combustible:,.0f}"],
        ["Mantenimiento", f"CLP ${costos.mantenimiento:,.0f}"],
        ["Peajes", f"CLP ${costos.peajes:,.0f}"],
        ["Otros Costos", f"CLP ${costos.otros_costos:,.0f}"],
        ["Gastos Totales", f"CLP ${costos.costo_total:,.0f}"],
    ]
    resumen_table = Table(resumen_data, colWidths=[2.5*inch, 2.5*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(resumen_table)
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("DETALLE DE PARADAS DE GASOLINA", subtitle_style))
    puntos = costos.puntos_recarga.all()
    if puntos:
        puntos_data = [["#", "Ubicación", "Kilometraje", "Litros", "Precio/Litro", "Costo Total"]]
        for p in puntos:
            puntos_data.append([
                p.orden,
                p.ubicacion,
                f"{p.kilometraje:,.2f}",
                f"{p.litros_cargados:,.2f}",
                f"CLP ${p.precio_combustible:,.0f}",
                f"CLP ${p.costo_total:,.0f}"
            ])
        puntos_table = Table(puntos_data, colWidths=[0.7*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        puntos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196f3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(Paragraph(f"Total de paradas de gasolina: {puntos.count()}", info_style))
        elements.append(puntos_table)
    else:
        elements.append(Paragraph("No hay puntos de recarga registrados.", info_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("DETALLE DE PEAJES", subtitle_style))
    peajes = viaje.peajes.all()
    if peajes:
        peajes_data = [["#", "Ubicación", "Monto", "Fecha Pago", "Comprobante"]]
        for idx, p in enumerate(peajes, 1):
            peajes_data.append([
                idx,
                p.lugar,
                f"CLP ${p.monto:,.0f}",
                p.fecha_pago.strftime('%d/%m/%Y %H:%M'),
                p.comprobante or '-'
            ])
        peajes_table = Table(peajes_data, colWidths=[0.7*inch, 1.5*inch, 1.2*inch, 1.5*inch, 1.2*inch])
        peajes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196f3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(Paragraph(f"Total de peajes: {peajes.count()}", info_style))
        elements.append(peajes_table)
    else:
        elements.append(Paragraph("No hay peajes registrados.", info_style))
    elements.append(Spacer(1, 0.2 * inch))
    # Nueva hoja: lista de pasajeros y gastos
    elements.append(PageBreak())
    elements.append(Paragraph("LISTA DE PASAJEROS Y GASTOS", title_style))
    pasajeros = viaje.pasajeros.all()
    if pasajeros:
        pasajeros_data = [["#", "Nombre", "RUT", "Teléfono", "Correo", "Gasto estimado"]]
        for idx, pasajero in enumerate(pasajeros, 1):
            pasajeros_data.append([
                idx,
                pasajero.nombre_completo,
                getattr(pasajero, 'rut', '-'),
                getattr(pasajero, 'telefono', '-'),
                getattr(pasajero, 'correo', '-'),
                "-"
            ])
        pasajeros_table = Table(pasajeros_data, colWidths=[0.7*inch, 2.2*inch, 1.2*inch, 1.2*inch, 1.7*inch, 1.2*inch])
        pasajeros_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(pasajeros_table)
    else:
        elements.append(Paragraph("No hay pasajeros registrados para este viaje.", info_style))
    elements.append(Paragraph("MANTENIMIENTOS ASOCIADOS", subtitle_style))
    mantenimientos = costos.mantenimientos.all()
    if mantenimientos:
        mant_data = [["Tipo", "Descripción", "Fecha", "Kilometraje", "Costo"]]
        for m in mantenimientos:
            mant_data.append([
                m.get_tipo_display(),
                m.descripcion,
                m.fecha_mantenimiento.strftime('%d/%m/%Y'),
                m.kilometraje,
                f"CLP ${m.costo:,.0f}"
            ])
        mant_table = Table(mant_data, colWidths=[1.2*inch, 2.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        mant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196f3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(mant_table)
    else:
        elements.append(Paragraph("No hay mantenimientos asociados.", info_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("OTROS COSTOS", subtitle_style))
    if costos.otros_costos > 0:
        elements.append(Paragraph(f"Monto: CLP ${costos.otros_costos:,.0f}", info_style))
        elements.append(Paragraph(f"Justificación: {costos.observaciones or '-'}", info_style))
    else:
        elements.append(Paragraph("No hay otros costos registrados.", info_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"<i>Informe generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema de Gestión de Flota</i>", info_style))
    doc.build(elements)
    return response
