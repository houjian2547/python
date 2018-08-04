from django.contrib import admin

# Register your models here.


from django.contrib import admin
from django_web.models import BlogsPost
from django_web.models import second_url_film_name


# Register your models here.
class BlogsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'timestamp']

class FilmShowAdmin(admin.ModelAdmin):
    list_display = ['id', 'film_name', 'download_ftp_url']

admin.site.register(BlogsPost, BlogsPostAdmin)

admin.site.register(second_url_film_name, FilmShowAdmin)
