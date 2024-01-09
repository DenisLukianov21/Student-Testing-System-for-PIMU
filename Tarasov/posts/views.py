from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from user.models import Cource, UserGroup
from django.db.models import F

from .models import Test, Question, Answer, Choice, Result


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


def test_by_slug(request, slug):
    cource = Cource.objects.filter(slug=slug)
    tests = Test.objects.filter(test_in_cource=cource[0])
    context = {
        'page_obj': tests,
    }
    return render(request, 'posts/tests.html', context)


@login_required
def display_quiz(request, quiz_id):
    quiz = get_object_or_404(Test, pk=quiz_id)
    question = quiz.question_set.first()
    return redirect(reverse('post:display_question', kwargs={
        'quiz_id': quiz_id, 'question_id': question.pk}))


@login_required
def display_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Test, pk=quiz_id)
    questions = quiz.question_set.all()
    current_question, next_question = None, None
    for ind, question in enumerate(questions):
        if question.pk == question_id:
            current_question = question
            if ind != len(questions) - 1:
                next_question = questions[ind + 1]
    context = {'quiz': quiz, 'question': current_question,
               'next_question': next_question}
    return render(request, 'posts/test_page.html', context)


@login_required
def grade_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    quiz = get_object_or_404(Test, pk=quiz_id)
    can_answer = question.user_can_answer(request.user)
    try:
        if not can_answer:
            return render(request, 
                'posts/partial.html',  
                {'question': question,
                'error_message': 'Вы уже отвечали на этот вопрос.'})

        if question.qtype == 'single':
            correct_answer = question.get_answers()
            user_answer = question.answer_set.get(pk=request.POST['answer'])
            choice = Choice(user=request.user, question=question,
                            answer=user_answer)
            choice.save()
            is_correct = correct_answer == user_answer
            result, created = Result.objects.get_or_create(user=request.user,
                                                           quiz=quiz)
            if is_correct is True:
                result.correct = F('correct') + 1
            else:
                result.wrong = F('wrong') + 1
            result.save()

        elif question.qtype == 'multiple':
            correct_answer = question.get_answers()
            answers_ids = request.POST.getlist('answer')
            user_answers = []
            if answers_ids:
                for answer_id in answers_ids:
                    user_answer = Answer.objects.get(pk=answer_id)
                    user_answers.append(user_answer.name)
                    choice = Choice(user=request.user,
                                    question=question, answer=user_answer)
                    choice.save()
                is_correct = correct_answer == user_answers
                result, created = Result.objects.get_or_create(user=request.user,
                                                               quiz=quiz)
                if is_correct is True:
                    result.correct = F('correct') + 1
                else:
                    result.wrong = F('wrong') + 1
                result.save()
    except:
        return render(request, 'posts/partial.html', {'question': question})
    return render(request, 'posts/partial.html',
                  {'is_correct': is_correct,
                   'correct_answer': correct_answer,
                   'question': question})


@login_required
def quiz_results(request, quiz_id):
    profile = request.user
    quiz = get_object_or_404(Test, pk=quiz_id)
    questions = quiz.question_set.all()
    results = Result.objects.filter(user=request.user, 
                                    quiz=quiz).values()
    correct = [i['correct'] for i in results][0]
    wrong = [i['wrong'] for i in results][0]
    context = {'quiz': quiz,
               'profile': profile,
               'correct': correct, 
               'wrong': wrong, 
               'number': len(questions), 
               'skipped': len(questions) - (correct + wrong)}
    return render(request, 'posts/results.html', context)
