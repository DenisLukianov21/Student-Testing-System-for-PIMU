from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

from .forms import CreationForm


class signup(CreateView):
    """
    View for user signup.

    This view is used to create new user accounts. It uses the `CreationForm`
    form for user registration. After successful registration, the user is
    redirected to the `posts:index` page.

    Attributes:
        form_class (CreationForm): The form used for user registration.
        success_url (str): The URL to redirect to after ->
        successful registration.
        template_name (str): The name of the template to use ->
        for user registration.
    """
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'user/signup.html'


def about_user(request):
    page_obj = request.user
    context = {
        'page_obj': page_obj
    }
    return render(request, 'user/user.html', context)
