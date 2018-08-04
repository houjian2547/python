from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

from django_web.models import BlogsPost
from django_web.models import second_url_film_name
import json
from django.http import JsonResponse


# Create your views here.


def index(request):
    return render(request, 'index.html')


def blog_index(request):
    blog_list = BlogsPost.objects.all()
    return render(request, 'blog.html', {'blog_list': blog_list})


def film_show(request):
    # film_list = second_url_film_name.objects.all()
    # film_list = second_url_film_name.objects.filter(id__lt=15111, id__gt=15103)
    dataname = request.GET.get('dataname', '')
    print(dataname)
    global film_list
    if dataname:
        print('not empty')
        film_list = second_url_film_name.objects.filter(film_name__icontains=dataname)
    else:
        print('empty')
        film_list = second_url_film_name.objects.filter(id__lt=15111, id__gt=15103)
    for film in film_list:
        print(film.film_name)
    return render(request, 'film.html', {'film_list': film_list})


def film_name_search(request):
    filmName = request.GET.get('filmName', '')
    print(filmName)
    global film_list
    if filmName:
        print('filmName is not empty')
        film_list = second_url_film_name.objects.filter(film_name__icontains=filmName)
    else:
        print('filmName is empty')
        film_list = second_url_film_name.objects.filter(id__lt=15111, id__gt=15103)

    content_list = []
    for film in film_list:
        print(film.film_name)
        # context = {'id': film.id, 'film_name': film.film_name, 'download_ftp_url': film.download_ftp_url}
        content_list.append(film)

    film_list = serializers.serialize("json", content_list)
    film_list = json.dumps(film_list)
    # response = HttpResponse()
    # response['Content-Type'] = "application/json"
    # response.write(film_list)
    # return HttpResponse(film_list)

    return HttpResponse(film_list, content_type='application/json')
