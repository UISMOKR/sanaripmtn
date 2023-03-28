from django.contrib import admin
from apps.users.models import (
    User,
    Branch,
    BranchType,
)
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.site_header = 'Административная панель'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['pin', 'date_of_birth', 'name', 'lastname', 'surname', 'branch', 'user_type']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    add_form_template = None
    add_form = UserCreationForm
    list_display = ['pin', 'name', 'lastname', 'surname', 'date_of_birth', 'branch', 'user_type', 'is_active', 'is_superuser']
    list_filter = ['user_type', 'branch']
    readonly_fields = ['created_by', 'date_of_creation', 'is_staff']
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Персональная информация', {'fields': ['name', 'lastname', 'surname', 'date_of_birth', 'branch', 'user_type',
                                                'created_by', 'date_of_creation', 'is_staff', 'is_active']}),
        ('Разрешения пользователя', {'fields': ['user_permissions']}),
    )
    add_fieldsets = (
        ('Персональная информация', {'fields': ['pin', 'password1', 'password2', 'name', 'lastname', 'surname',
                                                'date_of_birth', 'branch', 'user_type']}),
        ('Разрешения пользователя', {'fields': ['user_permissions']}),
    )
    search_fields = []
    ordering = []
    model = User

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        if obj.user_type == 'Администратор':
            obj.is_staff = True
        else:
            pass
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
admin.site.register(Branch)
admin.site.register(BranchType)
