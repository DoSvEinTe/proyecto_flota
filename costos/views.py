from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from .models import Peaje
class PeajeDeleteView(LoginRequiredMixin, DeleteView):
    model = Peaje
    template_name = 'costos/peaje_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        peaje = self.get_object()
        costos_viaje = CostosViaje.objects.filter(viaje=peaje.viaje).first()
        response = super().delete(request, *args, **kwargs)
        # Recalcular el total de peajes
        if costos_viaje:
            costos_viaje.peajes = sum(p.monto for p in peaje.viaje.peajes.all())
            costos_viaje.save()
        messages.success(request, 'Peaje eliminado exitosamente.')
        return response

    def get_success_url(self):
        costos_viaje = CostosViaje.objects.filter(viaje=self.object.viaje).first()
        if costos_viaje:
            return reverse_lazy('costos:registrar_peajes', kwargs={'costos_pk': costos_viaje.pk})
        return reverse_lazy('costos:gestion')
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, RedirectView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.http import JsonResponse, HttpResponse
from .models import CostosViaje, Peaje, PuntoRecarga
from .forms import CostosViajeForm, PuntoRecargaForm, KmInicialForm, KmFinalForm, CostosViajeFormCompleto
from flota.models import Mantenimiento
from flota.forms import MantenimientoForm
from viajes.models import Viaje
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io
from flota.models import Mantenimiento
from .informe_costos import informe_costos_pdf


class RedirectToViajesSinCostos(LoginRequiredMixin, RedirectView):
    """Redirección de la URL antigua a la lista de viajes sin costos."""
    pattern_name = 'costos:viajes_sin_costos'
    permanent = False


class CostosViajeListView(LoginRequiredMixin, ListView):
    """Vista para listar todos los costos de viajes."""
    model = CostosViaje
    template_name = 'costos/costos_list.html'
    context_object_name = 'costos_list'
    paginate_by = 10

    def get_queryset(self):
        return CostosViaje.objects.select_related('viaje', 'viaje__bus').prefetch_related('puntos_recarga')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener viajes sin costos asignados
        viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
        context['viajes_sin_costos'] = Viaje.objects.exclude(id__in=viajes_con_costos).select_related('bus', 'conductor', 'lugar_origen', 'lugar_destino')
        return context


class ViajesSinCostosListView(LoginRequiredMixin, ListView):
    """Vista para listar viajes que no tienen costos asignados."""
    model = Viaje
    template_name = 'costos/viajes_sin_costos.html'
    context_object_name = 'viajes'
    paginate_by = 10

    def get_queryset(self):
        viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
        return Viaje.objects.exclude(id__in=viajes_con_costos).select_related('bus', 'conductor', 'lugar_origen', 'lugar_destino')


class CostosViajeCreateView(LoginRequiredMixin, View):
    template_name = 'costos/seleccionar_viaje.html'

    def get(self, request):
        viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
        viajes = Viaje.objects.exclude(id__in=viajes_con_costos)
        return render(request, self.template_name, {'viajes': viajes})

    def post(self, request):
        viaje_id = request.POST.get('viaje')
        if viaje_id:
            viaje = Viaje.objects.get(pk=viaje_id)
            costos_viaje = CostosViaje.objects.create(viaje=viaje)
            return redirect('costos:registrar_km_inicial', costos_pk=costos_viaje.pk)
        viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
        viajes = Viaje.objects.exclude(id__in=viajes_con_costos)
        messages.error(request, 'Debes seleccionar un viaje.')
        return render(request, self.template_name, {'viajes': viajes})

def mantenimiento_costos(request, costos_pk):
    costos_viaje = get_object_or_404(CostosViaje, pk=costos_pk)
    bus = costos_viaje.viaje.bus
    if request.method == 'POST':
        if 'omitir' in request.POST:
            return redirect('costos:detalle', pk=costos_pk)
        from decimal import Decimal
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.bus = bus
            mantenimiento.save()
            costos_viaje.mantenimientos.add(mantenimiento)
            costos_viaje.mantenimiento += Decimal(str(mantenimiento.costo))
            costos_viaje.save()
            return redirect('costos:detalle', pk=costos_pk)
    else:
        form = MantenimientoForm()
    mantenimientos_registrados = list(costos_viaje.mantenimientos.all().order_by('-fecha_mantenimiento'))
    return render(request, 'costos/mantenimiento_costos_form.html', {
        'form': form,
        'bus': bus,
        'costos_pk': costos_pk,
        'mantenimientos_registrados': mantenimientos_registrados
    })

def otros_costos(request, costos_pk):
    costos_viaje = get_object_or_404(CostosViaje, pk=costos_pk)
    if request.method == 'POST':
        otros_costos = request.POST.get('otros_costos')
        justificacion_otros = request.POST.get('justificacion_otros_costos')
        if otros_costos:
            try:
                costos_viaje.otros_costos = float(otros_costos)
            except Exception:
                costos_viaje.otros_costos = 0
            if justificacion_otros:
                costos_viaje.observaciones = (costos_viaje.observaciones or '') + f"\nJustificación otros costos: {justificacion_otros}"
            costos_viaje.save()
        return redirect('costos:detalle', pk=costos_pk)
    return render(request, 'costos/otros_costos_form.html', {'costos_pk': costos_pk})
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
        # Calculo real de km recorridos
        if self.object.km_final is not None and self.object.km_inicial is not None:
            context['km_recorridos_real'] = self.object.km_final - self.object.km_inicial
        else:
            context['km_recorridos_real'] = context['total_kilometros']
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
        costos_viaje = self.get_object()
        # Eliminar puntos de recarga asociados a este registro de costos
        costos_viaje.puntos_recarga.all().delete()
        # Eliminar peajes asociados a este registro de costos
        costos_viaje.peajes.all().delete()
        # Eliminar mantenimientos solo si no están asociados a otros costos
        for mantenimiento in costos_viaje.mantenimientos.all():
            if mantenimiento.costos_viaje.count() == 1:
                mantenimiento.delete()
        messages.success(request, 'Costos del viaje y registros asociados eliminados exitosamente.')
        return super().delete(request, *args, **kwargs)


def agregar_puntos_recarga(request, costos_pk):
    costos_viaje = get_object_or_404(CostosViaje, pk=costos_pk)
    if request.method == 'POST':
        from decimal import Decimal
        recargas = []
        for key in request.POST:
            if key.startswith('recarga_ubicacion_'):
                idx = key.split('_')[-1]
                ubicacion = request.POST.get(f'recarga_ubicacion_{idx}')
                kilometraje = request.POST.get(f'recarga_kilometraje_{idx}')
                litros = request.POST.get(f'recarga_litros_{idx}')
                valor = request.POST.get(f'recarga_valor_{idx}')
                if ubicacion and kilometraje and litros and valor:
                    punto = PuntoRecarga.objects.create(
                        costos_viaje=costos_viaje,
                        orden=int(idx),
                        kilometraje=Decimal(kilometraje),
                        precio_combustible=Decimal(valor),
                        litros_cargados=Decimal(litros),
                        ubicacion=ubicacion
                    )
                    recargas.append(punto)
        costos_viaje.calcular_costo_combustible()
        costos_viaje.save()
        # Si ya tiene km_final, ir al detalle, si no, pedir km_final
        if costos_viaje.km_final is not None:
            return redirect('costos:detalle', pk=costos_pk)
        return redirect('costos:registrar_km_final', costos_pk=costos_pk)
    return render(request, 'costos/punto_recarga_form.html', {'costos_viaje': costos_viaje})


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

        # Obtener todos los costos registrados para el CRUD
        costos_list = CostosViaje.objects.select_related('viaje', 'viaje__bus').prefetch_related('puntos_recarga').all()

        # Estadísticas
        total_viajes_con_costos = CostosViaje.objects.count()
        total_viajes = Viaje.objects.count()

        context = {
            'viajes_sin_costos': viajes_sin_costos,
            'costos_list': costos_list,
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
    from reportlab.platypus import Table, PageBreak
    """Genera un PDF imprimible para que el conductor registre los costos manualmente."""
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    # Response PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="formulario_costos_viaje_{viaje.id}.pdf"'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=18
    )
    elements = []
    # ================================
    # ESTILOS
    # ================================
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_CENTER,
        spaceAfter=25,
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0d47a1'),
        spaceAfter=14,
        fontName='Helvetica-Bold'
    )
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    # ================================
    # HOJA 1 - Información del Viaje
    # ================================
    elements.append(Paragraph("FORMULARIO DE REGISTRO DE COSTOS DE VIAJE", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("INFORMACIÓN DEL VIAJE", subtitle_style))
    costos_viaje = CostosViaje.objects.filter(viaje=viaje).first()
    km_inicial = costos_viaje.km_inicial if costos_viaje and costos_viaje.km_inicial is not None else viaje.bus.kilometraje_inicial
    info_viaje = [
        f"<b>Bus:</b> {viaje.bus.placa} &nbsp;&nbsp;&nbsp; <b>Modelo:</b> {viaje.bus.modelo}",
        f"<b>Origen:</b> {viaje.lugar_origen.nombre} &nbsp;&nbsp;&nbsp; <b>Destino:</b> {viaje.lugar_destino.nombre}",
        f"<b>Conductor:</b> {viaje.conductor.nombre} {viaje.conductor.apellido} &nbsp;&nbsp;&nbsp; ",
        f"<b>Fecha:</b> {viaje.fecha_salida.strftime('%d/%m/%Y')}",
        f"<b>Kilometraje Inicial (real):</b> {km_inicial if km_inicial is not None else '_______________________________'}",
        f"<b>Kilometraje Final:</b> _______________________________",
    ]
    for linea in info_viaje:
        elements.append(Paragraph(linea, info_style))
    elements.append(Spacer(1, 0.3 * inch))
    # ================================
    # TABLA RECARGAS DE COMBUSTIBLE
    # ================================
    elements.append(Paragraph("REGISTRO DE RECARGAS DE COMBUSTIBLE", subtitle_style))
    elements.append(Spacer(1, 0.1 * inch))
    # Se elimina el texto de instrucción para la tabla de recargas
    recarga_data = [
        ['N°', 'Gasolinera / Ubicación', 'Kilometraje', 'Litros', 'Valor por Litro (CLP)']
    ]
    for i in range(1, 9):
        recarga_data.append([str(i), '', '', '', ''])
    recarga_table = Table(
        recarga_data,
        colWidths=[0.7 * inch, 2.2 * inch, 1.5 * inch, 1.3 * inch, 1.7 * inch]
    )
    recarga_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWHEIGHT', (0, 1), (-1, -1), 0.35 * inch),
    ]))
    elements.append(recarga_table)
    elements.append(PageBreak())
    # ================================
    # HOJA 2 - PEAJES + OBSERVACIONES
    # ================================
    elements.append(Paragraph("REGISTRO DE PEAJES DEL VIAJE", title_style))
    elements.append(Spacer(1, 0.2 * inch))
    peajes_data = [
        ['N°', 'Nombre Peaje', 'Ubicación', 'Monto (CLP)']
    ]
    for i in range(1, 8):
        peajes_data.append([str(i), '', '', ''])
    peajes_table = Table(
        peajes_data,
        colWidths=[0.7 * inch, 2.7 * inch, 2.7 * inch, 1.7 * inch]
    )
    peajes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWHEIGHT', (0, 1), (-1, -1), 0.35 * inch),
    ]))
    elements.append(peajes_table)
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("OBSERVACIONES GENERALES", subtitle_style))
    obs_box = Table([['']], colWidths=[6.5 * inch], rowHeights=[1.3 * inch])
    obs_box.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    elements.append(obs_box)
    elements.append(Spacer(1, 0.4 * inch))
    firma_data = [
        ['_' * 30, '_' * 30],
        ['Firma del Conductor', 'Fecha'],
    ]
    firma_table = Table(firma_data, colWidths=[3 * inch, 3 * inch])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    elements.append(firma_table)
    elements.append(Spacer(1, 0.2 * inch))
    # Footer
    elements.append(Paragraph(
        f"<i>Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema de Gestión de Flota</i>",
        footer_style
    ))
    # Construcción del PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def registrar_peajes(request, costos_pk):
    costos_viaje = get_object_or_404(CostosViaje, pk=costos_pk)
    if request.method == 'POST':
        # Procesar peajes
        from decimal import Decimal
        peajes = []
        for key in request.POST:
            if key.startswith('peaje_nombre_'):
                idx = key.split('_')[-1]
                nombre = request.POST.get(f'peaje_nombre_{idx}')
                ubicacion = request.POST.get(f'peaje_ubicacion_{idx}')
                monto = request.POST.get(f'peaje_monto_{idx}')
                if nombre and ubicacion and monto:
                    peaje = Peaje.objects.create(
                        viaje=costos_viaje.viaje,
                        costos_viaje=costos_viaje,
                        lugar=ubicacion,
                        monto=Decimal(monto),
                        fecha_pago=datetime.now(),
                        comprobante=""
                    )
                    peajes.append(peaje)
        # Sumar el total de peajes
        total_peajes = sum(Decimal(str(p.monto)) for p in peajes)
        costos_viaje.peajes = total_peajes
        costos_viaje.save()
        return redirect('costos:registrar_puntos_recarga', costos_pk=costos_pk)
    # Mostrar solo peajes asociados a este registro de costos
    peajes_registrados = costos_viaje.peajes_costos.all().order_by('fecha_pago')
    return render(request, 'costos/peajes_form.html', {'costos_pk': costos_pk, 'peajes_registrados': peajes_registrados})

def registrar_puntos_recarga(request, costos_pk):
    costos_viaje = get_object_or_404(CostosViaje, pk=costos_pk)
    puntos_registrados = costos_viaje.puntos_recarga.all().order_by('orden')
    if request.method == 'POST':
        from decimal import Decimal
        # Procesar puntos de recarga
        recargas = []
        for key in request.POST:
            if key.startswith('recarga_ubicacion_'):
                idx = key.split('_')[-1]
                ubicacion = request.POST.get(f'recarga_ubicacion_{idx}')
                kilometraje = request.POST.get(f'recarga_kilometraje_{idx}')
                litros = request.POST.get(f'recarga_litros_{idx}')
                valor = request.POST.get(f'recarga_valor_{idx}')
                if ubicacion and kilometraje and litros and valor:
                    punto = PuntoRecarga.objects.create(
                        costos_viaje=costos_viaje,
                        orden=int(idx),
                        kilometraje=Decimal(kilometraje),
                        precio_combustible=Decimal(valor),
                        litros_cargados=Decimal(litros),
                        ubicacion=ubicacion
                    )
                    recargas.append(punto)
        # Recalcular el costo total de combustible
        costos_viaje.calcular_costo_combustible()
        costos_viaje.save()
        # Finalizar flujo, redirigir a registro de km final
        return redirect('costos:registrar_km_final', costos_pk=costos_pk)
    return render(request, 'costos/puntos_recarga_form.html', {'costos_pk': costos_pk, 'puntos_registrados': puntos_registrados})

def registrar_km_inicial(request, costos_pk):
    costos_viaje = get_object_or_404(CostosViaje, pk=costos_pk)
    if request.method == 'POST':
        form = KmInicialForm(request.POST, instance=costos_viaje)
        if form.is_valid():
            form.save()
            return redirect('costos:mantenimiento_costos', costos_pk=costos_pk)
    else:
        form = KmInicialForm(instance=costos_viaje)
    return render(request, 'costos/km_inicial_form.html', {'form': form, 'costos_pk': costos_pk})

def registrar_km_final(request, costos_pk):
    costos_viaje = get_object_or_404(CostosViaje, pk=costos_pk)
    if request.method == 'POST':
        form = KmFinalForm(request.POST, instance=costos_viaje)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kilometraje final registrado correctamente.')
            return redirect('costos:detalle', pk=costos_pk)
    else:
        form = KmFinalForm(instance=costos_viaje)
    return render(request, 'costos/km_final_form.html', {'form': form, 'costos_pk': costos_pk})


def registrar_costos_completo(request, viaje_id):
    """Vista unificada para registrar todos los costos de un viaje en un solo formulario."""
    from decimal import Decimal
    
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    
    # Verificar si ya tiene costos registrados
    if CostosViaje.objects.filter(viaje=viaje).exists():
        messages.warning(request, 'Este viaje ya tiene costos registrados.')
        return redirect('costos:gestion')
    
    if request.method == 'POST':
        form = CostosViajeFormCompleto(request.POST)
        
        if form.is_valid():
            # Crear el registro de costos
            costos_viaje = form.save(commit=False)
            costos_viaje.viaje = viaje
            costos_viaje.save()
            
            # Procesar mantenimientos
            mantenimientos_list = []
            bus = costos_viaje.viaje.bus
            for key in request.POST:
                if key.startswith('nuevo_mant_fecha_'):
                    idx = key.split('_')[-1]
                    fecha = request.POST.get(f'nuevo_mant_fecha_{idx}', '').strip()
                    tipo = request.POST.get(f'nuevo_mant_tipo_{idx}', '').strip()
                    costo = request.POST.get(f'nuevo_mant_costo_{idx}', '').strip()
                    kilometraje = request.POST.get(f'nuevo_mant_kilometraje_{idx}', '').strip()
                    proveedor = request.POST.get(f'nuevo_mant_proveedor_{idx}', '').strip()
                    taller = request.POST.get(f'nuevo_mant_taller_{idx}', '').strip()
                    descripcion = request.POST.get(f'nuevo_mant_descripcion_{idx}', '').strip()
                    observaciones = request.POST.get(f'nuevo_mant_observaciones_{idx}', '').strip()
                    
                    if fecha and tipo and descripcion:
                        try:
                            costo_mant = Decimal(costo) if costo else Decimal('0')
                            km_mant = int(kilometraje) if kilometraje else 0
                            
                            nuevo_mantenimiento = Mantenimiento.objects.create(
                                bus=bus,
                                fecha_mantenimiento=fecha,
                                tipo=tipo,
                                costo=costo_mant,
                                kilometraje=km_mant,
                                proveedor=proveedor if proveedor else None,
                                taller=taller,
                                descripcion=descripcion,
                                observaciones=observaciones
                            )
                            mantenimientos_list.append(nuevo_mantenimiento)
                        except Exception as e:
                            messages.warning(request, f'No se pudo crear el mantenimiento: {str(e)}')
            
            # Asociar todos los mantenimientos al registro de costos
            if mantenimientos_list:
                costos_viaje.mantenimientos.set(mantenimientos_list)
                costos_viaje.mantenimiento = sum(Decimal(str(m.costo)) for m in mantenimientos_list)
            
            # Procesar peajes dinámicos
            total_peajes = Decimal('0')
            for key in request.POST:
                if key.startswith('peaje_lugar_'):
                    idx = key.split('_')[-1]
                    lugar = request.POST.get(f'peaje_lugar_{idx}', '').strip()
                    monto = request.POST.get(f'peaje_monto_{idx}', '').strip()
                    fecha_pago = request.POST.get(f'peaje_fecha_{idx}', '').strip()
                    voucher = request.FILES.get(f'peaje_voucher_{idx}')
                    
                    if lugar and monto:
                        try:
                            monto_decimal = Decimal(monto)
                            
                            # Usar la fecha proporcionada o la actual
                            if fecha_pago:
                                from datetime import datetime as dt
                                fecha = dt.strptime(fecha_pago, '%Y-%m-%d').date()
                            else:
                                fecha = datetime.now().date()
                            
                            peaje = Peaje.objects.create(
                                viaje=costos_viaje.viaje,
                                costos_viaje=costos_viaje,
                                lugar=lugar,
                                monto=monto_decimal,
                                fecha_pago=fecha,
                                comprobante=voucher if voucher else ""
                            )
                            total_peajes += monto_decimal
                        except Exception as e:
                            messages.warning(request, f'No se pudo crear el peaje: {str(e)}')
            
            costos_viaje.peajes = total_peajes
            
            # Procesar puntos de recarga dinámicos
            for key in request.POST:
                if key.startswith('recarga_lugar_'):
                    idx = key.split('_')[-1]
                    orden = request.POST.get(f'recarga_orden_{idx}', '').strip()
                    lugar = request.POST.get(f'recarga_lugar_{idx}', '').strip()
                    sucursal = request.POST.get(f'recarga_sucursal_{idx}', '').strip()
                    kilometraje = request.POST.get(f'recarga_kilometraje_{idx}', '').strip()
                    litros = request.POST.get(f'recarga_litros_{idx}', '').strip()
                    precio = request.POST.get(f'recarga_precio_{idx}', '').strip()
                    fecha_pago = request.POST.get(f'recarga_fecha_{idx}', '').strip()
                    voucher = request.FILES.get(f'recarga_voucher_{idx}')
                    
                    if lugar and kilometraje and litros and precio:
                        try:
                            # Crear ubicación completa
                            ubicacion_completa = lugar
                            if sucursal:
                                ubicacion_completa += f" - {sucursal}"
                            
                            # Crear observaciones con la fecha si existe
                            observaciones = ""
                            if fecha_pago:
                                observaciones = f"Fecha de pago: {fecha_pago}"
                            
                            PuntoRecarga.objects.create(
                                costos_viaje=costos_viaje,
                                orden=int(orden) if orden else int(idx),
                                kilometraje=Decimal(kilometraje),
                                precio_combustible=Decimal(precio),
                                litros_cargados=Decimal(litros),
                                ubicacion=ubicacion_completa,
                                observaciones=observaciones
                            )
                        except Exception as e:
                            messages.warning(request, f'No se pudo crear el punto de recarga: {str(e)}')
            
            # Recalcular el costo total de combustible
            costos_viaje.calcular_costo_combustible()
            
            # Procesar otros costos
            total_otros_costos = Decimal('0')
            observaciones_otros_costos = []
            
            for key in request.POST:
                if key.startswith('otro_costo_tipo_'):
                    idx = key.split('_')[-1]
                    tipo = request.POST.get(f'otro_costo_tipo_{idx}', '').strip()
                    monto = request.POST.get(f'otro_costo_monto_{idx}', '').strip()
                    descripcion = request.POST.get(f'otro_costo_descripcion_{idx}', '').strip()
                    voucher = request.FILES.get(f'otro_costo_voucher_{idx}')
                    
                    if tipo and monto and descripcion:
                        try:
                            monto_decimal = Decimal(monto)
                            total_otros_costos += monto_decimal
                            
                            # Agregar a observaciones
                            obs = f"{tipo.upper()}: {descripcion} - ${monto}"
                            if voucher:
                                obs += f" (Comprobante: {voucher.name})"
                            observaciones_otros_costos.append(obs)
                        except Exception as e:
                            messages.warning(request, f'No se pudo procesar el costo {tipo}: {str(e)}')
            
            # Actualizar otros_costos y observaciones
            costos_viaje.otros_costos = total_otros_costos
            if observaciones_otros_costos:
                obs_actuales = costos_viaje.observaciones or ''
                if obs_actuales:
                    obs_actuales += '\n\n'
                obs_actuales += 'OTROS COSTOS:\n' + '\n'.join(observaciones_otros_costos)
                costos_viaje.observaciones = obs_actuales
            
            costos_viaje.save()
            
            messages.success(request, 'Costos del viaje registrados exitosamente.')
            return redirect('costos:detalle', pk=costos_viaje.pk)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = CostosViajeFormCompleto()
    
    return render(request, 'costos/costos_completo_form.html', {'form': form, 'viaje': viaje})
