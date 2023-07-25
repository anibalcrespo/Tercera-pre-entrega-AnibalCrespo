from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name="index"), #index muestra ultimos blogs
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
    path('allblog/', allBlog, name="allblog"), # muestra listado de todos los blogs
    path('allpost/', allPost, name="allpost"), # muestra listado de todos los post de un blog particular
    path('blog/', blog, name="blog"), # muestra un blog particular y los ultimos posts
    path('post/', post, name="post"), # muestra un post particular y todos sus comentarios
    
    path('createBlogFormulario/', createBlogFormulario, name="createBlog"), # fomulario para crear un blog
    path('createPostFormulario/', createPostFormulario, name="createPost"), # fomulario para crear un post  
    path('createCommentFormulario/', createCommentFormulario, name="createComment"), # fomulario para crear un comentario

    path('buscarBlog/', buscarBlog, name="buscarBlog"), # fomulario para buscar blogs
        
]
