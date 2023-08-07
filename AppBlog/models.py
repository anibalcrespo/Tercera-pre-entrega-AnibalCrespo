from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=500)
    portada = models.ImageField(upload_to='uploads/')
    fecha = models.DateTimeField(default=datetime.now())
    visibilidad = models.IntegerField(default=0)  # 0 - publico (usuarios no autenticados acceden)
                                                  # 1 - restringido (usuarios autenticated acceden)
                                                  # 2 - Privado (autenticated solo el autor) 

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=False)
    titulo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=500)
    texto = RichTextField(default=None)
    imagen = models.ImageField(default=None, upload_to='uploads/')
    link = models.TextField(default=None)
    fecha = models.DateTimeField(default=datetime.now())
    estado = models.IntegerField(default=1) # 0 - Inactivo
                                            # 1 - Activo

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    texto = models.TextField(default=None)
    fecha = models.DateTimeField(default=datetime.now())
    estado = models.IntegerField(default=1) # 0 - Inactivo
                                            # 1 - Activo

class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.user} [{self.imagen}]"