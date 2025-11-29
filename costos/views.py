from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.http import JsonResponse, HttpResponse
from .models import CostosViaje, Peaje, PuntoRecarga
from .forms import CostosViajeForm, PuntoRecargaForm
from viajes.models import Viaje
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io


class CostosViajeListView(LoginRequiredMixin, ListView):
    """Vista para listar todos los costos de viajes."""
    model = CostosViaje
    template_name = 'costos/costos_list.html'
    context_object_name = 'costos_list'
    paginate_by = 10

    def get_queryset(self):
        return CostosViaje.objects.select_related('viaje', 'viaje__bus').prefetch_related('puntos_recarga')


class ViajesSinCostosListView(LoginRequiredMixin, ListView):
    """Vista para listar viajes que no tienen costos asignados."""
    model = Viaje
    template_name = 'costos/viajes_sin_costos.html'
    context_object_name = 'viajes'
    paginate_by = 10

    def get_queryset(self):
        viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
        return Viaje.objects.exclude(id__in=viajes_con_costos).select_related('bus', 'conductor', 'lugar_origen', 'lugar_destino')


class CostosViajeCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear costos de un viaje."""
    model = CostosViaje
    form_class = CostosViajeForm
    template_name = 'costos/costos_form.html'
    success_url = reverse_lazy('costos:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Costos del viaje creados exitosamente.')
        return super().form_valid(form)


class CostosViajeDetailView(LoginRequiredMixin, DetailView):
    """Vista para ver detalles de costos de un viaje."""
    model = CostosViaje
    template_name = 'costos/costos_detail.html'
    context_object_name = 'costos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puntos_recarga'] = self.object.puntos_recarga.all()
        context['total_kilometros'] = sum(p.kilometros_recorridos for p in context['puntos_recarga'])
        context['total_litros'] = sum(p.litros_cargados for p in context['puntos_recarga'])
        return context


class CostosViajeUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar costos de un viaje."""
    model = CostosViaje
    form_class = CostosViajeForm
    template_name = 'costos/costos_form.html'

    def get_success_url(self):
        return reverse_lazy('costos:detalle', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Costos del viaje actualizados exitosamente.')
        return super().form_valid(form)


class CostosViajeDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar costos de un viaje."""
    model = CostosViaje
    template_name = 'costos/costos_confirm_delete.html'
    success_url = reverse_lazy('costos:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Costos del viaje eliminados exitosamente.')
        return super().delete(request, *args, **kwargs)


class PuntoRecargaCreateView(LoginRequiredMixin, CreateView):
    """Vista para agregar un punto de recarga a un viaje."""
    model = PuntoRecarga
    form_class = PuntoRecargaForm
    template_name = 'costos/punto_recarga_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        costos_viaje = get_object_or_404(CostosViaje, pk=self.kwargs['costos_pk'])
        kwargs['costos_viaje'] = costos_viaje
        return kwargs

    def form_valid(self, form):
        costos_viaje = get_object_or_404(CostosViaje, pk=self.kwargs['costos_pk'])
        form.instance.costos_viaje = costos_viaje
        response = super().form_valid(form)
        
        # Recalcular el costo total de combustible
        costos_viaje.calcular_costo_combustible()
        costos_viaje.save()
        
        messages.success(self.request, 'Punto de recarga agregado exitosamente.')
        return response

    def get_success_url(self):
        return reverse_lazy('costos:detalle', kwargs={'pk': self.kwargs['costos_pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costos_viaje'] = get_object_or_404(CostosViaje, pk=self.kwargs['costos_pk'])
        return context


class PuntoRecargaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para editar un punto de recarga."""
    model = PuntoRecarga
    form_class = PuntoRecargaForm
    template_name = 'costos/punto_recarga_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['costos_viaje'] = self.object.costos_viaje
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Recalcular el costo total de combustible
        self.object.costos_viaje.calcular_costo_combustible()
        self.object.costos_viaje.save()
        
        messages.success(self.request, 'Punto de recarga actualizado exitosamente.')
        return response

    def get_success_url(self):
        return reverse_lazy('costos:detalle', kwargs={'pk': self.object.costos_viaje.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costos_viaje'] = self.object.costos_viaje
        return context


class PuntoRecargaDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar un punto de recarga."""
    model = PuntoRecarga
    template_name = 'costos/punto_recarga_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        punto = self.get_object()
        costos_viaje = punto.costos_viaje
        response = super().delete(request, *args, **kwargs)
        
        # Recalcular el costo total de combustible
        costos_viaje.calcular_costo_combustible()
        costos_viaje.save()
        
        messages.success(request, 'Punto de recarga eliminado exitosamente.')
        return response

    def get_success_url(self):
        return reverse_lazy('costos:detalle', kwargs={'pk': self.object.costos_viaje.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costos_viaje'] = self.object.costos_viaje
        return context


class GestionCostosView(LoginRequiredMixin, View):
    """Vista principal para gestionar costos de viajes."""
    template_name = 'costos/gestion_costos.html'

    def get(self, request):
        # Obtener viajes sin costos asignados
        viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
        viajes_sin_costos = Viaje.objects.exclude(id__in=viajes_con_costos).select_related('bus', 'conductor')[:5]
        
        # Obtener últimos costos registrados
        ultimos_costos = CostosViaje.objects.select_related('viaje', 'viaje__bus').prefetch_related('puntos_recarga')[:5]
        
        # Estadísticas
        total_viajes_con_costos = CostosViaje.objects.count()
        total_viajes = Viaje.objects.count()
        
        context = {
            'viajes_sin_costos': viajes_sin_costos,
            'ultimos_costos': ultimos_costos,
            'total_viajes_con_costos': total_viajes_con_costos,
            'total_viajes': total_viajes,
        }
        
        return render(request, self.template_name, context)


def calcular_distancia_viaje(request, viaje_id):
    """Vista AJAX para calcular la distancia de un viaje."""
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Método no permitido'}, status=405)
        
        viaje = get_object_or_404(Viaje, pk=viaje_id)
        
        # Obtener coordenadas de los lugares relacionados o del viaje
        try:
            lat_origen = viaje.latitud_origen if viaje.latitud_origen else viaje.lugar_origen.latitud
            lon_origen = viaje.longitud_origen if viaje.longitud_origen else viaje.lugar_origen.longitud
            lat_destino = viaje.latitud_destino if viaje.latitud_destino else viaje.lugar_destino.latitud
            lon_destino = viaje.longitud_destino if viaje.longitud_destino else viaje.lugar_destino.longitud
        except Exception as e:
            return JsonResponse({
                'error': f'Error al obtener coordenadas: {str(e)}'
            }, status=400)
        
        # Verificar que el viaje tenga coordenadas
        if not all([lat_origen, lon_origen, lat_destino, lon_destino]):
            return JsonResponse({
                'error': f'Faltan coordenadas. Origen: {viaje.lugar_origen.nombre} (lat: {lat_origen}, lon: {lon_origen}), Destino: {viaje.lugar_destino.nombre} (lat: {lat_destino}, lon: {lon_destino})'
            }, status=400)
        
        # Calcular la distancia
        distancia = viaje.calcular_distancia_real()
        
        if distancia:
            return JsonResponse({
                'success': True,
                'distancia_km': float(distancia),
                'mensaje': f'Distancia calculada: {distancia} km'
            })
        else:
            return JsonResponse({
                'error': 'No se pudo calcular la distancia. Verifica que las coordenadas sean correctas.'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error inesperado: {str(e)}'
        }, status=500)


def generar_formulario_costos_pdf(request, viaje_id):
    """Genera un PDF imprimible para que el conductor registre los costos manualmente."""
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    
    # Crear el objeto HttpResponse con el header PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="formulario_costos_viaje_{viaje.id}.pdf"'
    
    # Crear el PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0d47a1'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Título
    elements.append(Paragraph("FORMULARIO DE REGISTRO DE COSTOS DE VIAJE", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Información del viaje
    elements.append(Paragraph("INFORMACIÓN DEL VIAJE", heading_style))
    
    viaje_data = [
        ['Bus:', viaje.bus.placa, 'Modelo:', viaje.bus.modelo],
        ['Origen:', viaje.lugar_origen.nombre, 'Destino:', viaje.lugar_destino.nombre],
        ['Conductor:', f"{viaje.conductor.nombre} {viaje.conductor.apellido}", 'Fecha:', viaje.fecha_salida.strftime("%d/%m/%Y")],
        ['Km Inicial Bus:', f"{viaje.bus.kilometraje_inicial} km", '', ''],
    ]
    
    viaje_table = Table(viaje_data, colWidths=[1.2*inch, 2*inch, 1.2*inch, 2*inch])
    viaje_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(viaje_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de puntos de recarga
    elements.append(Paragraph("PUNTOS DE RECARGA DE COMBUSTIBLE", heading_style))
    elements.append(Paragraph("<i>Complete la siguiente tabla en cada punto de recarga durante el viaje:</i>", styles['Normal']))
    elements.append(Spacer(1, 0.1*inch))
    
    recarga_data = [
        ['N°', 'Ubicación/Gasolinera', 'Kilometraje\n(km)', 'Litros\nCargados', 'Precio por\nLitro (CLP)']
    ]
    
    # Agregar 8 filas vacías para completar
    for i in range(1, 9):
        recarga_data.append([str(i), '', '', '', ''])
    
    recarga_table = Table(recarga_data, colWidths=[0.4*inch, 2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    recarga_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWHEIGHT', (0, 1), (-1, -1), 0.4*inch),
    ]))
    
    elements.append(recarga_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Otros costos
    elements.append(Paragraph("OTROS COSTOS", heading_style))
    
    otros_data = [
        ['Concepto', 'Monto (CLP)'],
        ['Mantenimiento', ''],
        ['Peajes', ''],
        ['Otros gastos', ''],
    ]
    
    otros_table = Table(otros_data, colWidths=[4*inch, 2.5*inch])
    otros_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWHEIGHT', (0, 1), (-1, -1), 0.35*inch),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(otros_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Observaciones
    elements.append(Paragraph("OBSERVACIONES", heading_style))
    obs_data = [['', '', '', '']] * 3
    obs_table = Table(obs_data, colWidths=[6.5*inch/4]*4, rowHeights=[0.3*inch]*3)
    obs_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(obs_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Firmas
    elements.append(Spacer(1, 0.3*inch))
    firma_data = [
        ['_'*30, '_'*30],
        ['Firma del Conductor', 'Fecha'],
    ]
    firma_table = Table(firma_data, colWidths=[3*inch, 3*inch])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(firma_table)
    
    # Pie de página
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(
        f"<i>Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema de Gestión de Flota</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))
    
    # Construir PDF
    doc.build(elements)
    
    # Obtener el valor del buffer y escribirlo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
