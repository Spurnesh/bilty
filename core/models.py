import datetime
from django.db import models
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models import F

# Create your models here.

class Role(models.Model):
    """docstring for fees discount"""
    name = models.CharField(max_length=100)

    def get_nos(self):
        return NosName.objects.filter(role=self.id)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class NosName(models.Model):
    """docstring for fees discount"""
    name = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    role = models.ManyToManyField(Role, null=True, blank=True, default=None, related_name="role")
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)


class Bilty(models.Model):
    consignor = models.CharField(max_length=255)
    consignee = models.CharField(max_length=255)
    city = models.CharField(max_length=63)
    froms = models.CharField(max_length=100)
    to = models.CharField(max_length=100)
    bilty_number = models.IntegerField()
    truck_number = models.CharField(max_length=30)
    loading_date = models.DateTimeField(default=datetime.datetime.now())
    packages = models.CharField(max_length=100)
    weight = models.FloatField()


class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.IntegerField()
    bonus = models.IntegerField()


class Department(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee")
    name = models.CharField(max_length=100)