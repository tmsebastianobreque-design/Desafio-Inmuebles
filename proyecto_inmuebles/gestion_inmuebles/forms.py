from django import forms
from django.contrib.auth.models import User
from .models import Usuario
from .models import Inmueble

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    rut = forms.CharField(label="RUT", widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label="Dirección", widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label="Teléfono personal", widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo_usuario = forms.ChoiceField(
        label="Identificarse como",
        choices=[('arrendatario', 'Arrendatario'), ('arrendador', 'Arrendador')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        # 1. Guardamos el objeto User base de Django
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            
            Usuario.objects.create(
                user=user,
                rut=self.cleaned_data['rut'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                tipo_usuario=self.cleaned_data['tipo_usuario']
            )
        return user


class UserUpdateForm(forms.ModelForm):
    rut = forms.CharField(label="RUT", widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label="Dirección", widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label="Teléfono personal", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        # Usamos los nombres exactos de tu models.py
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'estacionamientos', 'habitaciones', 'banos', 'direccion', 'comuna', 'tipo_inmueble', 'precio_mensual']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'm2_construidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'm2_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'estacionamientos': forms.NumberInput(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'banos': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-control'}),
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
            'precio_mensual': forms.NumberInput(attrs={'class': 'form-control'})
        }