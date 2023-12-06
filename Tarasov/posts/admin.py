from django.contrib import admin
from .models import Test, Questions, Answers


class TestAdmin(admin.ModelAdmin):
    list_display = (
        'test_name',
        'question',
        'author',
    )
    list_editable = ('question', 'author',)
    empty_value_display = '-пусто-'


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
    )
    list_editable = ('text',)
    empty_value_display = '-пусто-'


class AnswersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
    )
    list_editable = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Test, TestAdmin)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(Answers, AnswersAdmin)
