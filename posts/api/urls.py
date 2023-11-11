from django.urls import path

from posts.api.views import CreatePostAPIView, AllPostAPIView

urlpatterns = [
    path("", AllPostAPIView.as_view(), name= "all_posts"),
    path("create-post", CreatePostAPIView.as_view(), name="create_post")
]
