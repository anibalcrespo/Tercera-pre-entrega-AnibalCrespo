from django.contrib import admin
from .models import Blog, Comment, Post, Avatar
  
# Register your models here.

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Avatar)