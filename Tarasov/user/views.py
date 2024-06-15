from django.shortcuts import render
from django_email_verification import send_email
from django.shortcuts import render, redirect
from .forms import CreationForm


def registration(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # высылаем письмо и делаем его неактивным
            user.is_active = False
            send_email(user)
            return redirect('/')
    else:
        form = CreationForm()
    return render(request, 'user/signup.html', {'form': form})


def about_user(request):
    page_obj = request.user
    context = {
        'page_obj': page_obj
    }
    return render(request, 'user/user.html', context)
