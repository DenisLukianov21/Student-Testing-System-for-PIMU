from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect
from user.models import Course, Group, UserGroup

from .models import Answer, Choice, Question, Result, Test


def delete_course(request, pk):
    Course.objects.filter(id=pk).delete()
    return redirect("/")


def delete_test(request, pk):
    Test.objects.filter(id=pk).delete()
    return redirect("/")


def add_course(request):
    data_course = request.POST.getlist('add-edit-course')
    print(data_course)
    data_len = len(data_course)
    new_course, created = Course.objects.get_or_create(
        name_course=data_course[data_len - 2],
        slug=data_course[data_len - 1]
    )
    select_groups = [group.id_group for group in Group.objects.filter(
        name_group__in=data_course[0:data_len - 2])]
    new_course.group_in_course.set(select_groups)
    new_course.save()
    return redirect("/")


@login_required
def add_test(request):
    data_test = request.POST.getlist('new-test-name')
    print(data_test)
    new_test, created = Test.objects.get_or_create(
        name=data_test[1],
        test_in_course=Course.objects.filter(slug=data_test[0])[0]
    )
    new_test.save()

    context = { 'quiz_id': new_test.pk }
    return render(request, 'posts/create_test.html', context)


@login_required
def edit_test(request, pk):
    quiz = get_object_or_404(Test, pk=pk)
    questions = quiz.question_set.all()

    context = {
        'quiz':quiz, 'quiz_id': pk,
        'questions': questions
    }
    return render(request, 'posts/edit_test.html', context)


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
            obj.tests = Test.objects.filter(test_in_course=course[0])

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
def create_quiz(request, quiz_id):
    iterator = 1
    while request.POST.getlist('questions-q' + str(iterator)) != []:
        data_question = request.POST.getlist('questions-q' + str(iterator))
        data_correct_ans = request.POST.getlist('correct-ans-q' + str(iterator))
        data_answers = request.POST.getlist('answers-q' + str(iterator))
        data_image = request.FILES.get('photo-q' + str(iterator), None)
        print(data_image)
        if data_image is None:
            data_image = ''

        new_question, created = Question.objects.get_or_create(
            name=data_question[0], test=get_object_or_404(Test, pk=quiz_id),
            eplanation=data_question[0], image=data_image
        )
        new_question.save()

        for answer in data_answers:
            new_ans, created = Answer.objects.get_or_create(
                question=new_question, name=answer
            )
            for correct_ans in data_correct_ans:
                if new_ans.name == correct_ans:
                    new_ans.is_correct = True
            new_ans.save()

        iterator = iterator + 1
    return redirect("/")


@login_required
def display_quiz(request, quiz_id):
    """
    Отображение вопроса.
    """
    quiz = get_object_or_404(Test, pk=quiz_id)
    questions = quiz.question_set.all()
    for question in questions:
        can_answer = question.user_can_answer(request.user)
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
    correct_answer = []
    for question in questions:
        correct_answer.append(question.get_answers()[0])
    answers_ids = request.POST.getlist('ans')
    user_answers = []
    if answers_ids:
        for answer_id in answers_ids:
            user_answer = Answer.objects.get(pk=answer_id)
            user_answers.append(user_answer.name)
            choice = Choice(user=request.user,
                            question=question, answer=user_answer)
            choice.save()
    for answer in user_answers:
        is_correct = answer in correct_answer
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
