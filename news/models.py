from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    admin_level = models.PositiveIntegerField()
    password = models.CharField(max_length=30)
    login = models.CharField(max_length=30, unique=True)
    token = models.CharField(max_length=30, unique=True)


class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    date = models.DateField()
