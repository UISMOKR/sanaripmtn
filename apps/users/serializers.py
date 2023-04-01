from rest_framework import serializers

from apps.users.models import (
    User,
    Branch,
)


class RegisterUserSerializer(serializers.ModelSerializer):
    """Register user model serializer"""

    class Meta:
        model = User
        fields = [
            'pin',
            'name',
            'lastname',
            'surname',
            'password',
            'date_of_birth',
            'user_type',
            'branch',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""

    class Meta:
        model = User
        exclude = [
            'groups',
            'user_permissions',
        ]
        read_only_fields = [
            'pin',
            'is_staff',
            'last_login',
            'is_superuser',
        ]
        extra_kwargs = {
            "password": {"required": False},
            "name": {"required": False},
            "lastname": {"required": False},
        }


# class PasswordChangeSerializer(serializers.ModelSerializer):
#     """User password change Serializer"""
#
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = 'password'
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Пароли не совпали"}
#             )


class LoginUserSerializer(serializers.ModelSerializer):
    """User login serializer"""
    class Meta:
        model = User
        fields = [
            'pin',
            'password'
        ]


class BranchSerializer(serializers.ModelSerializer):
    """"Branch Serializer"""

    class Meta:
        model = Branch
        fields = "__all__"


class SearchCitizenInfoSerializer(serializers.Serializer):
    """Citizen's address, family members search serializer"""

    pin = serializers.IntegerField()
