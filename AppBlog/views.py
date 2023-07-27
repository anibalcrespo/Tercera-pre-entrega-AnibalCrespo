from audioop import reverse
from django.shortcuts import redirect, render
from .forms import CrearBlogFormulario, CrearPostFormulario, CrearCommentFormulario
from datetime import datetime
from .models import *

# Create your views here.
def index(request):
    last_blogs = Blog.objects.all().order_by('-id')[:5]
    return render(request, "appblog/index.html", {'last_blogs' : last_blogs })

def about(request):
    return render(request, "appblog/about.html")

def allBlog(request):
    blogs = Blog.objects.all()
    return render(request, "appblog/allBlog.html", { 'blogs' : blogs})

def allPost(request, blog_id):
    posts = Post.objects.filter(blog_id=blog_id)
    blog = Blog.objects.get(id=blog_id)
    return render(request, "appblog/allPost.html", { 'posts' : posts, 'blog' : blog})

def blog(request, id):
    blog = Blog.objects.get(id=id)
    posts = Post.objects.filter(blog_id=id).order_by('-id')[:5]
    return render(request, "appblog/blog.html", {'blog' : blog, 'posts' : posts })

def post(request, id):
    post = Post.objects.get(id=id)
    blog = Blog.objects.get(id=post.blog_id)
    comments = Comment.objects.filter(post_id=id)
    return render(request, "appblog/post.html", {'post' : post, 'blog' : blog, 'comments' : comments })

def contact(request):
    return render(request, "appblog/contact.html")

def createBlogFormulario(request):
    if request.method == 'POST':
        miFormulario = CrearBlogFormulario(request.POST, request.FILES)
        if miFormulario.is_valid():
            nombre = miFormulario.cleaned_data.get('nombre')
            descripcion = miFormulario.cleaned_data.get('descripcion')
            portada = miFormulario.cleaned_data.get('portada')

            blog = Blog(nombre=nombre,
                        descripcion=descripcion,
                        portada=portada, 
                        fecha=datetime.now())
            blog.save()
            return redirect("blog", blog.id)

    else:
        miFormulario = CrearBlogFormulario()

    return render(request, "appblog/createBlog.html", {'miFormulario' : miFormulario})

def createPostFormulario(request, blog_id):
    if request.method == 'POST':
        miFormulario = CrearPostFormulario(request.POST, request.FILES)
        if miFormulario.is_valid():
            titulo = miFormulario.cleaned_data.get('titulo')
            descripcion = miFormulario.cleaned_data.get('descripcion')
            texto = miFormulario.cleaned_data.get('texto')
            imagen = miFormulario.cleaned_data.get('imagen')
            link = miFormulario.cleaned_data.get('link')

            post = Post(blog_id=blog_id,
                        titulo=titulo,
                        descripcion=descripcion,
                        texto=texto,
                        imagen=imagen, 
                        link=link,
                        fecha=datetime.now())
            post.save()
            return redirect("post", post.id)
    else:
        miFormulario = CrearPostFormulario()

    return render(request, "appblog/createPost.html", {'miFormulario' : miFormulario})

def createCommentFormulario(request, post_id):
    if request.method == 'POST':
        miFormulario = CrearCommentFormulario(request.POST)
        if miFormulario.is_valid():
            texto = miFormulario.cleaned_data.get('texto')

            comment = Comment(post_id=post_id,
                              texto=texto,
                              fecha=datetime.now())
            comment.save()
            return redirect("post", post_id)
    else:
        miFormulario = CrearCommentFormulario()
        post = Post.objects.get(id=post_id)
        blog = Blog.objects.get(id=post.blog_id)
        
    return render(request, "appblog/createComment.html", {'miFormulario' : miFormulario, 'blog' : blog })

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