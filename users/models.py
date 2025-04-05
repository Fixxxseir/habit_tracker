from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле email должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь флаг is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь флаг is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=255,
                                null=True,
                                blank=True,
                                verbose_name="Username",
                                help_text="Введите username"
                                )
    email = models.EmailField(unique=True,
                              verbose_name="Email",
                              help_text="Введите email"
                              )
    tg_username = models.CharField(max_length=50,
                                   unique=True,
                                   verbose_name="Телеграм никнейм",
                                   help_text="Введите никнейм телеграмм"
                                   )
    th_chat_id = models.CharField(max_length=50,
                                  null=True,
                                  blank=True,
                                  verbose_name="Айди чата телеграмм",
                                  help_text="Введите айди чата телеграмм"
                                  )

    phone_number = PhoneNumberField(blank=True,
                                    null=True,
                                    verbose_name="Телефон",
                                    help_text="Введите ваш телефон"
                                    )
    country = models.CharField(blank=True,
                               null=True,
                               max_length=30,
                               verbose_name="Страна проживания",
                               help_text="Введите страну проживания"
                               )
    avatar = models.ImageField(upload_to="users/avatars/",
                               blank=True,
                               null=True,
                               verbose_name="Аватар",
                               help_text="Загрузите свой аватар"
                               )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
