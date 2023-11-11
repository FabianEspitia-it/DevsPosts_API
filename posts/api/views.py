# REST_FRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from posts.api.serializers import CreatePostSerializer, AllPostSerializer

from db.models import Post

class CreatePostAPIView(APIView):
    message = {"message": "post created succesfully"}

    def post(self, request):
        serializer = CreatePostSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.message, status=status.HTTP_201_CREATED)

class AllPostAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = AllPostSerializer(posts, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)

