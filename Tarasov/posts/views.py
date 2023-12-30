from django.shortcuts import render
from .forms import CheckBoxForm

from user.models import UserGroup, Cource
from .models import Test


def check_test(request, tests):
    user_answers = request.POST.get('answer')
    user_sucsess = False
    id_right_answer = None
    for test in tests:
        id_right_answer = test.question.id_right_answer
    if user_answers == str(id_right_answer):
        user_sucsess = True
    return user_sucsess


def index(request):
    return render(request, 'posts/index.html')


def courses(request):
    user = request.user
    if user.is_authenticated:
        user_group = UserGroup.objects.filter(user=user)[0].group
        page_obj = Cource.objects.filter(group_in_course=user_group)
        context = {
            'page_obj': page_obj,
        }
        return render(request, 'posts/courses.html', context)
    else:
        return render(request, 'posts/courses.html')


def tests(request):
    tests = Test.objects.all()
    if request.method == 'POST':
        form = CheckBoxForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = CheckBoxForm()
    context = {
        'form': form,
        'page_obj': tests,
        'check': check_test(request, tests)
    }
    return render(request, 'posts/tests.html', context)
