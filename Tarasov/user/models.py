from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    email = models.EmailField('Почта', max_length=254, unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Group(models.Model):
    name_group = models.CharField(max_length=50)
    id_group = models.AutoField(primary_key=True)

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


class Cource(models.Model):
    name_cource = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True)
    group_in_course = models.ManyToManyField("Group",
                                             related_name='Group_in_course')

    def __str__(self):
        return self.name_cource
