from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class signup(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'user/signup.html'
