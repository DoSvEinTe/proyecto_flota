from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .models import Conductor, Lugar, Pasajero
from .permissions import admin_required, usuario_or_admin_required
import math


class ConductorForm(ModelForm):
    LICENCIAS_CHOICES = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('A3', 'A3'),
        ('A4', 'A4'),
        ('A5', 'A5'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    ]

    licencias = forms.MultipleChoiceField(
        choices=LICENCIAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Licencias',
        help_text='Selecciona al menos una licencia que posee el conductor.'
    )

    class Meta:
        model = Conductor
        fields = ['nombre', 'apellido', 'cedula', 'cedula_frontal', 'cedula_trasera', 'email', 'telefono', 'fecha_contratacion', 'activo', 'licencia_conducir_frontal', 'licencia_conducir_trasera', 'licencias']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del conductor'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido del conductor'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de cédula'}),
            'cedula_frontal': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
            'cedula_trasera': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'fecha_contratacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'licencia_conducir_frontal': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
            'licencia_conducir_trasera': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.licencias:
            self.initial['licencias'] = self.instance.licencias.split(',')

    def clean_licencias(self):
        licencias = self.cleaned_data.get('licencias', [])
        return ','.join(licencias)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.licencias = self.cleaned_data.get('licencias', '')
        if commit:
            instance.save()
        return instance




# Vistas para Conductores
@method_decorator(admin_required, name='dispatch')
class ConductorListView(ListView):
    model = Conductor
    template_name = 'core/conductor_list.html'
    context_object_name = 'conductores'
    paginate_by = 20

    def get_queryset(self):
        return Conductor.objects.all().order_by('-creado_en')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conductores = context['conductores']
        # Agregar lista de licencias procesada para cada conductor
        licencias_dict = {
            'A1': 'Taxis',
            'A2': 'Taxis, ambulancias y transporte público/privado de 10 a 17 pasajeros',
            'A3': 'Taxis, ambulancias, transporte escolar y vehículos de transporte público/privado sin límite de asientos',
            'A4': 'Transporte de carga > 3.500 kg',
            'A5': 'Todo tipo de vehículos de carga > 3.500 kg',
            'B': 'Vehículos particulares ≤ 3.500 kg, hasta 9 asientos',
            'C': 'Vehículos motorizados de dos o tres ruedas',
            'D': 'Maquinaria automotriz (tractores, grúas, etc.)',
            'E': 'Vehículos de tracción animal',
            'F': 'Vehículos de FF.AA., Carabineros, PDI, Bomberos',
        }
        lista_conductores = []
        for conductor in conductores:
            licencias_list = []
            for cod in conductor.licencias.split(',') if conductor.licencias else []:
                licencias_list.append({'codigo': cod, 'descripcion': licencias_dict.get(cod, cod)})
            lista_conductores.append({
                'obj': conductor,
                'licencias_list': licencias_list
            })
        context['conductores_list'] = lista_conductores
        return context


@method_decorator(admin_required, name='dispatch')
class ConductorDetailView(DetailView):
    model = Conductor
    template_name = 'core/conductor_detail.html'
    context_object_name = 'conductor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conductor = self.object
        # Calcular tiempo en la empresa
        if conductor.fecha_contratacion:
            from datetime import date
            hoy = date.today()
            delta = hoy - conductor.fecha_contratacion
            años = delta.days // 365
            meses = (delta.days % 365) // 30
            dias = (delta.days % 365) % 30
            context['tiempo_empresa'] = f"{años} año(s), {meses} mes(es), {dias} día(s)"
        else:
            context['tiempo_empresa'] = "-"
        # Diccionario de descripciones
        licencias_dict = {
            'A1': 'Taxis',
            'A2': 'Taxis, ambulancias y transporte público/privado de 10 a 17 pasajeros',
            'A3': 'Taxis, ambulancias, transporte escolar y vehículos de transporte público/privado sin límite de asientos',
            'A4': 'Transporte de carga > 3.500 kg',
            'A5': 'Todo tipo de vehículos de carga > 3.500 kg',
            'B': 'Vehículos particulares ≤ 3.500 kg, hasta 9 asientos',
            'C': 'Vehículos motorizados de dos o tres ruedas',
            'D': 'Maquinaria automotriz (tractores, grúas, etc.)',
            'E': 'Vehículos de tracción animal',
            'F': 'Vehículos de FF.AA., Carabineros, PDI, Bomberos',
        }
        licencias_list = []
        for cod in conductor.licencias.split(',') if conductor.licencias else []:
            licencias_list.append({'codigo': cod, 'descripcion': licencias_dict.get(cod, cod)})
        context['licencias_list'] = licencias_list
        return context


@method_decorator(admin_required, name='dispatch')
class ConductorCreateView(CreateView):
    model = Conductor
    form_class = ConductorForm
    template_name = 'core/conductor_form.html'
    success_url = reverse_lazy('conductor_list')

    def form_valid(self, form):
        messages.success(self.request, f'Conductor {form.instance.nombre} {form.instance.apellido} creado exitosamente.')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class ConductorUpdateView(UpdateView):
    model = Conductor
    form_class = ConductorForm
    template_name = 'core/conductor_form.html'
    success_url = reverse_lazy('conductor_list')

    def form_valid(self, form):
        messages.success(self.request, f'Conductor {form.instance.nombre} {form.instance.apellido} actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class ConductorDeleteView(DeleteView):
    model = Conductor
    template_name = 'core/conductor_confirm_delete.html'
    success_url = reverse_lazy('conductor_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f'Conductor {self.object.nombre} {self.object.apellido} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)




# Vista Home - Dashboard con estadísticas
@login_required(login_url='login')
def home_view(request):
    from flota.models import Bus, DocumentoVehiculo
    from viajes.models import Viaje
    from datetime import date, timedelta
    
    # Obtener buses con sus placas
    buses = Bus.objects.all()
    
    # Obtener documentos próximos a vencer (en los próximos 30 días)
    hoy = date.today()
    fecha_limite = hoy + timedelta(days=30)
    
    documentos_proximos_vencer = DocumentoVehiculo.objects.filter(
        fecha_vencimiento__gte=hoy,
        fecha_vencimiento__lte=fecha_limite,
        estado__in=['por_vencer', 'vigente']
    ).select_related('bus').order_by('fecha_vencimiento')[:5]  # Últimos 5
    
    # Documentos ya vencidos
    documentos_vencidos = DocumentoVehiculo.objects.filter(
        fecha_vencimiento__lt=hoy,
        estado='vencido'
    ).select_related('bus').order_by('-fecha_vencimiento')[:5]  # Últimos 5
    
    context = {
        'total_buses': buses.count(),
        'buses': buses,
        'total_conductores': Conductor.objects.count(),
        'total_lugares': Lugar.objects.count(),
        'total_pasajeros': Pasajero.objects.count(),
        'total_viajes': Viaje.objects.count(),
        'documentos_proximos_vencer': documentos_proximos_vencer,
        'documentos_vencidos': documentos_vencidos,
    }
    return render(request, 'home.html', context)


