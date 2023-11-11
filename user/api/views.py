# PYTHON
import jwt
import datetime

# REST_FRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from devsposts.settings import SECRET_KEY

from user.api.serializers import UserRegisterSerializer, UsersLoginSerializer, UserViewSerializer

from db.models import Users


class UsersRegisterAPIView(APIView):
    message = {'message': 'User created succesfully'}

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.message, status=status.HTTP_201_CREATED)


class UsersLoginAPIView(APIView):

    def post(self, request):
        serializer = UsersLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        payload_content = {
            "email": request.data["email"],
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
            "iat": datetime.datetime.now()
        }
        token = jwt.encode(payload_content, SECRET_KEY, algorithm="HS256")

        user = Users.objects.filter(email= request.data["email"]).first()

        message = {
            "username": user.username,
            "token": token
        }


        return Response(message, status=status.HTTP_202_ACCEPTED)

class UserViewAPIView(APIView):

    error_message = {"error": "user not found"}

    def get(self, request, pk):
        user = Users.objects.filter(id = pk).first()

        if user: 
            serializer = UserViewSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(self.error_message, status=status.HTTP_400_BAD_REQUEST)