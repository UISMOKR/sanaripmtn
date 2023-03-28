from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, pin, name, lastname, **extra_fields):
        """
        Methode creates user
        :param pin: int
        :param name: str
        :param lastname: str
        :param extra_fields: dict
        :return: User
        """
        if not pin:
            raise ValueError("Вы должны ввести свой ПИН")
        if not name:
            raise ValueError("Вы должны ввести свое имя")
        if not lastname:
            raise ValueError("Вы должны ввести свою фамилию")

        user = self.model(
            pin=pin,
            name=name,
            lastname=lastname,
            **extra_fields
        )
        user.set_password()
        user.save()
        return user

    def create_superuser(self, pin, name, lastname, password):
        """
        Methode creates superuser
        :param name: str
        :param lastname: str
        :param pin: int
        :param password: str
        :return: superuser
        """
        user = self.model(
            pin=pin,
            name=name,
            lastname=lastname,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 'Администратор'
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""

    operator = 'Оператор'
    admin = 'Администратор'
    user_type_choices = [
        (operator, 'Оператор'),
        (admin, 'Администратор'),
    ]

    pin = models.IntegerField(unique=True, verbose_name='ПИН')
    name = models.CharField(max_length=255, verbose_name='Имя')
    lastname = models.CharField(max_length=255, verbose_name='Фамилия')
    surname = models.CharField(max_length=255, null=True, blank=True, verbose_name='Отчество')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    user_type = models.CharField(max_length=255, choices=user_type_choices, default='operator', null=True, verbose_name='Роль пользователя')
    branch = models.ForeignKey('Branch', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Филиал')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Зарегистрировал')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    USERNAME_FIELD = "pin"
    REQUIRED_FIELDS = ["name", "lastname", ]

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.pin}'


class BranchType(models.Model):
    """Branch type model"""

    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'категорию филиала'
        verbose_name_plural = 'категории филиалов'

    def __str__(self):
        return f'{self.name}'


class Branch(models.Model):
    """Branch model"""

    name = models.CharField(max_length=255)
    type = models.ForeignKey('BranchType', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'филиал'
        verbose_name_plural = 'филиалы'

    def __str__(self):
        return f'{self.name}'
