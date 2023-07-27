from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Blog(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=500)
    portada = models.ImageField(upload_to='uploads/')
    fecha = models.DateTimeField()

class Post(models.Model):
    blog_id = models.BigIntegerField(default='NULL')
    titulo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=500)
    texto = RichTextField()
    imagen = models.ImageField(default='NULL', upload_to='uploads/')
    link = models.TextField(default='NULL')
    fecha = models.DateTimeField()

class Comment(models.Model):
    post_id = models.BigIntegerField(default="NULL")
    texto = models.TextField()
    fecha = models.DateTimeField()