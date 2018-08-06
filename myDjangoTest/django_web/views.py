from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

from django_web.models import BlogsPost
from django_web.models import second_url_film_name
import json
from django.http import JsonResponse
from django.db import connection


def index(request):
    return render(request, 'index.html')


def pass_page(request):
    pass


def blog_index(request):
    blog_list = BlogsPost.objects.all()
    return render(request, 'blog.html', {'blog_list': blog_list})


def film_show(request):
    # film_list = second_url_film_name.objects.all()
    # film_list = second_url_film_name.objects.filter(id__lt=2610, id__gt=2600)
    # print(film_list)
    # dataname = request.GET.get('dataname', '')
    # print(dataname)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id,film_name,type_code,download_ftp_url FROM django_web_second_url_film_name limit 10")
        film_list = cursor.fetchall()
        cursor.close()
        film_object_list = []
        for film in film_list:
            film_object = second_url_film_name()
            film_object.id = film[0]
            film_object.film_name = film[1]
            film_object.type_code = film[2]
            film_object.download_ftp_url = film[3]
            film_object_list.append(film_object)
    print(film_object_list)
    SearchStatus = "Success"
    SearchResult = film_object_list
    return render(request, 'film.html', {"SearchResult": SearchResult, "SearchStatus": SearchStatus})


def film_name_search(request):
    filmName = request.GET.get('filmName', '')
    print('search film name:' + filmName)
    global film_list
    if filmName:
        print('filmName is not empty')
        # with connection.cursor() as cursor:
        #     sql = "SELECT id,film_name,download_ftp_url FROM django_web_second_url_film_name where film_name like '%" + filmName + "%' limit 10"
        #     print(sql)
        #     cursor.execute(sql)
        #     film_list = cursor.fetchall()
        #     cursor.close()
        film_list = second_url_film_name.objects.filter(film_name__icontains=filmName)
    else:
        print('filmName is empty')
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT id,film_name,download_ftp_url FROM django_web_second_url_film_name limit 10")
        #     film_list = cursor.fetchall()
        #     cursor.close()
        film_list = second_url_film_name.objects.filter(id__lt=2610, id__gt=2600)
    film_list = serializers.serialize("json", film_list)
    film_list = json.dumps(film_list)
    # film_object_list = []
    # for film in film_list:
    #     film_object = second_url_film_name()
    #     film_object.id = film[0]
    #     film_object.film_name = film[1]
    #     film_object.download_ftp_url = film[2]
    #     film_object_list.append(film_object)
    # print(film_object_list)
    print(film_list)
    return HttpResponse(film_list, content_type='application/json')
