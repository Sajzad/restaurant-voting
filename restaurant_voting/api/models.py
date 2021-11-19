import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    """Represents user class model"""
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username

class Employee(models.Model):
    """Represents employee class model"""

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Restaurant(models.Model):
    """Represents restaurant class model"""
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    contact_no = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

class Menu(models.Model):
    """Represents menu class model"""
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE)
    file = models.FileField(upload_to='menus/')
    created_at = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.restaurant.name


class Vote(models.Model):
    """Represents vote class model"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee}'
