from django import forms
from .models import CostosViaje, PuntoRecarga
from viajes.models import Viaje


class CostosViajeForm(forms.ModelForm):
    """
    Formulario para crear o editar costos de un viaje.
    """
    mantenimientos = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Mantenimientos realizados (seleccione uno o varios)'
    )

    class Meta:
        model = CostosViaje
        fields = ['viaje', 'mantenimientos', 'peajes', 'otros_costos', 'observaciones']
        widgets = {
            'viaje': forms.Select(attrs={'class': 'form-control'}),
            'peajes': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'otros_costos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'viaje': 'Viaje',
            'peajes': 'Costo de Peajes (CLP)',
            'otros_costos': 'Otros Costos (CLP)',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo viajes que no tengan costos asignados (si es creación)
        if not self.instance.pk:
            viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
            self.fields['viaje'].queryset = Viaje.objects.exclude(id__in=viajes_con_costos)

        # Filtrar mantenimientos por bus del viaje seleccionado
        from flota.models import Mantenimiento
        self.fields['mantenimientos'].queryset = Mantenimiento.objects.none()
        if 'viaje' in self.data:
            try:
                viaje_id = int(self.data.get('viaje'))
                from flota.models import Mantenimiento, Bus
                bus = Viaje.objects.get(pk=viaje_id).bus
                self.fields['mantenimientos'].queryset = Mantenimiento.objects.filter(bus=bus)
            except Exception:
                self.fields['mantenimientos'].queryset = Mantenimiento.objects.none()
        elif self.instance.pk and self.instance.viaje:
            bus = self.instance.viaje.bus
            from flota.models import Mantenimiento
            self.fields['mantenimientos'].queryset = Mantenimiento.objects.filter(bus=bus)


class PuntoRecargaForm(forms.ModelForm):
    """
    Formulario para agregar puntos de recarga de combustible.
    """
    class Meta:
        model = PuntoRecarga
        fields = ['orden', 'kilometraje', 'precio_combustible', 'litros_cargados', 'ubicacion', 'observaciones']
        widgets = {
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'precio_combustible': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'litros_cargados': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'orden': 'Orden',
            'kilometraje': 'Kilometraje (km)',
            'precio_combustible': 'Precio por Litro (CLP)',
            'litros_cargados': 'Litros Cargados',
            'ubicacion': 'Ubicación del Punto',
            'observaciones': 'Observaciones',
        }
        help_texts = {
            'orden': 'Orden del punto de recarga (1, 2, 3...)',
            'kilometraje': 'Kilometraje del bus al llegar a este punto',
            'precio_combustible': 'Precio del combustible en CLP por litro',
            'litros_cargados': 'Cantidad de litros cargados',
        }

    def __init__(self, *args, costos_viaje=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.costos_viaje = costos_viaje
        
        # Si es un nuevo punto, sugerir el siguiente orden y kilometraje inicial
        if not self.instance.pk and costos_viaje:
            ultimo_orden = PuntoRecarga.objects.filter(costos_viaje=costos_viaje).count()
            self.fields['orden'].initial = ultimo_orden + 1
            
            # Establecer el kilometraje inicial basado en el último punto
            ultimo_punto = PuntoRecarga.objects.filter(costos_viaje=costos_viaje).order_by('-orden').first()
            if ultimo_punto:
                self.fields['kilometraje'].initial = ultimo_punto.kilometraje
                self.fields['kilometraje'].widget.attrs['min'] = str(ultimo_punto.kilometraje)
            else:
                # Si no hay puntos anteriores, usar el kilometraje inicial del bus
                self.fields['kilometraje'].initial = costos_viaje.viaje.bus.kilometraje_inicial
                self.fields['kilometraje'].widget.attrs['min'] = str(costos_viaje.viaje.bus.kilometraje_inicial)

    def clean_kilometraje(self):
        kilometraje = self.cleaned_data['kilometraje']
        
        if self.costos_viaje:
            # Validar que el kilometraje sea mayor al inicial del bus
            kilometraje_inicial = self.costos_viaje.viaje.bus.kilometraje_inicial
            if kilometraje < kilometraje_inicial:
                raise forms.ValidationError(
                    f'El kilometraje debe ser mayor o igual al kilometraje inicial del bus ({kilometraje_inicial} km)'
                )
            
            # Validar que el kilometraje sea mayor al punto anterior
            orden = self.cleaned_data.get('orden', 1)
            if orden > 1:
                punto_anterior = PuntoRecarga.objects.filter(
                    costos_viaje=self.costos_viaje,
                    orden__lt=orden
                ).order_by('-orden').first()
                
                if punto_anterior and kilometraje <= punto_anterior.kilometraje:
                    raise forms.ValidationError(
                        f'El kilometraje debe ser mayor al punto anterior ({punto_anterior.kilometraje} km)'
                    )
        
        return kilometraje

    def clean_orden(self):
        orden = self.cleaned_data['orden']
        
        if orden < 1:
            raise forms.ValidationError('El orden debe ser mayor o igual a 1')
        
        # Validar que no exista otro punto con el mismo orden (si es creación o cambio de orden)
        if self.costos_viaje:
            query = PuntoRecarga.objects.filter(costos_viaje=self.costos_viaje, orden=orden)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise forms.ValidationError(f'Ya existe un punto de recarga con el orden {orden}')
        
        return orden


class KmInicialForm(forms.ModelForm):
    class Meta:
        model = CostosViaje
        fields = ['km_inicial']
        widgets = {
            'km_inicial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': 'Ingrese el kilometraje inicial real del viaje'})
        }
        labels = {
            'km_inicial': 'Kilometraje inicial del viaje',
        }
        help_texts = {
            'km_inicial': 'Este valor se usará como referencia para todos los cálculos de este viaje.'
        }


class KmFinalForm(forms.ModelForm):
    class Meta:
        model = CostosViaje
        fields = ['km_final']
        widgets = {
            'km_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el kilometraje final del viaje',
                'step': '0.01',
                'min': '0',
            })
        }
        labels = {
            'km_final': 'Kilometraje final del viaje'
        }
        help_texts = {
            'km_final': 'Ingrese el kilometraje final real al terminar el viaje.'
        }
