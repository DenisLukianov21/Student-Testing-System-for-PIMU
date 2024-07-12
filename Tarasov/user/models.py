from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # По умолчанию пользователь неактивен

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Group(models.Model):
    name_group = models.CharField(max_length=50)
    id_group = models.AutoField(primary_key=True)
    courses = 0

    def __str__(self):
        return self.name_group


class UserGroup(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user',
        verbose_name='Ученик',
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        related_name='group',
        verbose_name='Группа',
        on_delete=models.CASCADE
    )


class Course(models.Model):
    name_course = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True)
    group_in_course = models.ManyToManyField("Group",
                                             related_name='Group_in_course')
    tests = 0

    def __str__(self):
        return self.name_course
