from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'post'

urlpatterns = [
    path('', views.courses, name='course'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/<pk>', views.delete_course, name='delete_course'),
    path('add_test/', views.add_test, name='add_test'),
    path('delete_test/<pk>', views.delete_test, name='delete_test'),
    path('course/<slug>', views.test_by_slug, name='slug'),
    path('statistic/', views.show_group, name='group'),
    path('statistic/<name_group>', views.show_static_group,
         name='static_group'),
    path('statistic/static/<quiz_id>', views.show_static, name='static'),
    path('create_test/<quiz_id>', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/', views.display_quiz, name='display_quiz'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
]
