from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Group, User, UserGroup, Course


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'id',
        'email',
    )
    list_filter = ('email',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name_group', 'id_group',)


@admin.register(UserGroup)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'group',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name_course',)
