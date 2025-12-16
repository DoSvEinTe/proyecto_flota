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
from django.core.mail import EmailMessage
from django.conf import settings
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


class ViajesSinCostosListView(LoginRequiredMixin, ListView):
    """Vista para listar viajes que no tienen costos asignados."""
    model = Viaje
    template_name = 'costos/viajes_sin_costos.html'
    context_object_name = 'viajes'
    paginate_by = 10

    def get_queryset(self):
        viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
        return Viaje.objects.exclude(id__in=viajes_con_costos).select_related('bus', 'conductor')


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
            # Cambiar estado a EN CURSO al iniciar registro de costos
            viaje.estado = 'en_curso'
            viaje.save()
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
        # Cambiar estado del viaje a COMPLETADO al finalizar el registro
        costos_viaje.viaje.estado = 'completado'
        costos_viaje.viaje.save()
        return redirect('costos:detalle', pk=costos_pk)
    return render(request, 'costos/otros_costos_form.html', {'costos_pk': costos_pk})
class CostosViajeDetailView(LoginRequiredMixin, DetailView):
    """Vista para ver detalles de costos de un viaje."""
    model = CostosViaje
    template_name = 'costos/costos_detail.html'
    context_object_name = 'costos'

    def get_context_data(self, **kwargs):
        # Cambiar estado del viaje a COMPLETADO cuando se accede al detalle
        if self.object.viaje.estado != 'completado':
            self.object.viaje.estado = 'completado'
            self.object.viaje.save()
        
        context = super().get_context_data(**kwargs)
        context['puntos_recarga'] = self.object.puntos_recarga.all()
        context['total_kilometros'] = sum(p.kilometros_recorridos for p in context['puntos_recarga'])
        context['total_litros'] = sum(p.litros_cargados for p in context['puntos_recarga'])
        # Calculo real de km recorridos
        if self.object.km_final is not None and self.object.km_inicial is not None:
            context['km_recorridos_real'] = self.object.km_final - self.object.km_inicial
        else:
            context['km_recorridos_real'] = context['total_kilometros']
        
        # Calcular consumo
        if context['total_litros'] > 0 and context['km_recorridos_real'] > 0:
            context['consumo_promedio'] = context['km_recorridos_real'] / context['total_litros']
        else:
            context['consumo_promedio'] = 0
            
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
    success_url = reverse_lazy('costos:gestion')

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
        # Si ya tiene km_final, ir a gestión, si no, pedir km_final
        if costos_viaje.km_final is not None:
            return redirect('costos:gestion')
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
        
        # Agregar un atributo temporal para mostrar "EN CURSO" en la tabla
        for viaje in viajes_sin_costos:
            viaje.estado_display = 'en_curso'

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
        
        # Obtener coordenadas directamente del viaje
        try:
            lat_origen = viaje.latitud_origen
            lon_origen = viaje.longitud_origen
            lat_destino = viaje.latitud_destino
            lon_destino = viaje.longitud_destino
        except Exception as e:
            return JsonResponse({
                'error': f'Error al obtener coordenadas: {str(e)}'
            }, status=400)
        
        # Verificar que el viaje tenga coordenadas
        if not all([lat_origen, lon_origen, lat_destino, lon_destino]):
            return JsonResponse({
                'error': f'Faltan coordenadas. Origen: {viaje.get_origen_display()} (lat: {lat_origen}, lon: {lon_origen}), Destino: {viaje.get_destino_display()} (lat: {lat_destino}, lon: {lon_destino})'
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
    """Genera un PDF con campos editables para que el conductor registre los costos manualmente."""
    from reportlab.pdfgen import canvas as pdf_canvas
    from reportlab.pdfbase import pdfform
    from reportlab.lib.colors import HexColor
    
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    
    # Buffer para el PDF base
    buffer = io.BytesIO()
    
    # Crear el PDF usando canvas
    c = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Colores
    color_azul = HexColor('#1e40af')
    color_gris = HexColor('#f3f4f6')
    
    costos_viaje = CostosViaje.objects.filter(viaje=viaje).first()
    km_inicial = costos_viaje.km_inicial if costos_viaje and costos_viaje.km_inicial is not None else ''
    
    # ================================
    # PÁGINA 1 - INFORMACIÓN Y RECARGAS
    # ================================
    y = height - 50
    
    # Título
    c.setFillColor(color_azul)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y, "FORMULARIO DE REGISTRO DE COSTOS DE VIAJE")
    
    y -= 40
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "INFORMACIÓN DEL VIAJE")
    
    # Información estática
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Bus: {viaje.bus.placa}    Modelo: {viaje.bus.modelo}")
    y -= 18
    c.drawString(50, y, f"Origen: {viaje.get_origen_display()}    Destino: {viaje.get_destino_display()}")
    y -= 18
    c.drawString(50, y, f"Conductor: {viaje.conductor.nombre} {viaje.conductor.apellido}")
    y -= 18
    c.drawString(50, y, f"Fecha: {viaje.fecha_salida.strftime('%d/%m/%Y')}")
    
    # Campos editables para kilometrajes usando acroForm
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Kilometraje Inicial:")
    c.drawString(300, y, "Kilometraje Final:")
    
    form = c.acroForm
    y_campo = y - 18
    
    form.textfield(
        name='km_inicial',
        tooltip='Kilometraje Inicial',
        x=180, y=y_campo, width=100, height=18,
        borderStyle='solid',
        borderWidth=1,
        borderColor=colors.grey,
        fillColor=colors.white,
        textColor=colors.black,
        forceBorder=True,
        value=str(km_inicial) if km_inicial else ''
    )
    
    form.textfield(
        name='km_final',
        tooltip='Kilometraje Final',
        x=430, y=y_campo, width=100, height=18,
        borderStyle='solid',
        borderWidth=1,
        borderColor=colors.grey,
        fillColor=colors.white,
        textColor=colors.black,
        forceBorder=True
    )
    
    # ================================
    # TABLA RECARGAS DE COMBUSTIBLE
    # ================================
    y = y_campo - 30
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(color_azul)
    c.drawString(50, y, "PUNTOS DE RECARGA DE COMBUSTIBLE")
    
    y -= 25
    # Encabezados de tabla
    c.setFillColor(color_azul)
    c.rect(50, y - 18, width - 100, 18, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    headers = ['N°', 'Lugar', 'Sucursal', 'KM', 'Fecha', 'Litros', 'Precio']
    x_pos = [55, 85, 175, 255, 310, 370, 430]
    for i, header in enumerate(headers):
        c.drawString(x_pos[i], y - 12, header)
    
    # Filas de la tabla con campos editables
    y -= 18
    c.setFillColor(colors.black)
    
    for i in range(1, 10):
        y -= 22
        c.setFont("Helvetica", 8)
        c.drawString(58, y + 5, str(i))
        
        # Campos de formulario editables
        form.textfield(name=f'recarga_lugar_{i}', x=80, y=y, width=90, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'recarga_sucursal_{i}', x=172, y=y, width=80, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'recarga_km_{i}', x=254, y=y, width=50, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'recarga_fecha_{i}', x=306, y=y, width=60, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'recarga_litros_{i}', x=368, y=y, width=60, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'recarga_precio_{i}', x=430, y=y, width=60, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
    
    # Nota sobre sucursales
    y -= 25
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.grey)
    c.drawString(50, y, "* Sucursal: COPEC, Shell, Petrobras, ENEX, Terpel, Otro")
    
    # ================================
    # TABLA MANTENIMIENTOS
    # ================================
    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(color_azul)
    c.drawString(50, y, "MANTENIMIENTOS")
    
    y -= 25
    # Encabezados
    c.setFillColor(color_azul)
    c.rect(50, y - 18, width - 100, 18, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7)
    headers_mant = ['N°', 'Fecha', 'Tipo', 'Descripción', 'Costo', 'Proveedor', 'KM', 'Taller']
    x_pos_mant = [55, 80, 130, 180, 290, 340, 420, 455]
    for i, header in enumerate(headers_mant):
        c.drawString(x_pos_mant[i], y - 12, header)
    
    # Filas con campos editables
    y -= 18
    c.setFillColor(colors.black)
    
    for i in range(1, 6):
        y -= 22
        c.setFont("Helvetica", 7)
        c.drawString(58, y + 5, str(i))
        
        form.textfield(name=f'mant_fecha_{i}', x=75, y=y, width=50, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'mant_tipo_{i}', x=127, y=y, width=50, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'mant_desc_{i}', x=179, y=y, width=108, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'mant_costo_{i}', x=289, y=y, width=48, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'mant_prov_{i}', x=339, y=y, width=78, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'mant_km_{i}', x=419, y=y, width=33, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'mant_taller_{i}', x=454, y=y, width=88, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
    
    c.showPage()
    
    # ================================
    # PÁGINA 2 - PEAJES Y OTROS
    # ================================
    y = height - 50
    
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(color_azul)
    c.drawString(50, y, "REGISTRO DE PEAJES")
    
    y -= 30
    # Encabezados
    c.setFillColor(color_azul)
    c.rect(50, y - 18, width - 100, 18, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(60, y - 12, "N°")
    c.drawString(120, y - 12, "Lugar")
    c.drawString(350, y - 12, "Monto (CLP)")
    c.drawString(460, y - 12, "Fecha")
    
    # Filas con campos editables
    y -= 18
    c.setFillColor(colors.black)
    
    for i in range(1, 10):
        y -= 22
        c.setFont("Helvetica", 9)
        c.drawString(63, y + 5, str(i))
        
        form.textfield(name=f'peaje_lugar_{i}', x=90, y=y, width=255, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'peaje_monto_{i}', x=347, y=y, width=110, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'peaje_fecha_{i}', x=459, y=y, width=85, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
    
    # ================================
    # OTROS COSTOS
    # ================================
    y -= 35
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(color_azul)
    c.drawString(50, y, "OTROS COSTOS")
    
    y -= 25
    # Encabezados
    c.setFillColor(color_azul)
    c.rect(50, y - 18, width - 100, 18, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(60, y - 12, "N°")
    c.drawString(120, y - 12, "Tipo de Costo")
    c.drawString(280, y - 12, "Descripción")
    c.drawString(470, y - 12, "Monto")
    
    # Filas con campos editables
    y -= 18
    c.setFillColor(colors.black)
    
    for i in range(1, 6):
        y -= 22
        c.setFont("Helvetica", 9)
        c.drawString(63, y + 5, str(i))
        
        form.textfield(name=f'otro_tipo_{i}', x=90, y=y, width=185, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'otro_desc_{i}', x=277, y=y, width=185, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
        
        form.textfield(name=f'otro_monto_{i}', x=464, y=y, width=80, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, forceBorder=True)
    
    # ================================
    # OBSERVACIONES
    # ================================
    y -= 35
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(color_azul)
    c.drawString(50, y, "OBSERVACIONES GENERALES")
    
    y -= 15
    # Campo de texto para observaciones
    form.textfield(
        name='observaciones',
        tooltip='Observaciones generales del viaje',
        x=50, y=y - 65, width=width - 100, height=70,
        borderStyle='solid',
        borderWidth=1,
        borderColor=colors.grey,
        fillColor=colors.white,
        textColor=colors.black,
        forceBorder=True
    )
    
    # ================================
    # FIRMA
    # ================================
    y -= 95
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(80, y, 250, y)
    c.line(350, y, 520, y)
    
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    c.drawCentredString(165, y - 15, "Firma del Conductor")
    c.drawCentredString(435, y - 15, "Fecha")
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(width/2, 30, 
        f"Formulario generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema FlotaGest")
    c.drawCentredString(width/2, 20, 
        "PDF interactivo - Complete los campos directamente en Adobe Reader, Foxit o cualquier visor PDF")
    
    c.save()
    
    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="formulario_costos_viaje_{viaje.id}.pdf"'
    
    return response


def enviar_formulario_email(request, viaje_id):
    """Envía el formulario PDF de costos por correo electrónico al conductor."""
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    conductor = viaje.conductor
    
    if not conductor.email:
        messages.error(request, f'El conductor {conductor.nombre} {conductor.apellido} no tiene un correo electrónico registrado.')
        return redirect('costos:gestion')
    
    try:
        # Generar el PDF en memoria usando el mismo código que generar_formulario_costos_pdf
        from reportlab.pdfgen import canvas as pdf_canvas
        from reportlab.pdfbase import pdfform
        from reportlab.lib.colors import HexColor
        
        buffer = io.BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        color_azul = HexColor('#1e40af')
        color_gris = HexColor('#f3f4f6')
        
        costos_viaje = CostosViaje.objects.filter(viaje=viaje).first()
        km_inicial = costos_viaje.km_inicial if costos_viaje and costos_viaje.km_inicial is not None else ''
        
        # PÁGINA 1
        y = height - 50
        c.setFillColor(color_azul)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, y, "FORMULARIO DE REGISTRO DE COSTOS DE VIAJE")
        
        y -= 40
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "INFORMACIÓN DEL VIAJE")
        
        y -= 25
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Bus: {viaje.bus.placa}    Modelo: {viaje.bus.modelo}")
        y -= 18
        c.drawString(50, y, f"Origen: {viaje.get_origen_display()}    Destino: {viaje.get_destino_display()}")
        y -= 18
        c.drawString(50, y, f"Conductor: {viaje.conductor.nombre} {viaje.conductor.apellido}")
        y -= 18
        c.drawString(50, y, f"Fecha: {viaje.fecha_salida.strftime('%d/%m/%Y')}")
        
        y -= 25
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Kilometraje Inicial:")
        c.drawString(300, y, "Kilometraje Final:")
        
        form = c.acroForm
        y_campo = y - 18
        
        form.textfield(name='km_inicial', tooltip='Kilometraje Inicial', x=180, y=y_campo, width=100, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white,
                      textColor=colors.black, forceBorder=True, value=str(km_inicial) if km_inicial else '')
        
        form.textfield(name='km_final', tooltip='Kilometraje Final', x=430, y=y_campo, width=100, height=18,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white,
                      textColor=colors.black, forceBorder=True)
        
        # TABLA RECARGAS
        y = y_campo - 30
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(color_azul)
        c.drawString(50, y, "PUNTOS DE RECARGA DE COMBUSTIBLE")
        
        y -= 25
        c.setFillColor(color_azul)
        c.rect(50, y - 18, width - 100, 18, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        headers = ['N°', 'Lugar', 'Sucursal', 'KM', 'Fecha', 'Litros', 'Precio']
        x_pos = [55, 85, 175, 255, 310, 370, 430]
        for i, header in enumerate(headers):
            c.drawString(x_pos[i], y - 12, header)
        
        y -= 18
        c.setFillColor(colors.black)
        
        for i in range(1, 10):
            y -= 22
            c.setFont("Helvetica", 8)
            c.drawString(58, y + 5, str(i))
            form.textfield(name=f'recarga_lugar_{i}', x=80, y=y, width=90, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'recarga_sucursal_{i}', x=172, y=y, width=80, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'recarga_km_{i}', x=254, y=y, width=50, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'recarga_fecha_{i}', x=306, y=y, width=60, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'recarga_litros_{i}', x=368, y=y, width=60, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'recarga_precio_{i}', x=430, y=y, width=60, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
        
        y -= 25
        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(colors.grey)
        c.drawString(50, y, "* Sucursal: COPEC, Shell, Petrobras, ENEX, Terpel, Otro")
        
        # TABLA MANTENIMIENTOS
        y -= 25
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(color_azul)
        c.drawString(50, y, "MANTENIMIENTOS")
        
        y -= 25
        c.setFillColor(color_azul)
        c.rect(50, y - 18, width - 100, 18, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 7)
        headers_mant = ['N°', 'Fecha', 'Tipo', 'Descripción', 'Costo', 'Proveedor', 'KM', 'Taller']
        x_pos_mant = [55, 80, 130, 180, 290, 340, 420, 455]
        for i, header in enumerate(headers_mant):
            c.drawString(x_pos_mant[i], y - 12, header)
        
        y -= 18
        c.setFillColor(colors.black)
        
        for i in range(1, 6):
            y -= 22
            c.setFont("Helvetica", 7)
            c.drawString(58, y + 5, str(i))
            form.textfield(name=f'mant_fecha_{i}', x=75, y=y, width=50, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'mant_tipo_{i}', x=127, y=y, width=50, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'mant_desc_{i}', x=179, y=y, width=108, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'mant_costo_{i}', x=289, y=y, width=48, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'mant_prov_{i}', x=339, y=y, width=78, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'mant_km_{i}', x=419, y=y, width=33, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'mant_taller_{i}', x=454, y=y, width=88, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
        
        c.showPage()
        
        # PÁGINA 2
        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(color_azul)
        c.drawString(50, y, "REGISTRO DE PEAJES")
        
        y -= 30
        c.setFillColor(color_azul)
        c.rect(50, y - 18, width - 100, 18, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(60, y - 12, "N°")
        c.drawString(120, y - 12, "Lugar")
        c.drawString(350, y - 12, "Monto (CLP)")
        c.drawString(460, y - 12, "Fecha")
        
        y -= 18
        c.setFillColor(colors.black)
        
        for i in range(1, 10):
            y -= 22
            c.setFont("Helvetica", 9)
            c.drawString(63, y + 5, str(i))
            form.textfield(name=f'peaje_lugar_{i}', x=90, y=y, width=255, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'peaje_monto_{i}', x=347, y=y, width=110, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'peaje_fecha_{i}', x=459, y=y, width=85, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
        
        # OTROS COSTOS
        y -= 35
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(color_azul)
        c.drawString(50, y, "OTROS COSTOS")
        
        y -= 25
        c.setFillColor(color_azul)
        c.rect(50, y - 18, width - 100, 18, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(60, y - 12, "N°")
        c.drawString(120, y - 12, "Tipo de Costo")
        c.drawString(280, y - 12, "Descripción")
        c.drawString(470, y - 12, "Monto")
        
        y -= 18
        c.setFillColor(colors.black)
        
        for i in range(1, 6):
            y -= 22
            c.setFont("Helvetica", 9)
            c.drawString(63, y + 5, str(i))
            form.textfield(name=f'otro_tipo_{i}', x=90, y=y, width=185, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'otro_desc_{i}', x=277, y=y, width=185, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
            form.textfield(name=f'otro_monto_{i}', x=464, y=y, width=80, height=18,
                          borderStyle='solid', borderWidth=1, borderColor=colors.grey, fillColor=colors.white, forceBorder=True)
        
        # OBSERVACIONES
        y -= 35
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(color_azul)
        c.drawString(50, y, "OBSERVACIONES GENERALES")
        
        y -= 15
        form.textfield(name='observaciones', tooltip='Observaciones generales del viaje',
                      x=50, y=y - 65, width=width - 100, height=70,
                      borderStyle='solid', borderWidth=1, borderColor=colors.grey,
                      fillColor=colors.white, textColor=colors.black, forceBorder=True)
        
        # FIRMA
        y -= 95
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.line(80, y, 250, y)
        c.line(350, y, 520, y)
        
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawCentredString(165, y - 15, "Firma del Conductor")
        c.drawCentredString(435, y - 15, "Fecha")
        
        # Footer
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(HexColor('#dc2626'))
        c.drawCentredString(width/2, 40, "📱 IMPORTANTE: Para editar en celulares necesitas Adobe Acrobat Reader, Xodo PDF o Foxit PDF")
        
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(colors.grey)
        c.drawCentredString(width/2, 27, f"Formulario generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} - Sistema FlotaGest")
        c.drawCentredString(width/2, 17, "Android: Descarga desde Play Store | iOS: Descarga desde App Store")
        
        c.save()
        buffer.seek(0)
        
        # Crear el email
        subject = f'Formulario de Costos - Viaje {viaje.bus.placa} ({viaje.fecha_salida.strftime("%d/%m/%Y")})'
        body = f"""Estimado/a {conductor.nombre} {conductor.apellido},

Por medio de la presente, adjunto encontrará el formulario para el registro de los costos correspondientes al viaje asignado.

DETALLES DEL VIAJE:
- Bus: {viaje.bus.placa} - {viaje.bus.modelo}
- Ruta: {viaje.get_origen_display()} a {viaje.get_destino_display()}
- Fecha de salida: {viaje.fecha_salida.strftime('%d/%m/%Y %H:%M')}
- Estado: {viaje.get_estado_display()}

INSTRUCCIONES PARA COMPLETAR EL FORMULARIO:

Para editar el formulario PDF en dispositivos móviles (celulares o tablets), es necesario contar con una aplicación compatible. Las aplicaciones recomendadas son:

- Adobe Acrobat Reader
- Xodo PDF (recomendado para Android)
- Foxit PDF

Puede descargar estas aplicaciones desde:
- Android: Google Play Store
- iOS: Apple App Store

Por favor, complete el formulario con todos los costos del viaje y envíelo de vuelta a la brevedad posible.

Quedamos atentos a cualquier consulta.

Cordialmente,
Sistema de Gestión de Flota - FlotaGest"""
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[conductor.email],
        )
        
        # Adjuntar el PDF
        filename = f'formulario_costos_viaje_{viaje.id}.pdf'
        email.attach(filename, buffer.getvalue(), 'application/pdf')
        
        # Enviar el email
        email.send()
        
        messages.success(request, f'✅ Formulario enviado exitosamente a {conductor.email}')
        
    except Exception as e:
        messages.error(request, f'❌ Error al enviar el correo: {str(e)}')
    
    return redirect('costos:gestion')


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
            return redirect('costos:gestion')
    else:
        form = KmFinalForm(instance=costos_viaje)
    return render(request, 'costos/km_final_form.html', {'form': form, 'costos_pk': costos_pk})


def registrar_costos_completo(request, viaje_id):
    """Vista unificada para registrar/editar todos los costos de un viaje en un solo formulario."""
    from decimal import Decimal
    
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    
    # Verificar si ya tiene costos registrados (modo edición)
    costos_existentes = CostosViaje.objects.filter(viaje=viaje).first()
    es_edicion = costos_existentes is not None
    
    if request.method == 'POST':
        if es_edicion:
            form = CostosViajeFormCompleto(request.POST, instance=costos_existentes)
        else:
            form = CostosViajeFormCompleto(request.POST)
        
        if form.is_valid():
            # Crear o actualizar el registro de costos
            costos_viaje = form.save(commit=False)
            if not es_edicion:
                costos_viaje.viaje = viaje
            costos_viaje.save()
            
            # Si es edición, eliminar registros antiguos antes de crear nuevos
            if es_edicion:
                costos_viaje.puntos_recarga.all().delete()
                costos_viaje.viaje.peajes.filter(costos_viaje=costos_viaje).delete()
                costos_viaje.mantenimientos.clear()
            
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
                                observaciones=observaciones,
                                comprobante=voucher if voucher else ""
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
                            # Limpiar el monto de caracteres no numéricos excepto punto y coma
                            monto_limpio = monto.replace(',', '').replace('$', '').replace(' ', '')
                            monto_decimal = Decimal(monto_limpio)
                            total_otros_costos += monto_decimal
                            
                            # Agregar a observaciones
                            obs = f"{tipo.upper()}: {descripcion} - ${monto_decimal}"
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
            
            if es_edicion:
                messages.success(request, 'Costos del viaje actualizados exitosamente.')
            else:
                messages.success(request, 'Costos del viaje registrados exitosamente.')
            return redirect('costos:gestion')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        if es_edicion:
            form = CostosViajeFormCompleto(instance=costos_existentes)
        else:
            form = CostosViajeFormCompleto()
    
    # Obtener datos existentes para prellenar formularios dinámicos
    puntos_recarga_existentes = []
    peajes_existentes = []
    mantenimientos_existentes = []
    otros_costos_existentes = []
    
    if es_edicion:
        puntos_recarga_existentes = list(costos_existentes.puntos_recarga.all().values(
            'id', 'orden', 'ubicacion', 'kilometraje', 'litros_cargados', 
            'precio_combustible', 'observaciones'
        ))
        # Formatear números para mostrar sin decimales innecesarios y extraer fecha
        for punto in puntos_recarga_existentes:
            if punto['kilometraje']:
                km = float(punto['kilometraje'])
                punto['kilometraje'] = int(km) if km == int(km) else km
            if punto['litros_cargados']:
                litros = float(punto['litros_cargados'])
                punto['litros_cargados'] = int(litros) if litros == int(litros) else litros
            if punto['precio_combustible']:
                precio = float(punto['precio_combustible'])
                punto['precio_combustible'] = int(precio) if precio == int(precio) else precio
            
            # Extraer fecha de las observaciones
            punto['fecha_pago'] = ''
            if punto['observaciones'] and 'Fecha de pago:' in punto['observaciones']:
                import re
                match = re.search(r'Fecha de pago:\s*(\d{4}-\d{2}-\d{2})', punto['observaciones'])
                if match:
                    punto['fecha_pago'] = match.group(1)
            if punto['precio_combustible']:
                precio = float(punto['precio_combustible'])
                punto['precio_combustible'] = int(precio) if precio == int(precio) else precio
            
        peajes_existentes = list(costos_existentes.viaje.peajes.all().values(
            'id', 'lugar', 'monto', 'fecha_pago', 'comprobante'
        ))
        # Formatear monto de peajes
        for peaje in peajes_existentes:
            if peaje['monto']:
                monto = float(peaje['monto'])
                peaje['monto'] = int(monto) if monto == int(monto) else monto
            
        mantenimientos_existentes = list(costos_existentes.mantenimientos.all().values(
            'id', 'fecha_mantenimiento', 'tipo', 'descripcion', 'costo', 
            'kilometraje', 'proveedor', 'taller', 'observaciones'
        ))
        
        # Parsear otros costos desde observaciones
        observaciones_limpias = ""
        if costos_existentes.observaciones and 'OTROS COSTOS:' in costos_existentes.observaciones:
            lineas = costos_existentes.observaciones.split('\n')
            capturando = False
            lineas_sin_otros_costos = []
            
            for linea in lineas:
                if 'OTROS COSTOS:' in linea:
                    capturando = True
                    continue
                if capturando and linea.strip():
                    # Formato: TIPO: Descripción - $Monto
                    if ':' in linea and '-' in linea and '$' in linea:
                        try:
                            partes = linea.split(':', 1)
                            tipo = partes[0].strip()
                            resto = partes[1].split('-')
                            descripcion = resto[0].strip()
                            monto_str = resto[1].strip().replace('$', '').replace(',', '')
                            monto = float(monto_str)
                            otros_costos_existentes.append({
                                'tipo': tipo,
                                'descripcion': descripcion,
                                'monto': monto
                            })
                        except:
                            pass
                else:
                    if not capturando:
                        lineas_sin_otros_costos.append(linea)
            
            observaciones_limpias = '\n'.join(lineas_sin_otros_costos).strip()
        else:
            observaciones_limpias = costos_existentes.observaciones if costos_existentes.observaciones else ""
        
        # Actualizar el form con observaciones limpias
        if es_edicion:
            form.initial['observaciones'] = observaciones_limpias
    
    context = {
        'form': form, 
        'viaje': viaje,
        'es_edicion': es_edicion,
        'puntos_recarga_existentes': puntos_recarga_existentes,
        'peajes_existentes': peajes_existentes,
        'mantenimientos_existentes': mantenimientos_existentes,
        'otros_costos_existentes': otros_costos_existentes,
    }
    
    return render(request, 'costos/costos_completo_form.html', context)
