from rest_framework import serializers

from api.models import *
from api.serializers import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone'
        ]


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone'
        ]


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        fields = [
            'username',
            'password',
        ]

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = [
            'user'
        ]
class CreateRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = [
            'name',
            'contact_no',
            'address'
        ]

class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class ResultMenuListSerializer(serializers.ModelSerializer):

    restaurant = serializers.CharField(read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id',
            'file',
            'restaurant',
            'votes',
            'created_at'
        ]
