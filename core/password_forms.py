"""
Formularios para cambio de contraseña
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class ChangePasswordForm(forms.Form):
    """Formulario para cambiar contraseña con validación de contraseña maestra"""
    
    master_password = forms.CharField(
        label='🔐 Contraseña Maestra',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa la contraseña maestra',
            'autocomplete': 'off'
        }),
        help_text='Ingresa la contraseña maestra para autorizar el cambio'
    )
    
    new_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa la nueva contraseña',
            'autocomplete': 'new-password'
        }),
        help_text='Mínimo 8 caracteres, debe incluir letras, números y caracteres especiales'
    )
    
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma la nueva contraseña',
            'autocomplete': 'new-password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # Validar que las contraseñas coincidan
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError('Las contraseñas no coinciden')
            
            # Validar fuerza de contraseña
            try:
                validate_password(new_password)
            except ValidationError as e:
                self.add_error('new_password', e)
        
        return cleaned_data


class ChangeOtherUserPasswordForm(forms.Form):
    """Formulario para que admin cambie contraseña de otro usuario"""
    
    username = forms.CharField(
        label='👤 Usuario a Modificar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa el nombre de usuario',
            'readonly': 'readonly'  # Solo lectura, se pasa como parámetro
        })
    )
    
    master_password = forms.CharField(
        label='🔐 Contraseña Maestra',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa la contraseña maestra',
            'autocomplete': 'off'
        }),
        help_text='Ingresa la contraseña maestra para autorizar el cambio'
    )
    
    new_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa la nueva contraseña',
            'autocomplete': 'new-password'
        }),
        help_text='Mínimo 8 caracteres, debe incluir letras, números y caracteres especiales'
    )
    
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma la nueva contraseña',
            'autocomplete': 'new-password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError('Las contraseñas no coinciden')
            
            try:
                validate_password(new_password)
            except ValidationError as e:
                self.add_error('new_password', e)
        
        return cleaned_data


class AdminChangePasswordForm(forms.Form):
    """Formulario simple para admin cambiar contraseña de usuario (sin validación de maestra)"""
    
    username = forms.CharField(
        label='👤 Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'readonly': 'readonly'
        })
    )
    
    new_password = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña',
            'autocomplete': 'new-password'
        }),
        help_text='Mínimo 8 caracteres, debe incluir letras, números y caracteres especiales'
    )
    
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'autocomplete': 'new-password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError('Las contraseñas no coinciden')
            
            try:
                validate_password(new_password)
            except ValidationError as e:
                self.add_error('new_password', e)
        
        return cleaned_data
