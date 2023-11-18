from django.urls import path

from user.api.views import *

urlpatterns = [
    path('register/', UsersRegisterAPIView.as_view(), name = 'register'),
    path('login/', UsersLoginAPIView.as_view(), name = 'login' ),
    path('logout/', UsersLogoutAPIView.as_view(), name= 'logout'),
    path('user-info/', AllUsersAPIView.as_view(), name = 'all_user_info'),
    path('user-info/<int:pk>', UserViewAPIView.as_view(), name='user_info')
    ]
