from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import initial_registration, additional_info, authentication
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', initial_registration, name='initial_registration'),
    path('user/signup/', additional_info, name='signup'),
    path('login/', authentication, name='login'),
    path('logout/', LogoutView.as_view(template_name='user/logged_out.html'),
         name='logout'),
    path('about', views.about_user, name='about')

]
