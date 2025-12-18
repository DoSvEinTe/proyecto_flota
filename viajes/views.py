from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.db.models import Q
from django.template.loader import get_template
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfgen import canvas
from .models import Viaje, ViajePasajero
from core.models import Conductor, Lugar, Pasajero
from core.views import PasajeroForm
from flota.models import Bus
from core.permissions import admin_required, usuario_or_admin_required
from core.access_control import check_object_access, validate_viaje_access


class ViajeForm(ModelForm):
    class Meta:
        model = Viaje
        fields = [
            'bus', 'conductor',
            'origen_nombre', 'origen_ciudad', 'origen_provincia', 'origen_pais',
            'latitud_origen', 'longitud_origen',
            'destino_nombre', 'destino_ciudad', 'destino_provincia', 'destino_pais',
            'latitud_destino', 'longitud_destino',
            'fecha_salida', 'fecha_llegada_estimada',
            'es_ida_vuelta',
            'observaciones'
        ]
        widgets = {
            'bus': forms.Select(attrs={'class': 'form-control'}),
            'conductor': forms.Select(attrs={'class': 'form-control'}),
            
            # Campos de origen
            'origen_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del lugar de origen',
                'id': 'id_origen_nombre'
            }),
            'origen_ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad de origen',
                'id': 'id_origen_ciudad'
            }),
            'origen_provincia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Provincia (opcional)',
                'id': 'id_origen_provincia'
            }),
            'origen_pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'País',
                'id': 'id_origen_pais'
            }),
            'latitud_origen': forms.HiddenInput(attrs={'id': 'id_latitud_origen'}),
            'longitud_origen': forms.HiddenInput(attrs={'id': 'id_longitud_origen'}),
            
            # Campos de destino
            'destino_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del lugar de destino',
                'id': 'id_destino_nombre'
            }),
            'destino_ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad de destino',
                'id': 'id_destino_ciudad'
            }),
            'destino_provincia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Provincia (opcional)',
                'id': 'id_destino_provincia'
            }),
            'destino_pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'País',
                'id': 'id_destino_pais'
            }),
            'latitud_destino': forms.HiddenInput(attrs={'id': 'id_latitud_destino'}),
            'longitud_destino': forms.HiddenInput(attrs={'id': 'id_longitud_destino'}),
            
            'fecha_salida': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora de salida'
            }, format='%Y-%m-%dT%H:%M'),
            'fecha_llegada_estimada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora estimada de llegada'
            }, format='%Y-%m-%dT%H:%M'),
            'es_ida_vuelta': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_es_ida_vuelta'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.utils import timezone
        from datetime import timedelta
        
        # Obtener la fecha y hora actual mínima
        ahora = timezone.now()
        ahora_iso = ahora.strftime('%Y-%m-%dT%H:%M')
        
        # Filtrar solo buses activos
        from core.models import Conductor
        from flota.models import Bus
        self.fields['bus'].queryset = Bus.objects.filter(estado='activo')
        self.fields['bus'].label = 'Bus (Solo activos)'
        self.fields['bus'].help_text = 'Solo se muestran los buses en estado activo'
        
        # Filtrar solo conductores activos
        self.fields['conductor'].queryset = Conductor.objects.filter(activo=True)
        self.fields['conductor'].label = 'Conductor (Solo activos)'
        self.fields['conductor'].help_text = 'Solo se muestran los conductores en estado activo'
        
        # Establecer fecha mínima para fecha de salida (no puede ser en el pasado)
        self.fields['fecha_salida'].widget.attrs['min'] = ahora_iso
        
        # Si estamos editando un viaje existente, establecer min de fecha_llegada basado en fecha_salida
        if self.instance.pk and self.instance.fecha_salida:
            fecha_salida = self.instance.fecha_salida
            # La fecha de llegada mínima es la de salida + 1 minuto
            fecha_llegada_min = (fecha_salida + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M')
            self.fields['fecha_llegada_estimada'].widget.attrs['min'] = fecha_llegada_min
        else:
            # En CREATE, la fecha de llegada mínima es ahora + 1 minuto
            fecha_llegada_min = (ahora + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M')
            self.fields['fecha_llegada_estimada'].widget.attrs['min'] = fecha_llegada_min
    
    def clean(self):
        cleaned_data = super().clean()
        from django.utils import timezone
        
        # Validar fechas de salida y llegada
        fecha_salida = cleaned_data.get('fecha_salida')
        fecha_llegada_estimada = cleaned_data.get('fecha_llegada_estimada')
        
        # Validar que la fecha de salida no sea en el pasado
        if fecha_salida:
            ahora = timezone.now()
            if fecha_salida < ahora:
                raise forms.ValidationError({
                    'fecha_salida': 'La fecha y hora de salida no puede ser anterior al día y hora actual.'
                })
        
        # Validar que la fecha de llegada sea posterior a la de salida
        if fecha_salida and fecha_llegada_estimada:
            if fecha_llegada_estimada <= fecha_salida:
                raise forms.ValidationError({
                    'fecha_llegada_estimada': 'La fecha y hora de llegada debe ser posterior a la fecha y hora de salida.'
                })
        
        # Validar que se hayan proporcionado coordenadas de origen
        if not cleaned_data.get('latitud_origen') or not cleaned_data.get('longitud_origen'):
            raise forms.ValidationError('Debe seleccionar un punto de origen en el mapa.')
        
        # Validar que se hayan proporcionado coordenadas de destino
        if not cleaned_data.get('latitud_destino') or not cleaned_data.get('longitud_destino'):
            raise forms.ValidationError('Debe seleccionar un punto de destino en el mapa.')
        
        # Validar campos de origen
        if not cleaned_data.get('origen_nombre'):
            raise forms.ValidationError('Debe especificar el nombre del lugar de origen.')
        if not cleaned_data.get('origen_ciudad'):
            raise forms.ValidationError('Debe especificar la ciudad de origen.')
        
        # Validar campos de destino
        if not cleaned_data.get('destino_nombre'):
            raise forms.ValidationError('Debe especificar el nombre del lugar de destino.')
        if not cleaned_data.get('destino_ciudad'):
            raise forms.ValidationError('Debe especificar la ciudad de destino.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Calcular distancia después de guardar
            if instance.latitud_origen and instance.longitud_origen and instance.latitud_destino and instance.longitud_destino:
                instance.calcular_distancia_real()
        return instance


# Vistas para Viajes
@method_decorator(usuario_or_admin_required, name='dispatch')
class ViajeListView(ListView):
    model = Viaje
    template_name = 'viajes/viaje_list.html'
    context_object_name = 'viajes'
    paginate_by = 10

    def get_queryset(self):
        from django.db.models import Q
        # Excluir viajes de tipo 'vuelta' ya que se mostrarán anidados en el viaje de IDA
        queryset = Viaje.objects.exclude(tipo_trayecto='vuelta').select_related('bus', 'conductor', 'viaje_relacionado')
        
        # Búsqueda
        search = self.request.GET.get('search', '')
        if search:
            # Si buscan por ID (ej: "VJ-56" o solo "56")
            search_clean = search.replace('VJ-', '').replace('vj-', '').strip()
            q_filter = Q(
                bus__placa__icontains=search
            ) | Q(
                conductor__nombre__icontains=search
            ) | Q(
                conductor__apellido__icontains=search
            ) | Q(
                origen_ciudad__icontains=search
            ) | Q(
                destino_ciudad__icontains=search
            ) | Q(
                origen_nombre__icontains=search
            ) | Q(
                destino_nombre__icontains=search
            )
            
            # Agregar búsqueda por ID si es un número
            if search_clean.isdigit():
                q_filter |= Q(pk=int(search_clean))
            
            queryset = queryset.filter(q_filter)
        
        # Filtros
        estado = self.request.GET.get('estado', '')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        bus = self.request.GET.get('bus', '')
        if bus:
            queryset = queryset.filter(bus_id=bus)
        
        conductor = self.request.GET.get('conductor', '')
        if conductor:
            queryset = queryset.filter(conductor_id=conductor)
        
        es_ida_vuelta = self.request.GET.get('es_ida_vuelta', '')
        if es_ida_vuelta == 'si':
            queryset = queryset.filter(es_ida_vuelta=True)
        elif es_ida_vuelta == 'no':
            queryset = queryset.filter(es_ida_vuelta=False)
        
        fecha_desde = self.request.GET.get('fecha_desde', '')
        if fecha_desde:
            queryset = queryset.filter(fecha_salida__date__gte=fecha_desde)
        
        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        if fecha_hasta:
            queryset = queryset.filter(fecha_salida__date__lte=fecha_hasta)
        
        # Ordenamiento
        orden = self.request.GET.get('orden', '-fecha_salida')
        queryset = queryset.order_by(orden)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Mantener parámetros de búsqueda y filtros en el contexto
        context['search'] = self.request.GET.get('search', '')
        context['estado'] = self.request.GET.get('estado', '')
        context['bus'] = self.request.GET.get('bus', '')
        context['conductor'] = self.request.GET.get('conductor', '')
        context['es_ida_vuelta'] = self.request.GET.get('es_ida_vuelta', '')
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        context['orden'] = self.request.GET.get('orden', '-fecha_salida')
        
        # Listas para los filtros
        context['buses_disponibles'] = Bus.objects.filter(estado='activo').order_by('placa')
        context['conductores_disponibles'] = Conductor.objects.filter(activo=True).order_by('apellido', 'nombre')
        
        return context


@method_decorator(usuario_or_admin_required, name='dispatch')
class ViajeDetailView(DetailView):
    model = Viaje
    template_name = 'viajes/viaje_detail.html'
    context_object_name = 'viaje'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        validate_viaje_access(self.request.user, obj)
        return obj


@method_decorator(usuario_or_admin_required, name='dispatch')
class ViajeCreateView(CreateView):
    model = Viaje
    form_class = ViajeForm
    template_name = 'viajes/viaje_form.html'
    success_url = reverse_lazy('viajes:viaje_list')

    def form_valid(self, form):
        from django.db import transaction
        
        # Establecer automáticamente el estado como PROGRAMADO
        form.instance.estado = 'programado'
        
        # Si es ida y vuelta, marcar como IDA y crear viaje de VUELTA
        if form.instance.es_ida_vuelta:
            with transaction.atomic():
                # Guardar el viaje de IDA
                form.instance.tipo_trayecto = 'ida'
                response = super().form_valid(form)
                viaje_ida = form.instance
                
                # Crear el viaje de VUELTA
                viaje_vuelta = Viaje.objects.create(
                    bus=viaje_ida.bus,
                    conductor=viaje_ida.conductor,
                    # Invertir origen y destino
                    origen_nombre=viaje_ida.destino_nombre,
                    origen_ciudad=viaje_ida.destino_ciudad,
                    origen_provincia=viaje_ida.destino_provincia,
                    origen_pais=viaje_ida.destino_pais,
                    latitud_origen=viaje_ida.latitud_destino,
                    longitud_origen=viaje_ida.longitud_destino,
                    destino_nombre=viaje_ida.origen_nombre,
                    destino_ciudad=viaje_ida.origen_ciudad,
                    destino_provincia=viaje_ida.origen_provincia,
                    destino_pais=viaje_ida.origen_pais,
                    latitud_destino=viaje_ida.latitud_origen,
                    longitud_destino=viaje_ida.longitud_origen,
                    # Fechas: el viaje de vuelta sale después de la llegada estimada del viaje de ida
                    fecha_salida=viaje_ida.fecha_llegada_estimada,
                    fecha_llegada_estimada=viaje_ida.fecha_llegada_estimada + (viaje_ida.fecha_llegada_estimada - viaje_ida.fecha_salida),
                    distancia_km=viaje_ida.distancia_km,
                    estado='programado',
                    es_ida_vuelta=True,
                    tipo_trayecto='vuelta',
                    viaje_relacionado=viaje_ida,
                    observaciones=f'Viaje de vuelta de: {viaje_ida.origen_ciudad} → {viaje_ida.destino_ciudad}'
                )
                
                # Vincular el viaje de ida con el de vuelta
                viaje_ida.viaje_relacionado = viaje_vuelta
                viaje_ida.save(update_fields=['viaje_relacionado'])
                
                messages.success(
                    self.request,
                    f'Viaje de ida y vuelta creado exitosamente: {viaje_ida.origen_ciudad} ↔ {viaje_ida.destino_ciudad}'
                )
                return response
        else:
            form.instance.tipo_trayecto = 'simple'
            messages.success(
                self.request,
                f'Viaje {form.instance.bus.placa} creado exitosamente.'
            )
            return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class ViajeUpdateView(UpdateView):
    model = Viaje
    form_class = ViajeForm
    template_name = 'viajes/viaje_form.html'
    success_url = reverse_lazy('viajes:viaje_list')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        validate_viaje_access(self.request.user, obj)
        return obj

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Viaje {form.instance.bus.placa} actualizado exitosamente.'
        )
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class ViajeDeleteView(DeleteView):
    model = Viaje
    template_name = 'viajes/viaje_confirm_delete.html'
    success_url = reverse_lazy('viajes:viaje_list')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        validate_viaje_access(self.request.user, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(
            request,
            f'Viaje {self.object.bus.placa} eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)


# Vistas para manejar pasajeros en viajes
@login_required(login_url='login')
def viaje_pasajeros_view(request, pk):
    """
    Vista para mostrar y manejar pasajeros de un viaje específico.
    """
    from django.db.models import Q
    viaje = get_object_or_404(Viaje, pk=pk)
    pasajeros_en_viaje = ViajePasajero.objects.filter(viaje=viaje).select_related('pasajero')
    
    # Búsqueda
    search = request.GET.get('search', '')
    if search:
        pasajeros_en_viaje = pasajeros_en_viaje.filter(
            Q(pasajero__nombre_completo__icontains=search) |
            Q(pasajero__rut__icontains=search) |
            Q(pasajero__pasaporte__icontains=search) |
            Q(pasajero__telefono__icontains=search) |
            Q(pasajero__correo__icontains=search) |
            Q(asiento__icontains=search)
        )
    
    # Ordenamiento
    orden = request.GET.get('orden', '-fecha_registro')
    pasajeros_en_viaje = pasajeros_en_viaje.order_by(orden)
    
    # Formulario para crear nuevo pasajero
    pasajero_form = PasajeroForm()
    
    context = {
        'viaje': viaje,
        'pasajeros_en_viaje': pasajeros_en_viaje,
        'pasajero_form': pasajero_form,
        'search': search,
        'orden': orden,
    }
    return render(request, 'viajes/viaje_pasajeros.html', context)


@login_required(login_url='login')
def agregar_pasajero_viaje(request, pk):
    """
    Vista para agregar un pasajero a un viaje.
    """
    if request.method == 'POST':
        viaje = get_object_or_404(Viaje, pk=pk)
        pasajero_id = request.POST.get('pasajero_id')
        asiento = request.POST.get('asiento')
        observaciones = request.POST.get('observaciones', '')
        
        try:
            pasajero = get_object_or_404(Pasajero, pk=pasajero_id)
            
            # Verificar si el pasajero ya está en el viaje
            if ViajePasajero.objects.filter(viaje=viaje, pasajero=pasajero).exists():
                messages.error(request, f'El pasajero {pasajero.nombre_completo} ya está registrado en este viaje.')
            else:
                # Verificar capacidad del bus
                if viaje.get_pasajeros_count() >= viaje.bus.capacidad_pasajeros:
                    messages.error(request, 'El bus ha alcanzado su capacidad máxima de pasajeros.')
                else:
                    ViajePasajero.objects.create(
                        viaje=viaje,
                        pasajero=pasajero,
                        asiento=asiento,
                        observaciones=observaciones
                    )
                    
                    # Actualizar el contador de pasajeros confirmados
                    viaje.pasajeros_confirmados = viaje.get_pasajeros_count()
                    viaje.save()
                    
                    messages.success(request, f'Pasajero {pasajero.nombre_completo} agregado al viaje exitosamente.')
                    
        except Pasajero.DoesNotExist:
            messages.error(request, 'Pasajero no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al agregar pasajero: {str(e)}')
    
    return redirect('viajes:viaje_pasajeros', pk=pk)


@login_required(login_url='login')
def quitar_pasajero_viaje(request, pk, pasajero_pk):
    """
    Vista para quitar un pasajero de un viaje.
    """
    if request.method == 'POST':
        viaje = get_object_or_404(Viaje, pk=pk)
        pasajero = get_object_or_404(Pasajero, pk=pasajero_pk)
        
        try:
            viaje_pasajero = ViajePasajero.objects.get(viaje=viaje, pasajero=pasajero)
            viaje_pasajero.delete()
            
            # Actualizar el contador de pasajeros confirmados
            viaje.pasajeros_confirmados = viaje.get_pasajeros_count()
            viaje.save()
            
            messages.success(request, f'Pasajero {pasajero.nombre_completo} removido del viaje exitosamente.')
            
        except ViajePasajero.DoesNotExist:
            messages.error(request, 'El pasajero no está registrado en este viaje.')
        except Exception as e:
            messages.error(request, f'Error al remover pasajero: {str(e)}')
    
    return redirect('viajes:viaje_pasajeros', pk=pk)


@login_required(login_url='login')
def editar_pasajero_viaje(request, pk, pasajero_pk):
    """
    Vista para editar información completa de un pasajero en un viaje.
    """
    viaje = get_object_or_404(Viaje, pk=pk)
    pasajero = get_object_or_404(Pasajero, pk=pasajero_pk)
    viaje_pasajero = get_object_or_404(ViajePasajero, viaje=viaje, pasajero=pasajero)
    
    if request.method == 'POST':
        # Actualizar información del pasajero
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        rut = request.POST.get('rut', '').strip() or None
        pasaporte_num = request.POST.get('pasaporte', '').strip() or None
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip()
        
        # Actualizar información del viaje-pasajero
        asiento = request.POST.get('asiento', '').strip()
        observaciones = request.POST.get('observaciones', '').strip()
        
        try:
            # Validar que haya al menos nombre, teléfono y correo
            if not nombre_completo or not telefono or not correo:
                messages.error(request, 'El nombre completo, teléfono y correo son obligatorios.')
                return redirect('viajes:editar_pasajero_viaje', pk=pk, pasajero_pk=pasajero_pk)
            
            # Verificar si el documento cambió y si el nuevo documento ya existe en este viaje
            documento_cambio = (rut != pasajero.rut) or (pasaporte_num != pasajero.pasaporte)
            
            if documento_cambio:
                # Buscar si el nuevo documento ya existe en este viaje (excluyendo el pasajero actual)
                documento_existente = ViajePasajero.objects.filter(
                    viaje=viaje
                ).exclude(
                    pasajero=pasajero
                ).filter(
                    Q(pasajero__rut=rut) | Q(pasajero__pasaporte=pasaporte_num)
                ).exists()
                
                if documento_existente:
                    messages.error(request, 'Este documento (RUT/Pasaporte) ya está registrado en otro pasajero de este viaje.')
                    return redirect('viajes:editar_pasajero_viaje', pk=pk, pasajero_pk=pasajero_pk)
            
            # Validar que el asiento no esté ocupado por otro pasajero (si se proporciona asiento)
            if asiento:
                asiento_duplicado = ViajePasajero.objects.filter(
                    viaje=viaje,
                    asiento=asiento
                ).exclude(
                    pasajero=pasajero
                ).exists()
                
                if asiento_duplicado:
                    messages.error(request, f'El asiento {asiento} ya está ocupado por otro pasajero en este viaje.')
                    return redirect('viajes:editar_pasajero_viaje', pk=pk, pasajero_pk=pasajero_pk)
            
            # Actualizar datos del pasajero
            pasajero.nombre_completo = nombre_completo
            pasajero.rut = rut
            pasajero.pasaporte = pasaporte_num
            pasajero.telefono = telefono
            pasajero.correo = correo
            pasajero.save()
            
            # Actualizar datos del viaje-pasajero
            viaje_pasajero.asiento = asiento if asiento else None
            viaje_pasajero.observaciones = observaciones
            viaje_pasajero.save()
            
            messages.success(request, f'Información del pasajero {pasajero.nombre_completo} actualizada exitosamente.')
            return redirect('viajes:viaje_pasajeros', pk=pk)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el pasajero: {str(e)}')
            return redirect('viajes:editar_pasajero_viaje', pk=pk, pasajero_pk=pasajero_pk)
    
    context = {
        'viaje': viaje,
        'pasajero': pasajero,
        'viaje_pasajero': viaje_pasajero,
    }
    return render(request, 'viajes/editar_pasajero_viaje.html', context)


@login_required(login_url='login')
@usuario_or_admin_required
def crear_pasajero_desde_viaje(request, pk):
    """
    Vista para crear un nuevo pasajero desde el contexto de un viaje.
    Después de crear el pasajero, lo agrega automáticamente al viaje y redirige de vuelta a la vista de pasajeros del viaje.
    """
    viaje = get_object_or_404(Viaje, pk=pk)
    
    if request.method == 'POST':
        # Validar que el RUT/Pasaporte no esté ya en este viaje
        rut = request.POST.get('rut', '').strip() or None
        pasaporte = request.POST.get('pasaporte', '').strip() or None
        
        # Verificar si el documento ya existe en este viaje
        # Solo buscar si tiene un valor válido
        documento_existente = False
        if rut:
            documento_existente = ViajePasajero.objects.filter(
                viaje=viaje,
                pasajero__rut=rut
            ).exists()
        elif pasaporte:
            documento_existente = ViajePasajero.objects.filter(
                viaje=viaje,
                pasajero__pasaporte=pasaporte
            ).exists()
        
        if documento_existente:
            pasajeros_en_viaje = ViajePasajero.objects.filter(viaje=viaje).select_related('pasajero').order_by('-fecha_registro')
            form = PasajeroForm(request.POST)
            context = {
                'viaje': viaje,
                'pasajeros_en_viaje': pasajeros_en_viaje,
                'pasajero_form': form,
            }
            messages.warning(request, '⚠️ Este pasajero (con el mismo RUT/Pasaporte) ya está registrado en este viaje.')
            return render(request, 'viajes/viaje_pasajeros.html', context)
        
        form = PasajeroForm(request.POST)
        if form.is_valid():
            try:
                # Obtener datos adicionales del formulario antes de crear
                asiento = request.POST.get('asiento', '').strip()
                observaciones = request.POST.get('observaciones', '').strip()
                
                # Validar que el asiento no esté duplicado en este viaje
                if asiento:
                    asiento_duplicado = ViajePasajero.objects.filter(
                        viaje=viaje,
                        asiento=asiento
                    ).exists()
                    
                    if asiento_duplicado:
                        pasajeros_en_viaje = ViajePasajero.objects.filter(viaje=viaje).select_related('pasajero').order_by('-fecha_registro')
                        context = {
                            'viaje': viaje,
                            'pasajeros_en_viaje': pasajeros_en_viaje,
                            'pasajero_form': form,
                        }
                        messages.error(request, f'El asiento "{asiento}" ya está asignado a otro pasajero en este viaje.')
                        return render(request, 'viajes/viaje_pasajeros.html', context)
                
                with transaction.atomic():
                    # Crear el pasajero
                    pasajero = form.save()
                    
                    # Verificar capacidad del bus
                    if viaje.get_pasajeros_count() >= viaje.bus.capacidad_pasajeros:
                        messages.warning(request, f'Pasajero {pasajero.nombre_completo} creado, pero el bus ha alcanzado su capacidad máxima. No se agregó al viaje automáticamente.')
                    else:
                        # Agregar automáticamente el pasajero al viaje
                        ViajePasajero.objects.create(
                            viaje=viaje,
                            pasajero=pasajero,
                            asiento=asiento if asiento else None,
                            observaciones=observaciones if observaciones else 'Creado desde gestión de viaje'
                        )
                        
                        # Actualizar el contador de pasajeros confirmados
                        viaje.pasajeros_confirmados = viaje.get_pasajeros_count()
                        viaje.save()
                        
                        messages.success(request, f'Pasajero {pasajero.nombre_completo} creado y agregado al viaje exitosamente.')
                    
                    return redirect('viajes:viaje_pasajeros', pk=pk)
                    
            except Exception as e:
                messages.error(request, f'Error al crear el pasajero: {str(e)}')
        else:
            # Si hay errores, volver a la vista de pasajeros con el formulario con errores
            pasajeros_en_viaje = ViajePasajero.objects.filter(viaje=viaje).select_related('pasajero').order_by('-fecha_registro')
            
            context = {
                'viaje': viaje,
                'pasajeros_en_viaje': pasajeros_en_viaje,
                'pasajero_form': form,  # Formulario con errores
                'formulario_con_errores': True,
            }
            messages.error(request, '⚠️ Revisa los datos ingresados. Algunos campos tienen errores.')
            return render(request, 'viajes/viaje_pasajeros.html', context)
    
    # Si es GET, redirigir a la vista de pasajeros
    return redirect('viajes:viaje_pasajeros', pk=pk)


@login_required(login_url='login')
def generar_pdf_pasajeros(request, pk):
    """
    Vista para generar un PDF con la lista de pasajeros del viaje.
    """
    viaje = get_object_or_404(Viaje, pk=pk)
    pasajeros_en_viaje = ViajePasajero.objects.filter(viaje=viaje).select_related('pasajero').order_by('-fecha_registro')
    
    # Crear el objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pasajeros_viaje_{viaje.id}.pdf"'
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
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
        alignment=1  # Centrado
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=20,
        alignment=1
    )
    
    # Título
    title = Paragraph(f"Lista de Pasajeros - Viaje {viaje.id}", title_style)
    elements.append(title)
    
    # Información del viaje
    viaje_info = f"""
    <b>Bus:</b> {viaje.bus.placa} - {viaje.bus.modelo}<br/>
    <b>Conductor:</b> {viaje.conductor.nombre} {viaje.conductor.apellido}<br/>
    <b>Origen:</b> {viaje.get_origen_display()}<br/>
    <b>Destino:</b> {viaje.get_destino_display()}<br/>
    <b>Fecha de Salida:</b> {viaje.fecha_salida.strftime('%d/%m/%Y %H:%M')}<br/>
    <b>Estado:</b> {viaje.get_estado_display()}
    """
    viaje_paragraph = Paragraph(viaje_info, styles['Normal'])
    elements.append(viaje_paragraph)
    elements.append(Spacer(1, 20))
    
    # Tabla de pasajeros
    data = [['#', 'Nombre Completo', 'Documento', 'Teléfono', 'Asiento', 'Observaciones']]
    
    for idx, vp in enumerate(pasajeros_en_viaje, 1):
        pasajero = vp.pasajero
        # Determinar el documento (RUT o Pasaporte)
        documento = ''
        if pasajero.rut:
            documento = f'RUT: {pasajero.rut}'
        elif pasajero.pasaporte:
            documento = f'PP: {pasajero.pasaporte}'
        else:
            documento = 'N/A'
        
        data.append([
            str(idx),
            pasajero.nombre_completo,
            documento,
            pasajero.telefono or 'N/A',
            vp.asiento or 'Sin asignar',
            vp.observaciones or '-'
        ])
    
    # Crear la tabla
    table = Table(data, colWidths=[0.5*inch, 2*inch, 1.2*inch, 1.2*inch, 0.8*inch, 1.8*inch])
    
    # Estilo de la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Resumen
    total_pasajeros = pasajeros_en_viaje.count()
    capacidad = viaje.bus.capacidad_pasajeros
    disponibles = capacidad - total_pasajeros
    
    resumen = f"""
    <b>Total de Pasajeros:</b> {total_pasajeros}<br/>
    <b>Capacidad del Bus:</b> {capacidad}<br/>
    <b>Asientos Disponibles:</b> {disponibles}<br/>
    <b>Ocupación:</b> {int((total_pasajeros / capacidad) * 100) if capacidad > 0 else 0}%
    """
    resumen_paragraph = Paragraph(resumen, styles['Normal'])
    elements.append(resumen_paragraph)
    
    # Pie de página
    elements.append(Spacer(1, 30))
    footer = Paragraph(
        f"Generado el {timezone.now().strftime('%d/%m/%Y %H:%M')} - FlotaGest - Hotel El Greco",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=1)
    )
    elements.append(footer)
    
    # Construir el PDF
    doc.build(elements)
    
    # Obtener el valor del buffer y escribirlo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response


@login_required
def iniciar_viaje(request, pk):
    """
    Vista para iniciar un viaje, cambiando su estado de PROGRAMADO a EN CURSO.
    Esto hace que el viaje aparezca en la lista de viajes pendientes de registro de costos.
    """
    viaje = get_object_or_404(Viaje, pk=pk)
    
    # Solo permitir iniciar viajes en estado PROGRAMADO
    if viaje.estado != 'programado':
        messages.warning(request, f'El viaje ya está en estado {viaje.get_estado_display()}.')
        return redirect('viajes:viaje_list')
    
    # Cambiar estado a EN CURSO
    viaje.estado = 'en_curso'
    viaje.save()
    
    # Si es un viaje de ida con viaje de vuelta relacionado, también iniciarlo
    if viaje.es_ida_vuelta and viaje.tipo_trayecto == 'ida' and viaje.viaje_relacionado:
        viaje_vuelta = viaje.viaje_relacionado
        if viaje_vuelta.estado == 'programado':
            viaje_vuelta.estado = 'en_curso'
            viaje_vuelta.save()
            messages.success(request, f'Viajes de IDA y VUELTA iniciados correctamente. Ahora aparecen en la lista de viajes pendientes de registro de costos.')
    else:
        messages.success(request, f'Viaje iniciado correctamente. Ahora aparece en la lista de viajes pendientes de registro de costos.')
    
    return redirect('viajes:viaje_list')


@login_required
def revertir_viaje(request, pk):
    """
    Vista para revertir un viaje de EN CURSO a PROGRAMADO.
    Solo se puede revertir si el viaje NO tiene costos registrados.
    """
    viaje = get_object_or_404(Viaje, pk=pk)
    
    # Verificar que el viaje esté EN CURSO
    if viaje.estado != 'en_curso':
        messages.warning(request, f'El viaje debe estar EN CURSO para revertirlo. Estado actual: {viaje.get_estado_display()}.')
        return redirect('costos:viajes_sin_costos')
    
    # Verificar que NO tenga costos registrados
    from costos.models import CostosViaje
    if CostosViaje.objects.filter(viaje=viaje).exists():
        messages.error(request, 'No se puede revertir un viaje que ya tiene costos registrados.')
        return redirect('costos:viajes_sin_costos')
    
    # Cambiar estado a PROGRAMADO
    viaje.estado = 'programado'
    viaje.save()
    
    # Si es un viaje de ida con viaje de vuelta relacionado, también revertirlo
    if viaje.es_ida_vuelta and viaje.tipo_trayecto == 'ida' and viaje.viaje_relacionado:
        viaje_vuelta = viaje.viaje_relacionado
        if viaje_vuelta.estado == 'en_curso' and not CostosViaje.objects.filter(viaje=viaje_vuelta).exists():
            viaje_vuelta.estado = 'programado'
            viaje_vuelta.save()
            messages.success(request, f'Viajes de IDA y VUELTA revertidos a PROGRAMADO correctamente.')
    else:
        messages.success(request, f'Viaje revertido a PROGRAMADO correctamente.')
    
    return redirect('costos:viajes_sin_costos')
