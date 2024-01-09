from django.contrib import admin
from .models import Test, Question, Answer, Choice, Result


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result)
