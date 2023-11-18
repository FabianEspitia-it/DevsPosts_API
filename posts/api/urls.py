from django.urls import path

from posts.api.views import *

urlpatterns = [
    path("", AllPostAPIView.as_view(), name= "all_posts"),
    path("create-post/", CreatePostAPIView.as_view(), name="create_post"),
    path("delete-post/<int:pk>", DeletePostAPIView.as_view(), name= "delete_post")
]
