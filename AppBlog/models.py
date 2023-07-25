from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Blog(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=500)
    portada = models.ImageField()
    fecha = models.DateTimeField()

class Post(models.Model):
    titulo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=500)
    texto = RichTextField()
    imagen = models.ImageField(default='NULL')
    link = models.TextField(default='NULL')
    fecha = models.DateTimeField()

class Comment(models.Model):
    texto = models.TextField()
    fecha = models.DateTimeField()