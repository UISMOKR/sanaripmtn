from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import (
    LoginUserView,
    RegisterUserView,
    UserProfileView,
    SearchAddressView,
    SearchFamilyMembersView,
    PasswordChangeView,
)


app_name = 'users'
router = DefaultRouter()
router.register('user-profile', UserProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path("citizen-address-info/", SearchAddressView.as_view(), name="citizen_address_info"),
    path("citizen-family-info/", SearchFamilyMembersView.as_view(), name="citizen_family_info"),
    path("user-register/", RegisterUserView.as_view(), name="user_register"),
    path("login/", LoginUserView.as_view(), name="login_user"),
    path("password-change", PasswordChangeView.as_view(), name="password_change")
]
