from django.db import models
from user.models import Course, User


class Test(models.Model):
    """
    Represents a test in a course.

    Attributes:
        name (str): The name of the test.
        test_in_course (Course): The course that the test belongs to.

    """
    name = models.CharField(max_length=120)
    test_in_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lead_time = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    """
    Represents a question in a test.

    Attributes:
        name (str): The name of the question.
        qtype (str): The type of the question.
        test (Test): The test that the question belongs to.
        eplanation (str): The explanation of the question.
        image (ImageField): The image associated with the question.

    Methods:
        get_answers(): Returns the names of the correct answers.
        user_can_answer(user): Checks if the user has
        already answered the question.
        __str__(): Returns the name of the question.
    """
    class qtype(models.TextChoices):
        multiple = 'multiple'

    name = models.CharField(max_length=350)
    qtype = models.CharField(max_length=8,
                             choices=qtype.choices,
                             default=qtype.multiple)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    eplanation = models.CharField(max_length=550)
    image = models.ImageField(blank=True)

    def get_answers(self):
        """Returns the names of the correct answers."""
        qs = self.answer_set.filter(is_correct=True).values()
        return [i.get('name') for i in qs]

    def user_can_answer(self, user):
        """Checks if the user has already answered the question."""
        user_choices = user.choice_set.all()
        done = user_choices.filter(question=self.id)
        print(done)
        if done.exists():
            return False
        return True

    def __str__(self):
        """Returns the name of the question."""
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    """
    Represents an answer to a question in a quiz.

    Attributes:
        question (Question): The question that this answer belongs to.
        name (str): The name of the answer.
        is_correct (bool): Whether or not this answer is correct.

    Methods:
        __str__(): Returns the name of the answer.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        """Returns the name of the answer."""
        return self.name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Choice(models.Model):
    """
    Represents a choice made by a user for a specific question.

    Attributes:
        user (User): The user who made the choice.
        question (Question): The question that the user chose an answer for.
        answer (Answer): The answer that the user chose.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Result(models.Model):
    """
    Represents a result of a user's participation in a specific quiz.

    Attributes:
        quiz (Test): The quiz that the user participated in.
        user (User): The user who participated in the quiz.
        correct (int): The number of correct answers chosen by the user.
        wrong (int): The number of incorrect answers chosen by the user.
    """
    quiz = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
