from django.urls import path, include
from .views import *

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name="index"), #index muestra ultimos blogs
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
    path('allblog/', allBlog, name="allblog"), # muestra listado de todos los blogs
    path('allpost/<blog_id>/', allPost, name="allpost"), # muestra listado de todos los post de un blog particular
    path('blog/<id>/', blog, name="blog"), # muestra un blog particular y los ultimos posts
    path('post/<id>/', post, name="post"), # muestra un post particular y todos sus comentarios
    
    path('createBlogFormulario/', createBlogFormulario, name="createBlog"), # fomulario para crear un blog
    path('createPostFormulario/<blog_id>/', createPostFormulario, name="createPost"), # fomulario para crear un post  
    path('createCommentFormulario/<post_id>/', createCommentFormulario, name="createComment"), # fomulario para crear un comentario
    path('EditarPostFormulario/<post_id>/', editarPostFormulario, name="editPost"), # fomulario para editar un post
    path('EditarBlogFormulario/<blog_id>/', editarBlogFormulario, name="editBlog"), # fomulario para editar un blog
    path('EditarCommentFormulario/<comment_id>/', editarCommentFormulario, name="editComment"), # fomulario para editar un Commentario
    path('EliminarBlog/<blog_id>/', eliminarBlog, name="deleteBlog"), # Elimina el blog
    path('EliminarPost/<post_id>/', eliminarPost, name="deletePost"), # Elimina el post
    path('EliminarComment/<comment_id>/', eliminarComment, name="deleteComment"), # Elimina el comment

    path('buscarBlog/', buscarBlog, name="buscarBlog"), # fomulario para buscar blogs
    
    path('login/', login_request, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', register, name="register"),

    path('editar_perfil/', editarPerfil, name="editar_perfil"),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"),    
]
