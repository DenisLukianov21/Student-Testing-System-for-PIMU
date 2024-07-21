from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import initial_registration, additional_info, authentication, confirm_view
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', initial_registration, name='initial_registration'),
    path('user/signup/', additional_info, name='signup'),
    path('email/<str:token>/', confirm_view),
    path('login/', authentication, name='login'),
    path('logout/', LogoutView.as_view(template_name='user/logged_out.html'),
         name='logout'),
    path('confirm/', views.confirm_view, name='confirm'),
]
