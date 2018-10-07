from django.contrib import admin
from .models import Post, App, PublicUsers, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    # Поле slug будет заполнено на основе поля title
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)
admin.site.register(App)
admin.site.register(PublicUsers)
admin.site.register(Comment)