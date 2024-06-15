from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.registration, name='signup'),
    path('login/', LoginView.as_view(template_name='user/new_auth.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='user/logged_out.html'),
         name='logout'),
    path('about', views.about_user, name='about')

]
