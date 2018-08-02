from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class BlogsPost(models.Model):
    title = models.CharField(max_length=150)  # 博客标题
    body = models.TextField()  # 博客正文
    timestamp = models.DateTimeField()  # 创建时间

class second_url_film_name(models.Model):
    id = models.BigIntegerField
    film_name = models.CharField(max_length=150)
    download_ftp_url = models.CharField(max_length=150)


