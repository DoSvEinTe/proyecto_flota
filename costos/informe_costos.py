from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from .models import CostosViaje

def informe_costos_pdf(request, costos_pk):
    costos = get_object_or_404(CostosViaje, pk=costos_pk)
    viaje = costos.viaje
    bus = viaje.bus
    conductor = viaje.conductor
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_costos_viaje_{viaje.id}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica-Bold',
        leading=26
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0d47a1'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#0d47a1'),
        borderPadding=5,
        backColor=colors.HexColor('#e3f2fd')
    )
    
    info_style = ParagraphStyle(
        'CustomInfo',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        leading=14
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_RIGHT
    )
    
    # ============ PORTADA ============
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("INFORME DE COSTOS DE VIAJE", title_style))
    elements.append(Paragraph(f"Sistema de Gestión de Flota", ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=colors.grey)))
    elements.append(Spacer(1, 0.3 * inch))
    
    # Cuadro de información principal
    info_principal = [
        ["INFORMACIÓN DEL VIAJE", ""],
        ["N° de Viaje:", f"{viaje.id}"],
        ["Fecha de Informe:", datetime.now().strftime('%d/%m/%Y %H:%M')],
        ["Estado del Viaje:", viaje.get_estado_display()],
    ]
    
    info_table = Table(info_principal, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_table)
    
    elements.append(Spacer(1, 0.4 * inch))
    
    # ============ RESUMEN EJECUTIVO ============
    elements.append(Paragraph("RESUMEN EJECUTIVO", subtitle_style))
    elements.append(Spacer(1, 0.1 * inch))
    
    # Calcular totales y métricas
    total_litros = sum(p.litros_cargados for p in costos.puntos_recarga.all())
    km_recorridos = costos.km_final - costos.km_inicial if costos.km_final and costos.km_inicial else 0
    consumo_promedio = km_recorridos / total_litros if total_litros > 0 else 0
    
    resumen_ejecutivo = [
        ["CONCEPTO", "VALOR"],
        ["Costo Total del Viaje", f"${costos.costo_total:,.0f}"],
        ["Kilometraje Recorrido", f"{km_recorridos:,.2f} km"],
        ["Combustible Consumido", f"{total_litros:,.2f} litros"],
        ["Consumo Promedio", f"{consumo_promedio:,.1f} km/L" if consumo_promedio > 0 else "N/A"],
        ["Número de Pasajeros", f"{viaje.get_pasajeros_count()} / {bus.capacidad_pasajeros}"],
    ]
    
    resumen_table = Table(resumen_ejecutivo, colWidths=[3*inch, 3*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e8f5e9')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 14),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#2e7d32')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(resumen_table)
    
    # ============ DATOS DEL BUS ============
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("DATOS DEL VEHÍCULO", subtitle_style))
    
    datos_bus_data = [
        ["Placa", bus.placa, "Marca", bus.marca],
        ["Modelo", bus.modelo, "Año", str(bus.año_fabricacion)],
        ["Capacidad", f"{bus.capacidad_pasajeros} pasajeros", "Km de Ingreso", f"{bus.kilometraje_ingreso:,.0f} km"],
        ["Estado", bus.get_estado_display(), "Chasis", bus.numero_chasis],
    ]
    
    datos_bus_table = Table(datos_bus_data, colWidths=[1.3*inch, 1.7*inch, 1.5*inch, 1.5*inch])
    datos_bus_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f5f5f5')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(datos_bus_table)
    
    # ============ DATOS DEL CONDUCTOR ============
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("DATOS DEL CONDUCTOR", subtitle_style))
    
    años_servicio = ((datetime.now().date() - conductor.fecha_contratacion).days // 365) if conductor.fecha_contratacion else 0
    
    datos_conductor_data = [
        ["Nombre Completo", f"{conductor.nombre} {conductor.apellido}"],
        ["Cédula", conductor.cedula if hasattr(conductor, 'cedula') else "N/A"],
        ["Teléfono", conductor.telefono],
        ["Correo Electrónico", conductor.email],
        ["Tipo de Licencia", conductor.licencias],
        ["Fecha de Contratación", conductor.fecha_contratacion.strftime('%d/%m/%Y') if conductor.fecha_contratacion else "N/A"],
        ["Años de Servicio", f"{años_servicio} años"],
    ]
    
    datos_conductor_table = Table(datos_conductor_data, colWidths=[2*inch, 4*inch])
    datos_conductor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(datos_conductor_table)
    
    # ============ DATOS DE RUTA ============
    elements.append(PageBreak())
    elements.append(Paragraph("INFORMACIÓN DE RUTA", subtitle_style))
    
    datos_ruta_data = [
        ["Origen", viaje.get_origen_display()],
        ["Coordenadas Origen", f"Lat: {viaje.latitud_origen}, Lng: {viaje.longitud_origen}" if viaje.latitud_origen else "N/A"],
        ["Destino", viaje.get_destino_display()],
        ["Coordenadas Destino", f"Lat: {viaje.latitud_destino}, Lng: {viaje.longitud_destino}" if viaje.latitud_destino else "N/A"],
        ["Fecha y Hora de Salida", viaje.fecha_salida.strftime('%d/%m/%Y %H:%M')],
        ["Fecha y Hora de Llegada Estimada", viaje.fecha_llegada_estimada.strftime('%d/%m/%Y %H:%M')],
        ["Distancia Ideal", f"{viaje.distancia_km:,.2f} km" if viaje.distancia_km else "No calculada"],
        ["Kilometraje Inicial", f"{costos.km_inicial:,.2f} km" if costos.km_inicial else "N/A"],
        ["Kilometraje Final", f"{costos.km_final:,.2f} km" if costos.km_final else "N/A"],
        ["Kilometraje Real Recorrido", f"{km_recorridos:,.2f} km"],
    ]
    
    if viaje.observaciones:
        datos_ruta_data.append(["Observaciones", viaje.observaciones])
    
    datos_ruta_table = Table(datos_ruta_data, colWidths=[2.5*inch, 3.5*inch])
    datos_ruta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(datos_ruta_table)
    
    # ============ DESGLOSE DE COSTOS ============
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("DESGLOSE DETALLADO DE COSTOS", subtitle_style))
    
    desglose_data = [
        ["CONCEPTO", "MONTO", "% DEL TOTAL"],
        ["Combustible", f"${costos.combustible:,.0f}", f"{(costos.combustible/costos.costo_total*100):.1f}%" if costos.costo_total > 0 else "0%"],
        ["Peajes", f"${costos.peajes:,.0f}", f"{(costos.peajes/costos.costo_total*100):.1f}%" if costos.costo_total > 0 else "0%"],
        ["Mantenimiento", f"${costos.mantenimiento:,.0f}", f"{(costos.mantenimiento/costos.costo_total*100):.1f}%" if costos.costo_total > 0 else "0%"],
        ["Otros Costos", f"${costos.otros_costos:,.0f}", f"{(costos.otros_costos/costos.costo_total*100):.1f}%" if costos.costo_total > 0 else "0%"],
    ]
    
    desglose_table = Table(desglose_data, colWidths=[3*inch, 1.75*inch, 1.25*inch])
    desglose_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(desglose_table)
    
    # Total
    total_data = [["COSTO TOTAL DEL VIAJE", f"${costos.costo_total:,.0f}", "100%"]]
    total_table = Table(total_data, colWidths=[3*inch, 1.75*inch, 1.25*inch])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2e7d32')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 2, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(total_table)
    
    # ============ DETALLE DE COMBUSTIBLE ============
    elements.append(PageBreak())
    elements.append(Paragraph("DETALLE DE RECARGAS DE COMBUSTIBLE", subtitle_style))
    
    puntos = costos.puntos_recarga.all().order_by('orden')
    if puntos:
        elements.append(Paragraph(f"Total de recargas realizadas: {puntos.count()}", info_style))
        elements.append(Spacer(1, 0.1 * inch))
        
        puntos_data = [["#", "Ubicación", "Km", "Km Rec.", "Litros", "Precio/L", "Costo", "Consumo"]]
        for p in puntos:
            consumo_parcial = p.kilometros_recorridos / p.litros_cargados if p.litros_cargados > 0 else 0
            puntos_data.append([
                str(p.orden),
                p.ubicacion[:20] if p.ubicacion else "N/A",
                f"{p.kilometraje:,.0f}",
                f"{p.kilometros_recorridos:,.0f}",
                f"{p.litros_cargados:,.1f}",
                f"${p.precio_combustible:,.0f}",
                f"${p.costo_total:,.0f}",
                f"{consumo_parcial:.1f}" if consumo_parcial > 0 else "N/A"
            ])
        
        # Totales
        total_km_rec = sum(p.kilometros_recorridos for p in puntos)
        puntos_data.append([
            "", "TOTALES", "", 
            f"{total_km_rec:,.0f}",
            f"{total_litros:,.1f}",
            "",
            f"${costos.combustible:,.0f}",
            f"{consumo_promedio:.1f}" if consumo_promedio > 0 else "N/A"
        ])
        
        puntos_table = Table(puntos_data, colWidths=[0.4*inch, 1.5*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.8*inch, 0.9*inch, 0.7*inch])
        puntos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196f3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -2), 'LEFT'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e9')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(puntos_table)
        
        # Agregar observaciones de recargas si existen
        obs_recargas = [p for p in puntos if p.observaciones]
        if obs_recargas:
            elements.append(Spacer(1, 0.15 * inch))
            elements.append(Paragraph("<b>Observaciones de Recargas:</b>", info_style))
            for p in obs_recargas:
                elements.append(Paragraph(f"• Recarga #{p.orden}: {p.observaciones}", info_style))
    else:
        elements.append(Paragraph("No se registraron recargas de combustible.", info_style))
    
    # ============ DETALLE DE PEAJES ============
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("DETALLE DE PEAJES", subtitle_style))
    
    peajes = viaje.peajes.all().order_by('fecha_pago')
    if peajes:
        elements.append(Paragraph(f"Total de peajes pagados: {peajes.count()}", info_style))
        elements.append(Spacer(1, 0.1 * inch))
        
        peajes_data = [["#", "Lugar", "Fecha y Hora", "Monto", "Comprobante"]]
        for idx, p in enumerate(peajes, 1):
            # Obtener el nombre del archivo si existe
            comprobante_nombre = ""
            if p.comprobante:
                try:
                    comprobante_nombre = p.comprobante.name.split('/')[-1] if p.comprobante.name else "Sin nombre"
                    if len(comprobante_nombre) > 15:
                        comprobante_nombre = comprobante_nombre[:15] + "..."
                except:
                    comprobante_nombre = "Adjunto"
            else:
                comprobante_nombre = "Sin comprobante"
            
            peajes_data.append([
                str(idx),
                p.lugar,
                p.fecha_pago.strftime('%d/%m/%Y %H:%M'),
                f"${p.monto:,.0f}",
                comprobante_nombre
            ])
        
        peajes_data.append(["", "TOTAL", "", f"${costos.peajes:,.0f}", ""])
        
        peajes_table = Table(peajes_data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 1*inch, 1.5*inch])
        peajes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196f3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -2), 'LEFT'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e9')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(peajes_table)
    else:
        elements.append(Paragraph("No se registraron peajes en este viaje.", info_style))
    
    # ============ MANTENIMIENTOS ============
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("MANTENIMIENTOS REALIZADOS", subtitle_style))
    
    mantenimientos = costos.mantenimientos.all().order_by('fecha_mantenimiento')
    if mantenimientos:
        elements.append(Paragraph(f"Total de mantenimientos: {mantenimientos.count()}", info_style))
        elements.append(Spacer(1, 0.1 * inch))
        
        mant_data = [["#", "Tipo", "Descripción", "Fecha", "Km", "Costo"]]
        for idx, m in enumerate(mantenimientos, 1):
            mant_data.append([
                str(idx),
                m.get_tipo_display(),
                m.descripcion[:30] + "..." if len(m.descripcion) > 30 else m.descripcion,
                m.fecha_mantenimiento.strftime('%d/%m/%Y'),
                f"{m.kilometraje:,.0f}",
                f"${m.costo:,.0f}"
            ])
        
        mant_data.append(["", "TOTAL", "", "", "", f"${costos.mantenimiento:,.0f}"])
        
        mant_table = Table(mant_data, colWidths=[0.5*inch, 1.2*inch, 2.3*inch, 1*inch, 0.8*inch, 0.8*inch])
        mant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196f3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -2), 'LEFT'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e9')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(mant_table)
    else:
        elements.append(Paragraph("No se realizaron mantenimientos durante este viaje.", info_style))
    
    # ============ OTROS COSTOS ============
    if costos.otros_costos > 0:
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("OTROS COSTOS", subtitle_style))
        elements.append(Paragraph(f"<b>Monto:</b> ${costos.otros_costos:,.0f}", info_style))
        if costos.observaciones:
            elements.append(Paragraph(f"<b>Justificación:</b> {costos.observaciones}", info_style))
    
    # ============ LISTA DE PASAJEROS ============
    elements.append(PageBreak())
    elements.append(Paragraph("LISTA DE PASAJEROS", subtitle_style))
    
    pasajeros = viaje.pasajeros.all()
    if pasajeros:
        elements.append(Paragraph(f"Total de pasajeros: {pasajeros.count()} de {bus.capacidad_pasajeros} disponibles ({(pasajeros.count()/bus.capacidad_pasajeros*100):.1f}% de ocupación)", info_style))
        elements.append(Spacer(1, 0.1 * inch))
        
        pasajeros_data = [["#", "Nombre Completo", "RUT", "Teléfono", "Correo Electrónico"]]
        for idx, pasajero in enumerate(pasajeros, 1):
            pasajeros_data.append([
                str(idx),
                pasajero.nombre_completo,
                getattr(pasajero, 'rut', 'N/A'),
                getattr(pasajero, 'telefono', 'N/A'),
                getattr(pasajero, 'correo', 'N/A')
            ])
        
        pasajeros_table = Table(pasajeros_data, colWidths=[0.4*inch, 2*inch, 1.2*inch, 1.2*inch, 1.7*inch])
        pasajeros_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(pasajeros_table)
    else:
        elements.append(Paragraph("No hay pasajeros registrados para este viaje.", info_style))
    
    # ============ ANÁLISIS Y CONCLUSIONES ============
    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph("ANÁLISIS Y MÉTRICAS", subtitle_style))
    
    # Calcular costo por kilómetro y por pasajero (con validación de división por cero)
    from decimal import Decimal
    costo_por_km = Decimal('0')
    if km_recorridos > 0:
        try:
            costo_por_km = costos.costo_total / Decimal(str(km_recorridos))
        except:
            costo_por_km = Decimal('0')
    
    costo_por_pasajero = Decimal('0')
    num_pasajeros = pasajeros.count()
    if num_pasajeros > 0:
        try:
            costo_por_pasajero = costos.costo_total / Decimal(str(num_pasajeros))
        except:
            costo_por_pasajero = Decimal('0')
    
    # Porcentajes de distribución (con validación)
    porcentaje_combustible = Decimal('0')
    porcentaje_peajes = Decimal('0')
    porcentaje_mantenimiento = Decimal('0')
    porcentaje_otros = Decimal('0')
    
    if costos.costo_total > 0:
        try:
            porcentaje_combustible = (costos.combustible / costos.costo_total * 100)
            porcentaje_peajes = (costos.peajes / costos.costo_total * 100)
            porcentaje_mantenimiento = (costos.mantenimiento / costos.costo_total * 100)
            porcentaje_otros = (costos.otros_costos / costos.costo_total * 100)
        except:
            pass
    
    # Tasa de ocupación
    tasa_ocupacion = Decimal('0')
    if bus.capacidad_pasajeros > 0:
        try:
            tasa_ocupacion = (Decimal(str(num_pasajeros)) / Decimal(str(bus.capacidad_pasajeros)) * 100)
        except:
            tasa_ocupacion = Decimal('0')
    
    analisis_texto = f"""
    <b>Costo por Kilómetro:</b> ${costo_por_km:,.2f}/km<br/>
    <b>Costo por Pasajero:</b> ${costo_por_pasajero:,.2f}<br/>
    <b>Eficiencia de Combustible:</b> {consumo_promedio:,.1f} km/L<br/>
    <b>Tasa de Ocupación:</b> {tasa_ocupacion:.1f}%<br/>
    <br/>
    <b>Distribución de Costos:</b><br/>
    • El combustible representa el {porcentaje_combustible:.1f}% del costo total<br/>
    • Los peajes representan el {porcentaje_peajes:.1f}% del costo total<br/>
    • El mantenimiento representa el {porcentaje_mantenimiento:.1f}% del costo total<br/>
    • Otros costos representan el {porcentaje_otros:.1f}% del costo total
    """
    elements.append(Paragraph(analisis_texto, info_style))
    
    # ============ PIE DE PÁGINA ============
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("_" * 80, info_style))
    elements.append(Paragraph(
        f"<i>Informe generado automáticamente el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}</i><br/>"
        f"<i>Sistema de Gestión de Flota - FlotaGest © {datetime.now().year}</i>",
        ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))
    
    # Construir el PDF
    doc.build(elements)
    return response


def informe_ida_vuelta_pdf(request, costos_ida_pk):
    """
    Genera un PDF combinado con los costos de los viajes de ida y vuelta
    """
    costos_ida = get_object_or_404(CostosViaje, pk=costos_ida_pk)
    viaje_ida = costos_ida.viaje
    
    # Obtener costos de vuelta
    costos_vuelta = None
    viaje_vuelta = None
    if viaje_ida.es_ida_vuelta and viaje_ida.viaje_relacionado:
        try:
            costos_vuelta = CostosViaje.objects.get(viaje=viaje_ida.viaje_relacionado)
            viaje_vuelta = costos_vuelta.viaje
        except CostosViaje.DoesNotExist:
            pass
    
    bus = viaje_ida.bus
    conductor = viaje_ida.conductor
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_ida_vuelta_{viaje_ida.id}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica-Bold',
        leading=26
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0d47a1'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#e3f2fd')
    )
    
    info_style = ParagraphStyle(
        'CustomInfo',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        leading=14
    )
    
    # ============ PORTADA ============
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("INFORME DE COSTOS - VIAJE IDA Y VUELTA", title_style))
    elements.append(Paragraph(f"Sistema de Gestión de Flota", ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=colors.grey)))
    elements.append(Spacer(1, 0.3 * inch))
    
    # Información del Bus y Conductor
    info_principal = [
        ["INFORMACIÓN GENERAL", ""],
        ["Bus:", f"{bus.placa} - {bus.modelo}"],
        ["Conductor:", f"{conductor.nombre} {conductor.apellido}"],
        ["Fecha de Informe:", datetime.now().strftime('%d/%m/%Y %H:%M')],
    ]
    
    info_table = Table(info_principal, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # ============ RESUMEN GENERAL ============
    if costos_vuelta:
        elements.append(Paragraph("RESUMEN GENERAL DEL VIAJE COMPLETO", subtitle_style))
        
        total_combustible = costos_ida.combustible + costos_vuelta.combustible
        total_peajes = costos_ida.peajes + costos_vuelta.peajes
        total_mantenimiento = costos_ida.mantenimiento + costos_vuelta.mantenimiento
        total_otros = costos_ida.otros_costos + costos_vuelta.otros_costos
        total_general = costos_ida.costo_total + costos_vuelta.costo_total
        
        resumen_data = [
            ["CONCEPTO", "MONTO"],
            ["Combustible Total", f"${total_combustible:,.0f}"],
            ["Peajes Total", f"${total_peajes:,.0f}"],
            ["Mantenimiento Total", f"${total_mantenimiento:,.0f}"],
            ["Otros Costos", f"${total_otros:,.0f}"],
            ["COSTO TOTAL", f"${total_general:,.0f}"],
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 3*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#4caf50')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
        ]))
        elements.append(resumen_table)
        elements.append(Spacer(1, 0.3 * inch))
    
    # ============ VIAJE DE IDA ============
    elements.append(PageBreak())
    elements.append(Paragraph("🡢 VIAJE DE IDA", subtitle_style))
    
    viaje_ida_data = [
        ["Ruta:", f"{viaje_ida.get_origen_display()} → {viaje_ida.get_destino_display()}"],
        ["Fecha Salida:", viaje_ida.fecha_salida.strftime('%d/%m/%Y %H:%M')],
        ["Estado:", viaje_ida.get_estado_display()],
        ["Pasajeros:", str(viaje_ida.pasajeros.count())],
    ]
    
    if costos_ida.km_inicial and costos_ida.km_final:
        viaje_ida_data.extend([
            ["Km Inicial:", f"{costos_ida.km_inicial:,.0f} km"],
            ["Km Final:", f"{costos_ida.km_final:,.0f} km"],
            ["Km Recorridos:", f"{costos_ida.km_final - costos_ida.km_inicial:,.0f} km"],
        ])
    
    ida_table = Table(viaje_ida_data, colWidths=[2*inch, 4*inch])
    ida_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e3f2fd')),
    ]))
    elements.append(ida_table)
    elements.append(Spacer(1, 0.2 * inch))
    
    # Costos del viaje de ida
    costos_ida_data = [
        ["CONCEPTO", "MONTO"],
        ["Combustible", f"${costos_ida.combustible:,.0f}"],
        ["Peajes", f"${costos_ida.peajes:,.0f}"],
        ["Mantenimiento", f"${costos_ida.mantenimiento:,.0f}"],
        ["Otros Costos", f"${costos_ida.otros_costos:,.0f}"],
        ["TOTAL VIAJE IDA", f"${costos_ida.costo_total:,.0f}"],
    ]
    
    costos_ida_table = Table(costos_ida_data, colWidths=[3*inch, 3*inch])
    costos_ida_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#1976D2')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
    ]))
    elements.append(costos_ida_table)
    
    # ============ VIAJE DE VUELTA ============
    if costos_vuelta and viaje_vuelta:
        elements.append(PageBreak())
        elements.append(Paragraph("🡠 VIAJE DE VUELTA", subtitle_style))
        
        viaje_vuelta_data = [
            ["Ruta:", f"{viaje_vuelta.get_origen_display()} → {viaje_vuelta.get_destino_display()}"],
            ["Fecha Salida:", viaje_vuelta.fecha_salida.strftime('%d/%m/%Y %H:%M')],
            ["Estado:", viaje_vuelta.get_estado_display()],
            ["Pasajeros:", str(viaje_vuelta.pasajeros.count())],
        ]
        
        if costos_vuelta.km_inicial and costos_vuelta.km_final:
            viaje_vuelta_data.extend([
                ["Km Inicial:", f"{costos_vuelta.km_inicial:,.0f} km"],
                ["Km Final:", f"{costos_vuelta.km_final:,.0f} km"],
                ["Km Recorridos:", f"{costos_vuelta.km_final - costos_vuelta.km_inicial:,.0f} km"],
            ])
        
        vuelta_table = Table(viaje_vuelta_data, colWidths=[2*inch, 4*inch])
        vuelta_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3e0')),
        ]))
        elements.append(vuelta_table)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Costos del viaje de vuelta
        costos_vuelta_data = [
            ["CONCEPTO", "MONTO"],
            ["Combustible", f"${costos_vuelta.combustible:,.0f}"],
            ["Peajes", f"${costos_vuelta.peajes:,.0f}"],
            ["Mantenimiento", f"${costos_vuelta.mantenimiento:,.0f}"],
            ["Otros Costos", f"${costos_vuelta.otros_costos:,.0f}"],
            ["TOTAL VIAJE VUELTA", f"${costos_vuelta.costo_total:,.0f}"],
        ]
        
        costos_vuelta_table = Table(costos_vuelta_data, colWidths=[3*inch, 3*inch])
        costos_vuelta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F57C00')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
        ]))
        elements.append(costos_vuelta_table)
    
    # ============ PIE DE PÁGINA ============
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("_" * 80, info_style))
    elements.append(Paragraph(
        f"<i>Informe generado automáticamente el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}</i><br/>"
        f"<i>Sistema de Gestión de Flota - FlotaGest © {datetime.now().year}</i>",
        ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))
    
    # Construir el PDF
    doc.build(elements)
    return response
