from django.shortcuts import render
from .forms import CrearBlogFormulario, CrearPostFormulario, CrearCommentFormulario
from datetime import datetime
from .models import *

# Create your views here.
def index(request):
    return render(request, "appblog/index.html")

def about(request):
    return render(request, "appblog/about.html")

def allBlog(request):
    blogs = Blog.objects.all()
    return render(request, "appblog/allBlog.html", { 'blogs' : blogs})

def allPost(request):
    posts = Post.objects.all()
    return render(request, "appblog/allPost.html", { 'posts' : posts})

def blog(request):
    return render(request, "appblog/blog.html")

def post(request):
    return render(request, "appblog/post.html")

def contact(request):
    return render(request, "appblog/contact.html")

def createBlogFormulario(request):
    if request.method == 'POST':
        miFormulario = CrearBlogFormulario(request.POST, request.FILES)
        print(miFormulario)
        if miFormulario.is_valid:
            nombre = miFormulario.cleaned_data.get('nombre')
            descripcion = miFormulario.cleaned_data.get('descripcion')
            portada = miFormulario.cleaned_data.get('portada')

            blog = Blog(nombre=nombre,
                        descripcion=descripcion,
                        portada=portada, 
                        fecha=datetime.now())
            blog.save()
            return render(request, "appblog/index.html") # Debe redirigir al nuevo blog
    else:
        miFormulario = CrearBlogFormulario()

    return render(request, "appblog/createBlog.html", {'miFormulario' : miFormulario})

def createPostFormulario(request):
    if request.method == 'POST':
        miFormulario = CrearPostFormulario(request.POST, request.FILES)
        print(miFormulario)
        if miFormulario.is_valid:
            titulo = miFormulario.cleaned_data.get('titulo')
            descripcion = miFormulario.cleaned_data.get('descripcion')
            texto = miFormulario.cleaned_data.get('texto')
            imagen = miFormulario.cleaned_data.get('imagen')
            link = miFormulario.cleaned_data.get('link')

            blog = Post(titulo=titulo,
                        descripcion=descripcion,
                        texto=texto,
                        imagen=imagen, 
                        link=link,
                        fecha=datetime.now())
            blog.save()
            return render(request, "appblog/index.html") # Tendria que llevarme a la portada del blog donde publique....
    else:
        miFormulario = CrearPostFormulario()

    return render(request, "appblog/createPost.html", {'miFormulario' : miFormulario})

def createCommentFormulario(request):
    if request.method == 'POST':
        miFormulario = CrearCommentFormulario(request.POST)
        print(miFormulario)
        if miFormulario.is_valid:
            texto = miFormulario.cleaned_data.get('texto')

            comment = Comment(texto=texto,
                        fecha=datetime.now())
            comment.save()
            return render(request, "appblog/index.html") # Tiene que redirigir al post donde comente
    else:
        miFormulario = CrearCommentFormulario()

    return render(request, "appblog/createComment.html", {'miFormulario' : miFormulario})

def buscarBlog(request):
    if request.GET['data']:
        data = request.GET['data']
        blogs = Blog.objects.filter(nombre__icontains=data)
        if blogs:
            return render(request, "appblog/resultadosBusqueda.html", {'blogs' : blogs })
        else:
            return render(request, "appblog/resultadosBusqueda.html", {'error' : "No se encontraron resultados."})  
    else:
        return render(request, "appblog/resultadosBusqueda.html", {'error' : "No ingresaste datos."})