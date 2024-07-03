from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
    path('', views.courses, name='course'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/<pk>', views.delete_course, name='delete_course'),
    path('delete_test/<pk>', views.delete_test, name='delete_test'),
    path('course/<slug>', views.test_by_slug, name='slug'),
    path('statistic/', views.show_group, name='group'),
    path('statistic/<name_group>', views.show_static_group,
         name='static_group'),
    path('statistic/static/<quiz_id>', views.show_static, name='static'),
    path('<int:quiz_id>/', views.display_quiz, name='display_quiz'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
]
