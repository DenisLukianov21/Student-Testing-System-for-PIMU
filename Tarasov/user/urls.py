from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='user/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='user/logged_out.html'),
         name='logout'),
    path('about', views.about_user, name='about')

]
