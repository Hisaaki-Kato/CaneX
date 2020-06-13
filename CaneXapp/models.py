from django.db import models
from django_mysql.models import ListCharField

class Patient(models.Model):
    name = models.CharField(blank=True, max_length=100)
    site = models.CharField(blank=True, max_length=10)
    p_TNM = models.CharField(blank=True, max_length=10)
    number = models.IntegerField(blank=False, null=False, default=0)

class Sharp(models.Model):
    name = models.CharField(blank=True, max_length=10)
    vectors = models.TextField(blank=False, null=False)

