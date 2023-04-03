import requests
from decouple import config

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import (
    SearchCitizenInfoSerializer,
    RegisterUserSerializer,
    UserProfileSerializer,
    LoginUserSerializer,
    PasswordChangeSerializer,
)


class RegisterUserView(CreateAPIView):
    """User Registration"""

    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, )

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user_type = request.data['user_type']
            if user_type == 'Администратор':
                serializer.save(is_staff=True, created_by=self.request.user)
                return Response(serializer.data)
            else:
                serializer.save(is_staff=False, created_by=self.request.user)
                return Response(serializer.data)
        return Response(serializer.errors)


class LoginUserView(CreateAPIView):
    """User login"""

    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        pin = request.data["pin"]
        password = request.data["password"]
        user = User.objects.filter(pin=pin).first()

        if user is None:
            raise AuthenticationFailed("Пользователь с такими учетными данными не найден!")
        if user.is_active is False:
            raise AuthenticationFailed("Ваша учетная запись неактивна")
        if not user.check_password(password):
            raise AuthenticationFailed("Неверный пароль!")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": "Вы, успешно авторизовались!",
                "user_id": user.pk,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class UserProfileView(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        """Filter profile by current user"""

        user = self.request.user

        if user.is_anonymous:
            return self.queryset.filter(id=-1)
        elif user.user_type == 'Оператор':
            return self.queryset.filter(id=user.pk)
        else:
            return self.queryset


class PasswordChangeView(APIView):
    """User password change"""

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):

        old_password = request.data['old_password']
        new_password = request.data['new_password']
        user = User.objects.filter(pk=self.request.user.pk).first()
        if not user.check_password(old_password):
            raise AuthenticationFailed("Действующий пароль неверный!")
        else:
            user.set_password(new_password)
            user.save()
            return Response({"статус": "Пароль успешно изменён"})


class SearchAddressView(GenericAPIView):
    """Search citizen address info by PIN"""

    serializer_class = SearchCitizenInfoSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        url = config('address_url')
        serializer = SearchCitizenInfoSerializer(data=request.data)
        if serializer.is_valid():
            pin = serializer.validated_data['pin']
            payload = requests.get(
                url=f'{url}/{pin}',
                headers={config('headers_key'): config('headers_value')},
                verify=False
            )
            return Response(payload.json(), status=status.HTTP_200_OK)
        return Response('По данному ПИНу ничего не найдено!', status=status.HTTP_404_NOT_FOUND)


class SearchFamilyMembersView(GenericAPIView):
    """Search citizen family members info by PIN"""

    serializer_class = SearchCitizenInfoSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        url = config('family_members_url')
        serializer = SearchCitizenInfoSerializer(data=request.data)
        if serializer.is_valid():
            pin = serializer.validated_data['pin']
            payload = requests.get(
                url=f'{url}/{pin}',
                headers={config('headers_key'): config('headers_value')},
                verify=False
            )
            return Response(payload.json(), status=status.HTTP_200_OK)
        return Response('По данному ПИНу ничего не найдено!', status=status.HTTP_404_NOT_FOUND)