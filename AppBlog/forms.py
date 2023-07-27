from django import forms
from ckeditor.widgets import CKEditorWidget

class CrearBlogFormulario (forms.Form):
    nombre = forms.CharField(max_length=250, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Nombre del Blog"}))
    
    descripcion = forms.CharField(max_length=500, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder" : "Descripcion del Blog"}))
    
    portada = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder" : "Portada"}))

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

class CrearCommentFormulario (forms.Form):
    texto = forms.CharField(max_length=500, 
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder" : "Commentario del Post"}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""