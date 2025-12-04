from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.http import JsonResponse
from django.db import transaction
from .models import Viaje, ViajePasajero
from core.models import Conductor, Lugar, Pasajero
from flota.models import Bus
from core.permissions import admin_required, usuario_or_admin_required


class PasajeroForm(ModelForm):
    class Meta:
        model = Pasajero
        fields = ['nombre_completo', 'rut', 'telefono', 'correo']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del pasajero'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT (ej: 12345678-9)'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }
    
    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo')
        if nombre and len(nombre.strip()) < 3:
            raise forms.ValidationError('El nombre completo debe tener al menos 3 caracteres.')
        return nombre.strip() if nombre else nombre
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            rut = rut.strip().upper()
            # Validar formato básico de RUT (permite formato con o sin guion)
            if not rut.replace('-', '').replace('.', '').isalnum():
                raise forms.ValidationError('El RUT debe contener solo números y letras.')
        return rut
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            telefono = telefono.strip()
            # Validar que el teléfono contenga solo números y caracteres permitidos
            if not telefono.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
                raise forms.ValidationError('El teléfono debe contener solo números y caracteres permitidos (+, -, espacios, paréntesis).')
        return telefono


class ViajeForm(ModelForm):
    class Meta:
        model = Viaje
        fields = [
            'bus', 'conductor',
            'origen_nombre', 'origen_ciudad', 'origen_provincia', 'origen_pais',
            'latitud_origen', 'longitud_origen',
            'destino_nombre', 'destino_ciudad', 'destino_provincia', 'destino_pais',
            'latitud_destino', 'longitud_destino',
            'fecha_salida', 'fecha_llegada_estimada', 'fecha_llegada_real',
            'estado', 'observaciones'
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
            }),
            'fecha_llegada_estimada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora estimada de llegada'
            }),
            'fecha_llegada_real': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Fecha y hora real de llegada (opcional)'
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
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
    paginate_by = 20

    def get_queryset(self):
        return Viaje.objects.all().order_by('-fecha_salida')


@method_decorator(usuario_or_admin_required, name='dispatch')
class ViajeDetailView(DetailView):
    model = Viaje
    template_name = 'viajes/viaje_detail.html'
    context_object_name = 'viaje'


@method_decorator(usuario_or_admin_required, name='dispatch')
class ViajeCreateView(CreateView):
    model = Viaje
    form_class = ViajeForm
    template_name = 'viajes/viaje_form.html'
    success_url = reverse_lazy('viajes:viaje_list')

    def form_valid(self, form):
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
    viaje = get_object_or_404(Viaje, pk=pk)
    pasajeros_en_viaje = ViajePasajero.objects.filter(viaje=viaje).select_related('pasajero')
    pasajeros_disponibles = Pasajero.objects.exclude(id__in=viaje.pasajeros.values_list('id', flat=True))
    
    context = {
        'viaje': viaje,
        'pasajeros_en_viaje': pasajeros_en_viaje,
        'pasajeros_disponibles': pasajeros_disponibles,
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
    Vista para editar información de un pasajero en un viaje.
    """
    viaje = get_object_or_404(Viaje, pk=pk)
    pasajero = get_object_or_404(Pasajero, pk=pasajero_pk)
    viaje_pasajero = get_object_or_404(ViajePasajero, viaje=viaje, pasajero=pasajero)
    
    if request.method == 'POST':
        asiento = request.POST.get('asiento')
        observaciones = request.POST.get('observaciones', '')
        
        viaje_pasajero.asiento = asiento
        viaje_pasajero.observaciones = observaciones
        viaje_pasajero.save()
        
        messages.success(request, f'Información del pasajero {pasajero.nombre_completo} actualizada exitosamente.')
        return redirect('viajes:viaje_pasajeros', pk=pk)
    
    context = {
        'viaje': viaje,
        'pasajero': pasajero,
        'viaje_pasajero': viaje_pasajero,
    }
    return render(request, 'viajes/editar_pasajero_viaje.html', context)


# Vistas para Pasajeros (dentro de viajes)
@method_decorator(usuario_or_admin_required, name='dispatch')
class PasajeroListView(ListView):
    model = Pasajero
    template_name = 'viajes/pasajero_list.html'
    context_object_name = 'pasajeros'
    paginate_by = 20

    def get_queryset(self):
        return Pasajero.objects.all().order_by('-creado_en')


@method_decorator(usuario_or_admin_required, name='dispatch')
class PasajeroDetailView(DetailView):
    model = Pasajero
    template_name = 'viajes/pasajero_detail.html'
    context_object_name = 'pasajero'


@method_decorator(usuario_or_admin_required, name='dispatch')
class PasajeroCreateView(CreateView):
    model = Pasajero
    form_class = PasajeroForm
    template_name = 'viajes/pasajero_form.html'
    success_url = reverse_lazy('viajes:pasajero_list')

    def form_valid(self, form):
        messages.success(self.request, f'Pasajero {form.instance.nombre_completo} creado exitosamente.')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class PasajeroUpdateView(UpdateView):
    model = Pasajero
    form_class = PasajeroForm
    template_name = 'viajes/pasajero_form.html'
    success_url = reverse_lazy('viajes:pasajero_list')

    def form_valid(self, form):
        messages.success(self.request, f'Pasajero {form.instance.nombre_completo} actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class PasajeroDeleteView(DeleteView):
    model = Pasajero
    template_name = 'viajes/pasajero_confirm_delete.html'
    success_url = reverse_lazy('viajes:pasajero_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f'Pasajero {self.object.nombre_completo} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
