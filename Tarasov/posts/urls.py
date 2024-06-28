from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
    path('', views.courses, name='course'),
    path('course/<slug>', views.test_by_slug, name='slug'),
    path('statistic/', views.show_group, name='group'),
    path('statistic/<name_group>', views.show_static_group,
         name='static_group'),
    path('statistic/static/<quiz_id>', views.show_static, name='static'),
    path('<int:quiz_id>/', views.display_quiz, name='display_quiz'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
]
