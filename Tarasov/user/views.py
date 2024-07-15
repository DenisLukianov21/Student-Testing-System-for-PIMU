from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import InitialRegistrationForm, AdditionalInfoForm, LoginForm
from django.contrib.auth import authenticate, login

from .models import User, UserGroup
from user.models import Group

def initial_registration(request):
    if request.method == 'POST':
        form = InitialRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Указываем используемый бэкенд
            login(request, user)

            request.session['user_id'] = user.id

            # Добавить логику для отправки email с подтверждением

            return HttpResponseRedirect(reverse('user:signup'))
    else:
        form = InitialRegistrationForm()
    return render(request, 'user/new_auth.html',
                  {'reg_form': form, 'login_form': LoginForm()})

def additional_info(request):
    user = 0
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
    else:
        return HttpResponseRedirect(reverse('user:login'))
    print(user)
    form = AdditionalInfoForm()
    groups = Group.objects.all()

    if request.method == 'POST':
        form = AdditionalInfoForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Активируем пользователя
            user.save()
            
            if 'group' in request.POST:
                user_group, created = UserGroup.objects.get_or_create(
                    user=user, group=Group.objects.get(name_group=request.POST.get('group'))
                )
                user_group.save()
            else:
                user_group, created = UserGroup.objects.get_or_create(
                    user=user, group=Group.objects.get(name_group='profs')
                )
                user_group.save()
                
                user.is_staff = True
                user.save()

            return redirect('/')

    context = {
        'form': form, 'groups': groups
    }  
    return render(request, 'user/signup.html', context)

def authentication(request):
    registration_form = InitialRegistrationForm()
    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')

    return render(request, 'user/new_auth.html',
                  {'reg_form': registration_form, 'login_form': login_form})

def about_user(request):
    page_obj = request.user
    context = {
        'page_obj': page_obj
    }
    return render(request, 'user/user.html', context)
