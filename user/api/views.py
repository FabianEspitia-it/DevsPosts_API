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

TOKEN_NAME = "user_token"

token = False


class AllUsersAPIView(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UserViewSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        """
        response = Response()
        response.set_cookie(key=TOKEN_NAME, value=token, httponly=True)
        response.status_code = status.HTTP_202_ACCEPTED
        response.data = {
            "message": f"Hello {user.username}"
        }
        return response
        """
        return Response({
            "token" : token
        }, status=status.HTTP_202_ACCEPTED)

class UserViewAPIView(APIView):

    error_message = {"error": "user not found"}

    def get(self, request, pk):
        user = Users.objects.filter(id = pk).first()

        if user: 
            serializer = UserViewSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(self.error_message, status=status.HTTP_400_BAD_REQUEST)

class UsersLogoutAPIView(APIView):
    error_message = {"error": "you are not authenticated"}
    succesfully_message = {"message": "see you next time"}

    def post(self, request):
        token = request.COOKIES.get(TOKEN_NAME)
        if token is not None:
            response = Response()
            response.delete_cookie(self.token_name)
            response.data = self.succesfully_message
            response.status_code = status.HTTP_200_OK
            return response
        return Response(self.error_message, status=status.HTTP_400_BAD_REQUEST)