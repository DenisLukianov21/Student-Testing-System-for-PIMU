from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect
from user.models import Course, Group, UserGroup

from .models import Answer, Choice, Question, Result, Test


@login_required
def delete_course(request, pk):
    """
    Deletes a course based on the provided primary key.
    Parameters:
        request (HttpRequest): The request object.
        pk (int): The primary key of the course to be deleted.
    Returns:
        HttpResponseRedirect: Redirects to the homepage.
    """
    Course.objects.filter(id=pk).delete()
    return redirect("/")


@login_required
def delete_test(request, pk):
    """
    Deletes a test from the database based on the provided primary key.

    Parameters:
        request (HttpRequest): The request object.
        pk (int): The primary key of the test to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the homepage.
    """
    Test.objects.filter(id=pk).delete()
    return redirect("/")


@login_required
def add_course(request):
    """
    Adds a new course to the database.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the homepage.
    """
    # Get the list of data from the POST request
    data_course = request.POST.getlist('add-edit-course')
    # Get the length of the data list
    data_len = len(data_course)
    # Extract the course name and slug from the data list
    course_name = data_course[data_len - 2]
    slug = data_course[data_len - 1]
    # Get or create the course object
    new_course, created = Course.objects.get_or_create(
        name_course=course_name,
        slug=slug
    )
    # Get the list of group IDs from the data list
    select_groups = [group.id_group for group in Group.objects.filter(
        name_group__in=data_course[0:data_len - 2])]
    # Set the course's group_in_course field to the selected groups
    new_course.group_in_course.set(select_groups)
    new_course.save()
    return redirect("/")


@login_required
def add_test(request):
    """
    Adds a new test to the database.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the test creation page with the
        newly created test's primary key.
    """
    # Get the list of data from the POST request
    data_test = request.POST.getlist('new-test-name')
    # Extract the test name and course slug from the data list
    test_name = data_test[1]
    course_slug = data_test[0]
    # Get or create the test object
    new_test, created = Test.objects.get_or_create(
        name=test_name,
        test_in_course=Course.objects.get(slug=course_slug)
    )
    new_test.save()
    context = {'quiz_id': new_test.pk}
    # Render the test creation page with the context
    return render(request, 'posts/create_test.html', context)


@login_required
def edit_test(request, pk):
    """
    Edits an existing test.

    Parameters:
        request (HttpRequest): The request object.
        pk (int): The primary key of the test to be edited.

    Returns:
        HttpResponse: The rendered edit_test.html page with the test's data.
    """
    # Get the test object with the given primary key
    quiz = get_object_or_404(Test, pk=pk)
    # Get all questions related to the test
    questions = quiz.question_set.all()
    # Create a context dictionary with the test and its questions
    
    context = {
        'quiz': quiz,  # The test object
        'quiz_id': pk,  # The primary key of the test
        'questions': questions  # All questions related to the test
    }
    # Render the edit_test.html page with the context
    return render(request, 'posts/edit_test.html', context)


@login_required
def index(request):
    """
    Renders the index.html template and displays the main page.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered index.html page.
    """
    # Render the index.html page with the request object
    return render(request, 'posts/index.html')


@login_required
def courses(request):
    """
    Renders the courses.html template and displays all the courses
    available to the user.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered courses.html page with the courses' data.
    """
    # Get all groups
    group = Group.objects.all()

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the user's group
        user_group = UserGroup.objects.filter(user=request.user)[0].group

        # Get all courses in the user's group
        page_obj = Course.objects.filter(group_in_course=user_group)

        # Get all tests in each course and add them to the course object
        for obj in page_obj:
            course = Course.objects.filter(slug=obj.slug)
            obj.tests = Test.objects.filter(test_in_course=course[0])

        # Create a context dictionary with the groups and courses
        context = {
            'group': group,  # All groups
            'page_obj': page_obj,  # All courses in the user's group
        }

        # Render the courses.html page with the context
        return render(request, 'posts/courses.html', context)
    else:
        # Render the courses.html if the user is not authenticated
        return render(request, 'posts/courses.html')


@login_required
def test_by_slug(request, slug):
    """
    Render the tests.html template and display all the tests available
    to the user in the given course.

    Parameters:
        request (HttpRequest): The request object.
        slug (str): The slug of the course.

    Returns:
        HttpResponse: The rendered tests.html page with the tests' data.

    Raises:
        PermissionDenied: If the user does not have access to the course.
    """
    # Get the user's group
    group = UserGroup.objects.get(user=request.user).group

    # Get the course with the given slug
    course = Course.objects.filter(slug=slug)

    # Check if the user has access to the course
    if group not in course[0].group_in_course.all():
        raise PermissionDenied()

    # Get all the tests in the course
    tests = Test.objects.filter(test_in_course=course[0])

    # Create a context dictionary with the tests
    context = {
        'page_obj': tests,
    }

    # Render the tests.html page with the context
    return render(request, 'posts/tests.html', context)


@login_required
def create_quiz(request, quiz_id):
    """
    Create a quiz by adding questions to a test.

    Parameters:
        request (HttpRequest): The request object.
        quiz_id (int): The id of the test.

    Returns:
        HttpResponse: The redirect to the homepage.
    """
    # Initialize the iterator
    iterator = 1

    # Iterate over the questions
    while request.POST.getlist('questions-q' + str(iterator)) != []:
        # Get the data for the current question
        data_question = request.POST.getlist('questions-q' + str(iterator))
        data_correct_ans = request.POST.getlist(
            'correct-ans-q' + str(iterator))
        data_answers = request.POST.getlist('answers-q' + str(iterator))
        data_image = request.FILES.get('photo-q' + str(iterator), None)

        # If no image is provided, set it to an empty string
        if data_image is None:
            data_image = ''

        # Create a new question
        new_question, created = Question.objects.get_or_create(
            name=data_question[0], test=get_object_or_404(Test, pk=quiz_id),
            eplanation=data_question[0], image=data_image
        )
        new_question.save()

        # Create answers for the question
        for answer in data_answers:
            new_ans, created = Answer.objects.get_or_create(
                question=new_question, name=answer
            )
            # Set the correct answer
            for correct_ans in data_correct_ans:
                if new_ans.name == correct_ans:
                    new_ans.is_correct = True
            new_ans.save()

        # Increment the iterator
        iterator = iterator + 1

    # Redirect to the homepage
    return redirect("/")


@login_required
def display_quiz(request, quiz_id):
    """
    Display a quiz question to the user.

    Args:
        request (HttpRequest): The request object.
        quiz_id (int): The primary key of the quiz.

    Returns:
        HttpResponse: The rendered test_page.html page with the quiz data.
    """
    # Get the quiz object with the given primary key
    quiz = get_object_or_404(Test, pk=quiz_id)
    # Get all questions related to the quiz
    questions = quiz.question_set.all()

    # Check if the user can answer the quiz
    for question in questions:
        can_answer = question.user_can_answer(request.user)
    if not can_answer:
        # If the user cannot answer, render the partial.html page
        return render(request, 'posts/partial.html', {'quiz': quiz,
                                                      'questions': questions,
                                                      'user': request.user})

    # Create a context dictionary with the quiz and its questions
    context = {
        'quiz': quiz,  # The quiz object
        'quiz_id': quiz_id,  # The primary key of the quiz
        'questions': questions  # All questions related to the quiz
    }

    # Render the test_page.html page with the context
    return render(request, 'posts/test_page.html', context)


@login_required
def quiz_results(request, quiz_id):
    """
    Display the quiz results to the user.

    Args:
        request (HttpRequest): The request object.
        quiz_id (int): The primary key of the quiz.

    Returns:
        HttpResponse: The rendered results.html page with the quiz data.
    """
    # Get the quiz object with the given primary key
    quiz = get_object_or_404(Test, pk=quiz_id)
    # Get all questions related to the quiz
    questions = quiz.question_set.all()
    # Get the correct answers for each question
    correct_answer = []
    for question in questions:
        correct_answer.append(question.get_answers()[0])
    # Get the user's answers from the request
    answers_ids = request.POST.getlist('ans')
    user_answers = []
    if answers_ids:
        for answer_id in answers_ids:
            # Get the user's answer from the database
            user_answer = Answer.objects.get(pk=answer_id)
            user_answers.append(user_answer.name)
            # Create a Choice object to save the user's answer
            choice = Choice(user=request.user,
                            question=question, answer=user_answer)
            choice.save()
    # Calculate the number of correct and wrong answers
    for answer in user_answers:
        is_correct = answer in correct_answer
        result, created = Result.objects.get_or_create(
            user=request.user,
            quiz=quiz)
        if is_correct:
            result.correct += F('correct') + 1
        else:
            result.wrong += F('wrong') + 1
        result.save()
    # Calculate the percentage of correct answers
    result = Result.objects.get(quiz=quiz)
    percentage = int(result.correct / len(questions) * 100)
    # Create a context dictionary with the quiz and its results
    context = {
        'quiz': quiz,  # The quiz object
        'result': percentage  # The percentage of correct answers
    }
    # Render the results.html page with the context
    return render(request, 'posts/results.html', context)
