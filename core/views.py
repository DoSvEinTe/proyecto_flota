from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.db import models
from .models import Conductor, Lugar, Pasajero
from .permissions import admin_required, usuario_or_admin_required


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


class LugarForm(ModelForm):
    class Meta:
        model = Lugar
        fields = ['nombre', 'ciudad', 'provincia', 'pais', 'latitud', 'longitud']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre del lugar',
                'id': 'id_nombre'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ciudad',
                'id': 'id_ciudad'
            }),
            'provincia': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Provincia (opcional)',
                'id': 'id_provincia'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'País',
                'id': 'id_pais'
            }),
            'latitud': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.000001', 
                'placeholder': 'Latitud (opcional)',
                'id': 'id_latitud'
            }),
            'longitud': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.000001', 
                'placeholder': 'Longitud (opcional)',
                'id': 'id_longitud'
            }),
        }


class PasajeroForm(ModelForm):
    tipo_documento = forms.ChoiceField(
        choices=[('rut', 'RUT/Cédula'), ('pasaporte', 'Pasaporte')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='rut',
        label='Tipo de Documento'
    )
    
    class Meta:
        model = Pasajero
        fields = ['nombre_completo', 'rut', 'pasaporte', 'telefono', 'correo']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del pasajero'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT (ej: 12345678-9)', 'id': 'id_rut'}),
            'pasaporte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de pasaporte', 'id': 'id_pasaporte'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get('rut')
        pasaporte = cleaned_data.get('pasaporte')
        tipo_documento = cleaned_data.get('tipo_documento')
        
        # Validar que se ingrese RUT o Pasaporte según la selección
        if tipo_documento == 'rut':
            if not rut:
                raise forms.ValidationError('Debe ingresar un RUT/Cédula')
            # Limpiar pasaporte si se seleccionó RUT
            cleaned_data['pasaporte'] = None
        elif tipo_documento == 'pasaporte':
            if not pasaporte:
                raise forms.ValidationError('Debe ingresar un número de pasaporte')
            # Limpiar RUT si se seleccionó Pasaporte
            cleaned_data['rut'] = None
        
        return cleaned_data


# Vistas para Conductores
@method_decorator(admin_required, name='dispatch')
class ConductorListView(ListView):
    model = Conductor
    template_name = 'core/conductor_list.html'
    context_object_name = 'conductores'
    paginate_by = 10

    def get_queryset(self):
        queryset = Conductor.objects.all()
        
        # Búsqueda
        search = self.request.GET.get('search', '')
        if search:
            # Normalizar el texto de búsqueda (remover tildes)
            import unicodedata
            from django.db.models import Value, CharField
            from django.db.models.functions import Concat
            
            search_normalized = ''.join(
                c for c in unicodedata.normalize('NFD', search)
                if unicodedata.category(c) != 'Mn'
            )
            
            # Crear campo virtual con nombre completo
            queryset = queryset.annotate(
                nombre_completo=Concat('nombre', Value(' '), 'apellido', output_field=CharField())
            )
            
            # Buscar tanto en el texto original como en el normalizado
            q_filter = models.Q()
            for term in [search, search_normalized]:
                q_filter |= (
                    models.Q(nombre__icontains=term) |
                    models.Q(apellido__icontains=term) |
                    models.Q(nombre_completo__icontains=term) |
                    models.Q(cedula__icontains=term) |
                    models.Q(email__icontains=term) |
                    models.Q(telefono__icontains=term)
                )
            
            queryset = queryset.filter(q_filter)
        
        # Filtros
        estado = self.request.GET.get('estado', '')
        if estado == 'activo':
            queryset = queryset.filter(activo=True)
        elif estado == 'inactivo':
            queryset = queryset.filter(activo=False)
        
        licencia = self.request.GET.get('licencia', '')
        if licencia:
            queryset = queryset.filter(licencias__icontains=licencia)
        
        # Ordenamiento
        orden = self.request.GET.get('orden', '-creado_en')
        queryset = queryset.order_by(orden)
        
        return queryset

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
        
        # Mantener parámetros de búsqueda y filtros en el contexto
        context['search'] = self.request.GET.get('search', '')
        context['estado'] = self.request.GET.get('estado', '')
        context['licencia'] = self.request.GET.get('licencia', '')
        context['orden'] = self.request.GET.get('orden', '-creado_en')
        
        # Lista de licencias disponibles para el filtro
        context['licencias_opciones'] = [
            {'codigo': 'A1', 'nombre': 'A1 - Taxis'},
            {'codigo': 'A2', 'nombre': 'A2 - Transporte público 10-17 pasajeros'},
            {'codigo': 'A3', 'nombre': 'A3 - Transporte escolar'},
            {'codigo': 'A4', 'nombre': 'A4 - Carga > 3.500 kg'},
            {'codigo': 'A5', 'nombre': 'A5 - Carga pesada'},
            {'codigo': 'B', 'nombre': 'B - Particulares'},
            {'codigo': 'C', 'nombre': 'C - Motos'},
            {'codigo': 'D', 'nombre': 'D - Maquinaria'},
            {'codigo': 'E', 'nombre': 'E - Tracción animal'},
            {'codigo': 'F', 'nombre': 'F - FF.AA.'},
        ]
        
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


# Vistas para Lugares
@method_decorator(usuario_or_admin_required, name='dispatch')
class LugarListView(ListView):
    model = Lugar
    template_name = 'core/lugar_list.html'
    context_object_name = 'lugares'
    paginate_by = 20

    def get_queryset(self):
        return Lugar.objects.all().order_by('ciudad', 'nombre')


@method_decorator(usuario_or_admin_required, name='dispatch')
class LugarDetailView(DetailView):
    model = Lugar
    template_name = 'core/lugar_detail.html'
    context_object_name = 'lugar'


@method_decorator(usuario_or_admin_required, name='dispatch')
class LugarCreateView(CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'core/lugar_form.html'
    success_url = reverse_lazy('lugar_list')

    def form_valid(self, form):
        messages.success(self.request, f'Lugar {form.instance.nombre} creado exitosamente.')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class LugarUpdateView(UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'core/lugar_form.html'
    success_url = reverse_lazy('lugar_list')

    def form_valid(self, form):
        messages.success(self.request, f'Lugar {form.instance.nombre} actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class LugarDeleteView(DeleteView):
    model = Lugar
    template_name = 'core/lugar_confirm_delete.html'
    success_url = reverse_lazy('lugar_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f'Lugar {self.object.nombre} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# Vistas para Pasajeros
@method_decorator(usuario_or_admin_required, name='dispatch')
class PasajeroListView(ListView):
    model = Pasajero
    template_name = 'core/pasajero_list.html'
    context_object_name = 'pasajeros'
    paginate_by = 20

    def get_queryset(self):
        return Pasajero.objects.all().order_by('-creado_en')


@method_decorator(usuario_or_admin_required, name='dispatch')
class PasajeroDetailView(DetailView):
    model = Pasajero
    template_name = 'core/pasajero_detail.html'
    context_object_name = 'pasajero'


@method_decorator(usuario_or_admin_required, name='dispatch')
class PasajeroCreateView(CreateView):
    model = Pasajero
    form_class = PasajeroForm
    template_name = 'core/pasajero_form.html'
    success_url = reverse_lazy('pasajero_list')

    def form_valid(self, form):
        messages.success(self.request, f'Pasajero {form.instance.nombre_completo} creado exitosamente.')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class PasajeroUpdateView(UpdateView):
    model = Pasajero
    form_class = PasajeroForm
    template_name = 'core/pasajero_form.html'
    success_url = reverse_lazy('pasajero_list')

    def form_valid(self, form):
        messages.success(self.request, f'Pasajero {form.instance.nombre_completo} actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class PasajeroDeleteView(DeleteView):
    model = Pasajero
    template_name = 'core/pasajero_confirm_delete.html'
    success_url = reverse_lazy('pasajero_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f'Pasajero {self.object.nombre_completo} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# Vista Home - Dashboard con estadísticas
@login_required(login_url='login')
def home_view(request):
    from flota.models import Bus, DocumentoVehiculo
    from viajes.models import Viaje
    from costos.models import CostosViaje
    from datetime import date, timedelta
    from django.db.models import Sum, Avg, Count, Q
    from decimal import Decimal
    
    # Obtener buses con sus placas
    buses = Bus.objects.all()
    
    # Obtener viajes
    viajes = Viaje.objects.all()
    viajes_activos = viajes.filter(estado__in=['programado', 'en_curso']).count()
    viajes_completados = viajes.filter(estado='completado').count()
    ultimos_viajes = viajes.select_related('bus', 'conductor').order_by('-creado_en')[:5]
    
    # Estadísticas de costos
    costos = CostosViaje.objects.all()
    
    # Costos totales
    total_costos = costos.aggregate(
        total_combustible=Sum('combustible'),
        total_mantenimiento=Sum('mantenimiento'),
        total_peajes=Sum('peajes'),
        total_otros=Sum('otros_costos'),
        total_general=Sum('costo_total')
    )
    
    # Viajes con mayor costo
    viajes_mayor_costo = costos.select_related('viaje__bus', 'viaje__conductor').order_by('-costo_total')[:5]
    
    # Promedio de costos
    promedio_costos = costos.aggregate(
        promedio_combustible=Avg('combustible'),
        promedio_total=Avg('costo_total')
    )
    
    # Costos del último mes
    fecha_mes_atras = date.today() - timedelta(days=30)
    costos_mes = costos.filter(creado_en__gte=fecha_mes_atras).aggregate(
        total_mes=Sum('costo_total'),
        viajes_mes=Count('id')
    )
    
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
        'total_viajes': viajes.count(),
        'viajes_activos': viajes_activos,
        'viajes_completados': viajes_completados,
        'ultimos_viajes': ultimos_viajes,
        'documentos_proximos_vencer': documentos_proximos_vencer,
        'documentos_vencidos': documentos_vencidos,
        # Estadísticas de costos
        'total_costos': total_costos,
        'viajes_mayor_costo': viajes_mayor_costo,
        'promedio_costos': promedio_costos,
        'costos_mes': costos_mes,
        'total_costos_registrados': costos.count(),
    }
    return render(request, 'home_new.html', context)


