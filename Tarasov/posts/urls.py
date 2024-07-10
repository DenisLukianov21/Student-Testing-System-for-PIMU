from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
    path('', views.courses, name='course'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/<pk>', views.delete_course, name='delete_course'),
    path('add_test/', views.add_test, name='add_test'),
    path('edit_test/<pk>', views.edit_test, name='edit_test'),
    path('delete_test/<pk>', views.delete_test, name='delete_test'),
    path('course/<slug>', views.test_by_slug, name='slug'),
    path('create_test/<quiz_id>', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/', views.display_quiz, name='display_quiz'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
    path('quick_results/', views.quiz_quick_results, name='quiz_quick_results'),
    path('group_results/', views.quiz_group_results, name='quiz_group_results')
]
