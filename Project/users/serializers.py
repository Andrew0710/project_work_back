from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неправельний номер або пароль")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone", "first_name", "last_name", "role", "is_active")
        read_only_fields = ("id",)

    def validate_role(self, value):
        request = self.context.get("request")
        if request and request.user.is_authenticated and request.user.role != "ADMIN":
            raise serializers.ValidationError("Only admins can assign roles.")
        return value


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD