from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

from .forms import CreationForm


class signup(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'user/signup.html'


def about_user(request):
    page_obj = request.user
    context = {
        'page_obj': page_obj
    }
    return render(request, 'user/user.html', context)
