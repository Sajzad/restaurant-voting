from django.urls import path
from .views import (
    RegisterUserAPIView,
    LoginAPIView,
    LogoutView,
    CreateRestaurantAPIView,
    UploadMenuAPIView,
    CreateEmployeeAPIView,
    RestaurantList,
    TodayMenuList,
    VoteAPIView,
    ResultsAPIView

)

app_name = 'api'


urlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view(), name="register-user"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('create-restaurant/', CreateRestaurantAPIView.as_view(), name="create-restaurant"),
    path('upload_menu/', UploadMenuAPIView.as_view(), name="upload-menu"),
    path('create-employee/', CreateEmployeeAPIView.as_view(), name="create-employee"),
    path('vote/<int:menu_id>/', VoteAPIView.as_view(), name="vote"),
    path('results/', ResultsAPIView.as_view(), name="results"),
    path('restaurants/', RestaurantList.as_view(), name="restaurants"),
    path('menu-list/', TodayMenuList.as_view(), name="menu-list"),

]
