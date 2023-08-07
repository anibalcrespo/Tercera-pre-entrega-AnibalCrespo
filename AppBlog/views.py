from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .forms import *
from datetime import datetime
from .models import *

from django.http import HttpResponseRedirect

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    if request.user.is_authenticated:
        # publicos, restrigidos y privados mios (si soy yo quien esta logueado) 
        last_blogs = Blog.objects.filter(visibilidad__in=[0,1]).union(Blog.objects.filter(visibilidad=2, user_id=request.user.id)).order_by('-id')[:5] 
    else:
        # publicos
        last_blogs = Blog.objects.filter(visibilidad=0).order_by('-id')[:5]
    
    return render(request, "appblog/index.html", {'last_blogs' : last_blogs })

def about(request):
    return render(request, "appblog/about.html")

def contact(request):
    return render(request, "appblog/contact.html")

def allBlog(request):
    if request.user.is_authenticated:
        # publicos, restrigidos y privados mios (si soy yo quien esta logueado) 
        blogs = Blog.objects.filter(visibilidad__in=[0,1]).union(Blog.objects.filter(visibilidad=2, user_id=request.user.id)) 
    else:
        blogs = Blog.objects.filter(visibilidad=0) #publicos

    return render(request, "appblog/allBlog.html", { 'blogs' : blogs})

def blog(request, id):

    blog = Blog.objects.get(id=id)

    if request.user.is_authenticated:

        # el blog es mio
        if blog.user_id == request.user.id:
            # traigo ultimos 5 posts 
            posts = Post.objects.filter(blog_id=id).order_by('-id')[:5]
        # no es publico y no restringido    
        elif blog.visibilidad not in [0,1]:
            return allBlog(request)
        else:
            # traigo ultimos 5 posts activos
            posts = Post.objects.filter(blog_id=id, estado=1).order_by('-id')[:5]
    # es restringido o privado
    elif blog.visibilidad in [1,2]: 
        return allBlog(request)
    else:
        posts = Post.objects.filter(blog_id=id, estado=1).order_by('-id')[:5]
    
    # renderiza y muestra
    return render(request, "appblog/blog.html", {'blog' : blog, 'posts' : posts })

def allPost(request, blog_id):

    blog = Blog.objects.get(id=blog_id)

    if request.user.is_authenticated:

        # el blog es mio
        if blog.user_id == request.user.id:
            # traigo todos posts
            posts = Post.objects.filter(blog_id=blog_id).order_by('id')
        # no es publico y no restringido    
        elif blog.visibilidad not in [0,1]:
            return allPost(request, blog_id)
        else:
            # traigo todos posts activos
            posts = Post.objects.filter(blog_id=blog_id, estado=1).order_by('id')
    
    # es restringido o privado
    elif blog.visibilidad in [1,2]: 
        return allPost(request, blog_id)
    else:
        posts = Post.objects.filter(blog_id=blog_id, estado=1).order_by('id')
    
    # renderiza y muestra
    return render(request, "appblog/allPost.html", {'blog' : blog, 'posts' : posts })

def post(request, id):

    post = Post.objects.get(id=id)

    if request.user.is_authenticated:

        # el post es de mi blog
        if post.user_id == request.user.id:
            blog = Blog.objects.get(id=post.blog_id)
            comments = Comment.objects.filter(post_id=id)
            pass
        # esta inactivo 
        elif post.estado == 0:
            return allPost(request, post.blog_id)
        else:
           blog = Blog.objects.get(id=post.blog_id)
           comments = Comment.objects.filter(post_id=id)
           pass
    
    # esta inactivo
    elif post.estado == 0: 
        return allBlog(request)
    else:
        blog = Blog.objects.get(id=post.blog_id)
        comments = Comment.objects.filter(post_id=id)
        pass

    # renderiza y muestra
    return render(request, "appblog/post.html", {'blog' : blog, 'post' : post, 'comments' : comments })

@login_required(login_url="login")
def createBlogFormulario(request):
    if request.method == 'POST':
        miFormulario = CrearBlogFormulario(request.POST, request.FILES)
        if miFormulario.is_valid():
            nombre = miFormulario.cleaned_data.get('nombre')
            descripcion = miFormulario.cleaned_data.get('descripcion')
            portada = miFormulario.cleaned_data.get('portada')
            visibilidad = miFormulario.cleaned_data.get('visibilidad')
            blog = Blog(user_id=request.user.id,
                        nombre=nombre,
                        descripcion=descripcion,
                        portada=portada,
                        visibilidad=visibilidad)
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

            post = Post(user_id=request.user.id,
                        blog_id=blog_id,
                        titulo=titulo,
                        descripcion=descripcion,
                        texto=texto,
                        imagen=imagen, 
                        link=link)
            post.save()
            return redirect("post", post.id)
    else:
        blog = Blog.objects.get(id=blog_id)
        # autenticado
        if request.user.is_authenticated:
            if blog.visibilidad == 0: #publico
                pass
            elif blog.visibilidad == 1: #restringido
                pass
            elif blog.visibilidad == 2 and blog.user.id == request.user.id: #privado mio
                pass
            else:
                login_request(request)
        else:
            if blog.visibilidad == 0: #publico
                pass
            elif blog.visibilidad == 1: #restringido
                login_request(request)
            elif blog.visibilidad == 2: #privado
                login_request(request)
            else:
                pass

        miFormulario = CrearPostFormulario()

    return render(request, "appblog/createPost.html", {'miFormulario' : miFormulario})

def createCommentFormulario(request, post_id):
    if request.method == 'POST':
        miFormulario = CrearCommentFormulario(request.POST)
        if miFormulario.is_valid():
            texto = miFormulario.cleaned_data.get('texto')

            comment = Comment(user_id=request.user.id,
                              post_id=post_id,
                              texto=texto)
            comment.save()
            return redirect("post", post_id)
    else:
        miFormulario = CrearCommentFormulario()
        post = Post.objects.get(id=post_id)
        blog = Blog.objects.get(id=post.blog_id)

        # autenticado (blog privado y yo)
        if request.user.is_authenticated:
            if blog.visibilidad == 0: #publico
                pass
            elif blog.visibilidad == 1: #restringido
                pass
            elif blog.visibilidad == 2 and blog.user.id == request.user.id: #privado mio
                pass
            else:
                login_request(request)
        else:
            if blog.visibilidad == 0: #publico
                pass
            elif blog.visibilidad == 1: #restringido
                login_request(request)
            elif blog.visibilidad == 2: #privado
                login_request(request)
            else:
                pass
        
    return render(request, "appblog/createComment.html", {'miFormulario' : miFormulario, 'blog' : blog })

def editarBlogFormulario(request, blog_id):
    if request.method == 'POST':
        miFormulario = EditarBlogFormulario(request.POST, request.FILES)
        if miFormulario.is_valid():
            nombre = miFormulario.cleaned_data.get('nombre')
            descripcion = miFormulario.cleaned_data.get('descripcion')
            portada = miFormulario.cleaned_data.get('portada')
            visibilidad = miFormulario.cleaned_data.get('visibilidad')

            blog = Blog.objects.get(id=blog_id)
            
            blog.user_id=request.user.id
            blog.nombre=nombre
            blog.descripcion=descripcion
            blog.portada=portada
            blog.visibilidad=visibilidad
            
            blog.save()

            return redirect("blog", blog.id)
    else:
        blog = Blog.objects.get(id=blog_id)

        miFormulario = EditarBlogFormulario(instance=blog)
        
        # autenticado 
        if request.user.is_authenticated:
            if blog.user.id == request.user.id: # Si es mio
                pass
            else:
                login_request(request)
        else:
            login_request(request)
            
    return render(request, "appblog/editBlog.html", {'miFormulario' : miFormulario})

def editarPostFormulario(request, post_id):
    if request.method == 'POST':
        miFormulario = EditarPostFormulario(request.POST, request.FILES)
        if miFormulario.is_valid():
            titulo = miFormulario.cleaned_data.get('titulo')
            descripcion = miFormulario.cleaned_data.get('descripcion')
            texto = miFormulario.cleaned_data.get('texto')
            imagen = miFormulario.cleaned_data.get('imagen')
            link = miFormulario.cleaned_data.get('link')
            estado = miFormulario.cleaned_data.get('estado')

            post = Post.objects.get(id=post_id)
            
            post.user_id=request.user.id
            post.titulo=titulo
            post.descripcion=descripcion
            post.texto=texto
            post.imagen=imagen
            post.link=link
            post.estado=estado
            
            post.save()

            return redirect("post", post.id)
    else:
        post = Post.objects.get(id=post_id)
        blog = post.blog

        miFormulario = EditarPostFormulario(instance=post)
        
        # autenticado 
        if request.user.is_authenticated:
            if blog.user.id == request.user.id: # Si es mio
                pass
            else:
                login_request(request)
        else:
            login_request(request)
            
    return render(request, "appblog/editPost.html", {'miFormulario' : miFormulario})

def editarCommentFormulario(request, comment_id):
    if request.method == 'POST':
        miFormulario = EditarCommentFormulario(request.POST)
        if miFormulario.is_valid():
            texto = miFormulario.cleaned_data.get('texto')
            estado = miFormulario.cleaned_data.get('estado')

            comment = Comment.objects.get(id=comment_id)
            
            comment.user_id=request.user.id
            comment.texto=texto
            comment.estado=estado
            
            comment.save()

            return redirect("post", comment.id)
    else:
        comment = Comment.objects.get(id=comment_id)
        blog = comment.post.blog

        miFormulario = EditarCommentFormulario(instance=comment)
        
        # autenticado 
        if request.user.is_authenticated:
            if blog.user.id == request.user.id: # Si es mio
                pass
            else:
                login_request(request)
        else:
            login_request(request)
            
    return render(request, "appblog/editComment.html", {'miFormulario' : miFormulario})

def buscarBlog(request):
    if request.GET['data']:
        data = request.GET['data']
        
        if request.user.is_authenticated:
            # publicos, restrigidos y privados mios (si soy yo quien esta logueado) 
            blogs = Blog.objects.filter(nombre__icontains=data, visibilidad__in=[0,1]).union(Blog.objects.filter(nombre__icontains=data, visibilidad=2, user_id=request.user.id)) 
        else:
            blogs = Blog.objects.filter(nombre__icontains=data, visibilidad=0) #publicos

        if blogs:
            return render(request, "appblog/resultadosBusqueda.html", {'blogs' : blogs })
        else:
            return render(request, "appblog/resultadosBusqueda.html", {'error' : "No se encontraron resultados."})  
    else:
        return render(request, "appblog/resultadosBusqueda.html", {'error' : "No ingresaste datos."})
    
def login_request(request):
    if request.method == "POST":
        miForm = LoginUsuariosForm(request, data=request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            clave = miForm.cleaned_data.get('password')
            user = authenticate(username=usuario, password=clave)
            if user is not None:
                login(request, user)

                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = '/media/avatares/default.png'
                finally:
                    request.session['avatar'] = avatar

                return index(request) # forware dentro de otra view
            else:
                return render(request, "appblog/login.html", {"form":miForm, "mensaje": "Datos Inválidos"})
        else:    
            return render(request, "appblog/login.html", {"form":miForm, "mensaje": "Datos Inválidos"})

    miForm = LoginUsuariosForm()

    return render(request, "appblog/login.html", {"form":miForm})    

def register(request):
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST) # UserCreationForm 
        if form.is_valid():  # Si pasó la validación de Django
            usuario = form.cleaned_data.get('username')
            form.save()
            return render(request, "appblog/index.html", {"mensaje":"Usuario Creado"})        
    else:
        form = RegistroUsuariosForm() # UserCreationForm 

    return render(request, "appblog/registro.html", {"form": form})

@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            usuario.email = form.cleaned_data.get('email')
            usuario.password1 = form.cleaned_data.get('password1')
            usuario.password2 = form.cleaned_data.get('password2')
            usuario.first_name = form.cleaned_data.get('first_name')
            usuario.last_name = form.cleaned_data.get('last_name')
            usuario.save()
            return render(request, "appblog/index.html", {'mensaje': f"Usuario {usuario.username} actualizado correctamente"})
        else:
            return render(request, "appblog/editarPerfil.html", {'form': form})
    else:
        form = UserEditForm(instance=usuario)
    return render(request, "appblog/editarPerfil.html", {'form': form, 'usuario':usuario.username})

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarFormulario(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            #_________________ Esto es para borrar el avatar anterior
            avatarViejo = Avatar.objects.filter(user=u)
            if len(avatarViejo) > 0: # Si esto es verdad quiere decir que hay un Avatar previo
                avatarViejo[0].delete()

            #_________________ Grabo avatar nuevo
            avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
            avatar.save()

            #_________________ Almacenar en session la url del avatar para mostrarla en base
            imagen = Avatar.objects.get(user=request.user.id).imagen.url
            request.session['avatar'] = imagen

            return render(request, "appblog/index.html")
    else:
        form = AvatarFormulario()
    return render(request, "appblog/agregarAvatar.html", {'form': form})

@login_required
def eliminarComment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post_id = comment.post.id
    comment.delete()
    return  redirect(reverse_lazy('post', args=[post_id]))

@login_required
def eliminarPost(request, post_id):
    post = Post.objects.get(id=post_id)
    blog_id = post.blog.id
    post.delete() 
    return redirect(reverse_lazy('blog', args=[blog_id]))
@login_required

def eliminarBlog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect(reverse_lazy('index'))