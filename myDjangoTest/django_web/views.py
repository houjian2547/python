from django.shortcuts import render
from django_web.models import BlogsPost
from django_web.models import second_url_film_name


# Create your views here.


def index(request):
    return render(request, 'index.html')


def blog_index(request):
    blog_list = BlogsPost.objects.all()
    return render(request, 'blog.html', {'blog_list': blog_list})


def film_show(request):
    # film_list = second_url_film_name.objects.all()
    # film_list = second_url_film_name.objects.filter(id__lt=15111, id__gt=15103)
    film_list = second_url_film_name.objects.filter(film_name__icontains='破门而入')
    return render(request, 'film.html', {'film_list': film_list})
