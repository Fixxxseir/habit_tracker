from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "tg_username",
            "th_chat_id",
            "phone_number",
            "avatar",
            "country",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "date_joined",
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)
        return {
            'user': {
                'username': user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
