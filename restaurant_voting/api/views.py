from datetime import datetime
from datetime import date, timedelta

from django.conf import settings
from django.template import loader
from django.utils.html import strip_tags
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import *
from api.serializers import *

from .custom_jwt import (
    jwt_payload_handler,
    jwt_encode_handler,
    jwt_decode_handler
)

class RegisterUserAPIView(APIView):

    def post(self, request, format=None):
        req = request.data
        serializer = UserSerializer(data=req)
        if serializer.is_valid():
            try:
                new_user = User.objects.create(
                    username=req.get('username'),
                    email=req.get('email'),
                    first_name=req.get('first_name').capitalize(),
                    last_name=req.get('last_name').capitalize(),
                    is_active=True,
                    phone=req.get('phone'),
                    # identification_no=req.get('identification_no'),
                    is_staff=True

                )

                password = User.objects.make_random_password(length=10)
                new_user.set_password(password)
                new_user.save()

                login_site = settings.LOGIN_REDIRECT_URL

                creds = {
                    "username": new_user.username,
                    "password": password,
                    "link": "/api/login/",
                    'user_email': new_user.email
                }

                serializer = UserSerializer(new_user)
                ser = UserDetailSerializer(new_user)
                text = 'Check your email for login information'
                res = {
                    "msg": f"Successfully registered.{text}",
                    "data": ser.data,
                    "credentials": creds,
                    "success": True}
                return Response(data=res, status=status.HTTP_201_CREATED)
            except Exception as e:
                res = {"msg": str(e), "data": None, "success": False}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = {"msg": str(serializer.errors), "data": None, "success": False}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        try:
            if check_password(request.data["password"], user.password):
                payload = jwt_payload_handler(user)

                token = jwt_encode_handler(payload)

                fullname = user.first_name + " " + user.last_name
                res = {
                    "msg": "Login success",
                    "success": True,
                    "data": {
                        "name": fullname,
                        "username": user.username,
                        "token": token
                        }
                    }
                return Response(data=res, status=status.HTTP_200_OK)

            else:
                res = {
                    "msg": "Invalid login credentials",
                    "data": None,
                    "success": False}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            res = {"msg": str(e), "success": False, "data": None}
            return Response(data=res, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            username = jwt_decode_handler(request.auth).get('username')
            user = User.objects.get(username=username)
            payload = jwt_payload_handler(user)
            jwt_encode_handler(payload)
            res = {
                "msg": "User logged out successfully",
                "success": True,
                "data": None}
            return Response(data=res, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CreateEmployeeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        req = request.data
        user = jwt_decode_handler(request.auth)

        employee = Employee.objects.filter(user__username=user.get('username'))
        text = f"EMPLOYEE NO { user.get('username') } already exists"
        if employee.exists():
            res = {
                "msg": text,
                "data": None,
                "success": False}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(data=req)

        if serializer.is_valid():
        	try:
        		user_obj = User.objects.filter(username=user.get('username'))
        		if user_obj.exists():
        			user_id = user_obj[0].id
        			Employee.objects.create(user_id=user_id)
        			res = {
						"msg": "Employee successfully created",
					    "data": {
					    	"username":user.get("username"),
					    	"email":user.get("email"),
					    	"first_name":user.get("first name"),
					    	"last_name":user.get("last name"),
					    	"full_name":user.get("full_name")
					    },
					    "success": True}
        	except Exception as e:
        		res = {"msg": str(e), "data": None, "success": False}
        		return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        	return Response(data=res, status=status.HTTP_201_CREATED)

        res = {"msg": str(serializer.errors), "data": None, "success": False}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

class CreateRestaurantAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        req = request.data
        serializer = CreateRestaurantSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
            res = {
                "msg": "Restaurant Created",
                "success": True,
                "data": serializer.data}
            return Response(data=res, status=status.HTTP_201_CREATED)

        res = {"msg": str(serializer.errors), "success": False, "data": None}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

class UploadMenuAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            req = request.data
            todays_date = date.today()
            menu = Menu.objects.filter(
                restaurant__name=req.get('restaurant'),
                created_at__date=todays_date)

            user = jwt_decode_handler(request.auth).get('username')

            if menu.exists():
                res = {
                    "msg": "Menu already added.",
                    "success": False,
                    "data": None}
                return Response(data=res, status=status.HTTP_200_OK)
            try:    
                restaurant_obj = get_object_or_404(Restaurant, name=req.get('restaurant'))
                Menu.objects.create(
                    restaurant=restaurant_obj,
                    file = request.FILES['file']
                    )
                res = {
                    "message": "Restaurant is created",
                    "restaurant name": req.get('restaurant'),
                    "success":True
                }

                return Response(data=res, status=status.HTTP_201_CREATED)
            except Exception as e:
                res = {
                    "msg": str(e),
                    "success": False,
                    "data": None}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = {"msg": str(e), "success": False, "data": None}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

class TodayMenuList(APIView):

    def get(self, request):

        menu_qs = Menu.objects.filter(Q(created_at__date=date.today()))
        serializer = MenuListSerializer(menu_qs, many=True)
        res = {"msg": 'success', "data": serializer.data, "success": True}
        return Response(data=res, status=status.HTTP_200_OK)


class RestaurantList(generics.ListAPIView):
    serializer_class = RestaurantListSerializer
    queryset = Restaurant.objects.all()

class VoteAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    todays_date = date.today()

    def post(self, request, menu_id):
        try:
            username = jwt_decode_handler(request.auth).get('username')
            todays_date = date.today()

            employee = Employee.objects.get(user__username=username)
            menu = Menu.objects.get(id=menu_id)

            if Vote.objects.filter(
                    employee__user__username=username,
                    voted_at__date=todays_date,
                    menu__id=menu_id).exists():
                res = {"msg": 'You already voted!', "data": None, "success": False}
                return Response(data=res, status=status.HTTP_200_OK)
            else:
                Vote.objects.create(
                    employee=employee,
                    menu=menu

                )
                menu.votes += 1
                menu.save()

                qs = Menu.objects.filter(created_at__date=todays_date)
                
                res = {
                    "msg": 'You voted successfully!',
                    "data":None,
                    "success": True}
                return Response(data=res, status=status.HTTP_200_OK)
        except Exception as e:
            res = {"msg": str(e), "data": None, "success": False}
            return Response(data=res, status=status.HTTP_200_OK)


class ResultsAPIView(APIView):

    def get(self, request):
        today = date.today()
        last_3_days = today - timedelta(days=3)
        start = today - timedelta(days=today.weekday())
        current_menu_qs = Menu.objects.filter(created__date__gte = last_3_days)
        if len(current_menu_qs) == 0:
            res = {
                "msg": 'Results not found for today!',
                "data": None,
                "success": False}
            return Response(data=res, status=status.HTTP_200_OK)
        previous_restaurants = []
        try:
            for day_count in range(1,4):
                pre_results = current_menu_qs.filter(
                    created_at__date = today - timedelta(days = day_count)
                    ).order_by('-votes')
                if pre_results:
                    previous_restaurants.append(pre_results[0].restaurant_id)
            todays_result = current_menu_qs.filter(
                created_at__date=today).exclude(
                restaurant_id__in = previous_restaurants).order_by('-votes')
            if len(todays_result) == 0:
                res = {
                    "msg": 'Results not found for today!',
                    "data": None,
                    "success": False}
                return Response(data=res, status=status.HTTP_200_OK)
            else:
                result = {
                        "rank": 1,
                        "votes": todays_result[0].votes,
                        "restaurant": todays_result[0].restaurant.name,
                        "menu_url": todays_result[0].file.url}

                res = {"msg": 'success', "data": result, "success": True}
                return Response(data=res, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(e)
            res = {"msg": str(e), "success": False, "data": None}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
