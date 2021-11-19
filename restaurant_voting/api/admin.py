from django.contrib import admin

# Register your models here.
from .models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at',
    )


class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'contact_no',
        'address',
        'created_at',
    )


class MenuAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'restaurant',
        'file',
        'votes',
        'created_at',
        'created'
    )


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'menu', 'voted_at')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Vote, VoteAdmin)
