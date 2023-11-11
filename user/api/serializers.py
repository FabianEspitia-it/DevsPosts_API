from rest_framework import serializers

from db.models import Users


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length= 100)
    email = serializers.CharField(max_length = 100)
    userpassword = serializers.CharField(max_length=200)
    confirmpassword = serializers.CharField(max_length = 200)
    country = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=100)

    def validate(self, data):
        if data["userpassword"] != data["confirmpassword"]:
            raise serializers.ValidationError("Passwords do not match")
        return data 

    def create(self, validated_data):
        validated_data.pop("confirmpassword")
        user = Users.objects.create(
            username=validated_data["username"], 
            email=validated_data["email"],
            phone= validated_data["phone"]
        ),
        user.set_password(validated_data["userpassword"])
        user.save()
        return user


class UsersLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    userpassword = serializers.CharField(max_length=200)

    def validate(self, data):
        user = Users.objects.filter(email=data["email"]).first()
        if user and user.verify_password(data["userpassword"]):
            return data
        raise serializers.ValidationError("Invalid credentials")

    def create(self, validated_data):
        return validated_data


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['userpassword']


