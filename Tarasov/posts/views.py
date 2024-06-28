from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from user.models import Course, Group, UserGroup

from .models import Answer, Choice, Question, Result, Test


@login_required
def index(request):
    """ Показывает главную страницу.1 """
    return render(request, 'posts/index.html')


@login_required
def courses(request):
    """ Показывает все курсы доступные пользователю. """
    group = Group.objects.all()
    if request.user.is_authenticated:
        user_group = UserGroup.objects.filter(user=request.user)[0].group
        page_obj = Course.objects.filter(group_in_course=user_group)

        for obj in page_obj:
            course = Course.objects.filter(slug=obj.slug)
            print(course)
            obj.tests = Test.objects.filter(test_in_course=course[0])
            print(obj.tests)

        context = {
            'group': group,
            'page_obj': page_obj,
        }
        return render(request, 'posts/courses.html', context)
    else:
        return render(request, 'posts/courses.html')


@login_required
def test_by_slug(request, slug):
    """
    Показывает все тесты в курсе доступные пользователю.
    """
    group = UserGroup.objects.get(user=request.user).group
    course = Course.objects.filter(slug=slug)
    # Проверка доступа юзера
    if group not in course[0].group_in_course.all():
        raise PermissionDenied()
    tests = Test.objects.filter(test_in_course=course[0])
    context = {
        'page_obj': tests,
    }
    return render(request, 'posts/tests.html', context)


@login_required
def display_quiz(request, quiz_id):
    """
    Отображение вопроса.
    """
    quiz = get_object_or_404(Test, pk=quiz_id)
    questions = quiz.question_set.all()

    can_answer = questions[0].user_can_answer(request.user)
    if not can_answer:
        return render(request, 'posts/partial.html', {'quiz': quiz,
                                                      'questions': questions,
                                                      'user': request.user})

    context = {'quiz': quiz, 'quiz_id': quiz_id,
               'questions': questions}
    return render(request, 'posts/test_page.html', context)


@login_required
def quiz_results(request, quiz_id):
    """
    Отображение результата теста.
    """
    quiz = get_object_or_404(Test, pk=quiz_id)
    questions = quiz.question_set.all()

    for question in questions:
        correct_answer = question.get_answers()
        answers_ids = request.POST.getlist('ans')
        user_answers = []
        if answers_ids:
            for answer_id in answers_ids:
                user_answer = Answer.objects.get(pk=answer_id)
                user_answers.append(user_answer.name)
                choice = Choice(user=request.user,
                                question=question, answer=user_answer)
                choice.save()
            is_correct = correct_answer == user_answers
            result, created = Result.objects.get_or_create(
                user=request.user,
                quiz=quiz)
            if is_correct is True:
                result.correct = F('correct') + 1
            else:
                result.wrong = F('wrong') + 1
            result.save()
    result = Result.objects.get(quiz=quiz)
    context = {'quiz': quiz,
               'result': int(result.correct / len(questions) * 100)}
    return render(request, 'posts/results.html', context)


@login_required
def show_group(request):
    """
    Отображение групп.
    """
    group = Group.objects.all()
    context = {
        'page_obj': group
    }
    return render(request, 'posts/static_group.html', context)


@login_required
def show_static_group(request, name_group):
    """
    Отображение участников групп.
    """
    group = Group.objects.get(name_group=name_group)
    user_group = UserGroup.objects.filter(group=group)
    course = Course.objects.filter(group_in_course=group)
    tests = Test.objects.filter(test_in_course=course[0])
    context = {
        'page_obj': user_group,
        'test_obj': tests,
    }
    return render(request, 'posts/static_group_show.html', context)


@login_required
def show_static(request, quiz_id):
    """
    Отображение общей статистики группы по тесту.
    """
    if request.user.is_staff:
        test = get_object_or_404(Test, pk=quiz_id)
        questions = len(Question.objects.filter(test=test))
        result = Result.objects.filter(quiz=test)
        page_obj = []
        for user in result:
            procentage = (questions/user.correct) * 100
            user_and_procentage = [user.user, procentage]
            page_obj.append(user_and_procentage)
        context = {
            'page_obj': page_obj,
            'test': test,
        }
    else:
        result = Result.objects.filter(user=request.user)
        page_obj = []
        for obj in result:
            name_course_and_tests = [obj.quiz.test_in_course, obj.quiz]
            page_obj.append(name_course_and_tests)
        print(page_obj)
        context = {
            'U_page_obj': page_obj
        }

    return render(request, 'posts/static.html', context)
