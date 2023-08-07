from django import forms
from ckeditor.widgets import CKEditorWidget

from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *

class CrearBlogFormulario (forms.Form):
    nombre = forms.CharField(max_length=250, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Nombre del Blog"}))
    
    descripcion = forms.CharField(max_length=500, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Descripcion del Blog"}))
    
    portada = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder" : "Portada"}))

    visibilidad = forms.ChoiceField(
        choices=[(0, 'Público'), (1, 'Restringido'), (2, 'Privado')],
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Seleccione la Visibilidad del Blog"}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class CrearPostFormulario (forms.Form):
    titulo = forms.CharField(max_length=250, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Titulo del Post"}))
    
    descripcion = forms.CharField(max_length=500, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Descripcion del Post"}))
    
    texto = forms.CharField(
        widget = CKEditorWidget(attrs={"class": "form-control", "placeholder" : "Descripcion del Post"}))
    
    imagen = forms.ImageField(required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Imagen para el Post"}))

    link = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Link para el Post"}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class EditarBlogFormulario (forms.ModelForm):
    nombre = forms.CharField(max_length=250, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Nombre del Blog"}))
    
    descripcion = forms.CharField(max_length=500, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Descripcion del Blog"}))
    
    portada = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder" : "Portada"}))

    visibilidad = forms.ChoiceField(
        choices=[(0, 'Público'), (1, 'Restringido'), (2, 'Privado')],
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Seleccione la Visibilidad del Blog"}))
       
    class Meta:
        model = Blog
        fields = ['nombre', 'descripcion', 'portada', 'visibilidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class EditarPostFormulario (forms.ModelForm):
    titulo = forms.CharField(max_length=250, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Titulo del Post"}))
    
    descripcion = forms.CharField(max_length=500, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Descripcion del Post"}))
    
    texto = forms.CharField(
        widget = CKEditorWidget(attrs={"class": "form-control", "placeholder" : "Descripcion del Post"}))
    
    imagen = forms.ImageField(required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Imagen para el Post"}))

    link = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Link para el Post"}))
    
    estado = forms.ChoiceField(
        choices=[(0, 'Inactivo'), (1, 'Activo')], 
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Seleccione el estado"}))
    
    class Meta:
        model = Post
        fields = ['titulo', 'descripcion', 'texto', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        instancia_modelo = kwargs.get('instance')
        valor_opcion_seleccionado = instancia_modelo.estado if instancia_modelo else None
        self.fields['estado'].initial = valor_opcion_seleccionado

        for key, field in self.fields.items():
            field.label = ""

class CrearCommentFormulario (forms.Form):
    texto = forms.CharField(max_length=500, 
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder" : "Commentario del Post"}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class EditarCommentFormulario (forms.ModelForm):
    texto = forms.CharField(max_length=500, 
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder" : "Commentario del Post"}))
    
    estado = forms.ChoiceField(
        choices=[(0, 'Inactivo'), (1, 'Activo')],
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Seleccione el estado"}))
    
    class Meta:
        model = Comment
        fields = ['texto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instancia_modelo = kwargs.get('instance')
        valor_opcion_seleccionado = instancia_modelo.estado if instancia_modelo else None
        self.fields['estado'].initial = valor_opcion_seleccionado
        
        for key, field in self.fields.items():
            field.label = ""

class RegistroUsuariosForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de Usuario"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repetir Contraseña"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class LoginUsuariosForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de Usuario"}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class UserEditForm(UserCreationForm):
    email = forms.EmailField(label="Modificar E-mail",  widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}))
    password2 = forms.CharField(label='Repetir la contraseña', widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repetir Contraseña"})) 
    first_name = forms.CharField(label="Nombre/s", max_length=50, required=False,  widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}))
    last_name = forms.CharField(label="Apellido/s", max_length=50, required=False,  widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"}))

    class Meta:
        model = User
        fields = [ 'email', 'password1', 'password2', 'first_name', 'last_name' ] 
        #Saca los mensajes de ayuda
        help_texts = { k:"" for k in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class AvatarFormulario(forms.Form):
    imagen = forms.ImageField(required=True,
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Seleccionar imagen"}))        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
        