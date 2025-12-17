from django import forms
from datetime import date
import re
from .models import Mantenimiento, DocumentoVehiculo, Bus

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['placa', 'marca', 'modelo', 'año_fabricacion', 'capacidad_pasajeros', 'kilometraje_ingreso',
                  'numero_chasis', 'numero_motor', 'estado', 'fecha_adquisicion']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: AB-1234-CD o ABCD-12-EF', 'style': 'text-transform: uppercase;'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mercedes Benz'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: O500RS'}),
            'año_fabricacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1990}),
            'capacidad_pasajeros': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 70}),
            'kilometraje_ingreso': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'numero_chasis': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_motor': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_adquisicion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer dinámicamente el max de fecha_adquisicion al día actual
        today_str = date.today().isoformat()
        self.fields['fecha_adquisicion'].widget.attrs['max'] = today_str
        
        # Establecer dinámicamente el max del año_fabricacion al año actual
        año_actual = date.today().year
        self.fields['año_fabricacion'].widget.attrs['max'] = año_actual
        
        # Hacer número de chasis y número de motor opcionales
        self.fields['numero_chasis'].required = False
        self.fields['numero_motor'].required = False
        
        # Agregar ayuda para el campo de placa
        self.fields['placa'].help_text = '<strong>Formato de Patente:</strong><br>' \
                                         '• Formato antiguo: <code>AB-1234-CD</code> (2 letras - 4 números - 2 letras)<br>' \
                                         '• Formato moderno: <code>ABCD-12-EF</code> (4 caracteres - 2 números - 2 caracteres)<br>' \
                                         '<i class="fas fa-exclamation-circle"></i> <strong>Importante:</strong> La patente DEBE incluir guiones (-) en las posiciones correctas.'
        
        # Asegurar que el campo de fecha muestre el valor inicial correctamente en edición
        if self.instance and self.instance.pk and self.instance.fecha_adquisicion:
            self.fields['fecha_adquisicion'].initial = self.instance.fecha_adquisicion
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_adquisicion = cleaned_data.get('fecha_adquisicion')
        año_fabricacion = cleaned_data.get('año_fabricacion')
        placa = cleaned_data.get('placa')
        
        # Validar formato de placa (Chile)
        if placa:
            placa_upper = placa.upper().strip()
            # Formato antiguo: XX-1234-XX (2 letras - 4 números - 2 letras)
            # Formato moderno: XXXX-12-XX (4 caracteres - 2 números - 2 caracteres)
            patron_antiguo = re.compile(r'^[A-Z]{2}-\d{4}-[A-Z]{2}$')
            patron_moderno = re.compile(r'^[A-Z0-9]{4}-\d{2}-[A-Z0-9]{2}$')
            
            if not (patron_antiguo.match(placa_upper) or patron_moderno.match(placa_upper)):
                raise forms.ValidationError({
                    'placa': 'Formato de placa inválido (Chile). Debe ser: AB-1234-CD (antiguo) o ABCD-12-EF (moderno)'
                })
            
            # Verificar estructura básica
            partes = placa_upper.split('-')
            if len(partes) != 3:
                raise forms.ValidationError({
                    'placa': 'La placa debe contener dos guiones (-) separando sus partes.'
                })
            
            primera_parte = partes[0]
            segunda_parte = partes[1]
            tercera_parte = partes[2]
            
            # Validar primera parte
            if len(primera_parte) == 2:  # Formato antiguo
                if not primera_parte.isalpha():
                    raise forms.ValidationError({
                        'placa': 'Los primeros 2 caracteres deben ser letras (formato antiguo).'
                    })
                # Validar segunda parte (debe ser 4 números)
                if len(segunda_parte) != 4 or not segunda_parte.isdigit():
                    raise forms.ValidationError({
                        'placa': 'Los números deben ser exactamente 4 dígitos (formato antiguo).'
                    })
                # Validar tercera parte (debe ser 2 letras)
                if len(tercera_parte) != 2 or not tercera_parte.isalpha():
                    raise forms.ValidationError({
                        'placa': 'Los últimos 2 caracteres deben ser letras (formato antiguo).'
                    })
            elif len(primera_parte) == 4:  # Formato moderno
                # Validar segunda parte (debe ser 2 números)
                if len(segunda_parte) != 2 or not segunda_parte.isdigit():
                    raise forms.ValidationError({
                        'placa': 'La parte central debe ser exactamente 2 números (formato moderno).'
                    })
                # Validar tercera parte (debe ser 2 caracteres)
                if len(tercera_parte) != 2:
                    raise forms.ValidationError({
                        'placa': 'Los últimos 2 caracteres representan la región (formato moderno).'
                    })
            else:
                raise forms.ValidationError({
                    'placa': 'Formato de placa inválido. Use AB-1234-CD o ABCD-12-EF'
                })
        
        if fecha_adquisicion:
            if fecha_adquisicion > date.today():
                raise forms.ValidationError({'fecha_adquisicion': 'La fecha de adquisición no puede ser superior al día actual.'})
        
        if año_fabricacion:
            año_actual = date.today().year
            if año_fabricacion > año_actual:
                raise forms.ValidationError({'año_fabricacion': f'El año de fabricación no puede ser superior a {año_actual}.'})
        
        return cleaned_data


class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ['fecha_mantenimiento', 'tipo', 'descripcion', 'observaciones', 'costo', 'proveedor', 'taller', 'kilometraje', 'comprobante']
        widgets = {
            'fecha_mantenimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Descripción del trabajo realizado...',
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Observaciones adicionales...',
                'class': 'form-control'
            }),
            'costo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'taller': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometraje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
        }
        labels = {
            'fecha_mantenimiento': 'Fecha de Mantenimiento',
            'descripcion': 'Descripción',
            'observaciones': 'Observaciones',
            'costo': 'Costo ($)',
            'kilometraje': 'Kilometraje (km)',
            'comprobante': 'Comprobante (Imagen/PDF)',
        }
    
    def __init__(self, *args, **kwargs):
        self.bus = kwargs.pop('bus', None)
        super().__init__(*args, **kwargs)
        from datetime import date
        today_str = date.today().isoformat()
        # Fecha de mantenimiento máxima = hoy
        self.fields['fecha_mantenimiento'].widget.attrs['max'] = today_str
        
        # Si hay bus, establecer el min del kilometraje al kilometraje_ingreso del bus
        if self.bus:
            self.fields['kilometraje'].widget.attrs['min'] = self.bus.kilometraje_ingreso
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_mantenimiento = cleaned_data.get('fecha_mantenimiento')
        
        # Validar que la fecha de mantenimiento no sea superior al día actual
        if fecha_mantenimiento:
            from datetime import date
            if fecha_mantenimiento > date.today():
                raise forms.ValidationError({'fecha_mantenimiento': 'La fecha de mantenimiento no puede ser superior al día actual.'})
        
        return cleaned_data


class DocumentoVehiculoForm(forms.ModelForm):
    class Meta:
        model = DocumentoVehiculo
        fields = ['tipo', 'numero_documento', 'fecha_emision', 'fecha_vencimiento', 'archivo', 'observaciones']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Observaciones del documento...',
                'class': 'form-control'
            }),
        }
        labels = {
            'tipo': 'Tipo de Documento',
            'numero_documento': 'Número de Documento',
            'fecha_emision': 'Fecha de Emisión',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'archivo': 'Archivo (PDF, imagen, etc.) *',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import date
        today_str = date.today().isoformat()
        # Fecha de emisión máxima = hoy
        self.fields['fecha_emision'].widget.attrs['max'] = today_str
        
        # Si es una edición (tiene pk), el archivo es opcional
        # Si es una creación nueva, el archivo es obligatorio
        if self.instance.pk:
            self.fields['archivo'].required = False
            self.fields['archivo'].label = 'Archivo (PDF, imagen, etc.)'
        else:
            self.fields['archivo'].required = True
            self.fields['archivo'].label = 'Archivo (PDF, imagen, etc.) *'
        
        # Mostrar fecha actual en edición
        if self.instance and self.instance.pk and self.instance.fecha_emision:
            self.fields['fecha_emision'].initial = self.instance.fecha_emision
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')
        
        if fecha_emision and fecha_vencimiento:
            if fecha_vencimiento < fecha_emision:
                raise forms.ValidationError('La fecha de vencimiento no puede ser anterior a la fecha de emisión.')
        
        return cleaned_data