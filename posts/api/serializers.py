import datetime

from rest_framework import serializers

from db.models import Post, Technology


class AllPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ['deleted_at']


    def to_representation(self, instance):

        tech = Technology.objects.filter(id= instance.technology_id).first()
        return{
            "title": instance.title,
            "content": instance.content,
            "likes": instance.likes,
            "technology": tech.title,
            "created_at": instance.created_at,
            "user": instance.user
        }

class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    technology = serializers.CharField(max_length=100)    

    def create(self, validated_data):
        
        tech_info = Technology.objects.filter(title=validated_data["technology"]).first()

        if not tech_info:
            tech_info = Technology.objects.create(title=validated_data["technology"])
            

        post = Post.objects.create(
            title= validated_data["title"],
            content= validated_data["content"],
            created_at= datetime.datetime.now(),
            technology_id= tech_info.id,
            likes = 0

        )

        return post
