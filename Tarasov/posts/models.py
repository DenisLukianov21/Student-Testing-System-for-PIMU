from django.db import models
from user.models import Cource


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    test_in_cource = models.ForeignKey(Cource, on_delete=models.CASCADE)
    test_name = models.TextField()
    question = models.ForeignKey(
        'Questions',
        on_delete=models.CASCADE,
        related_name='quesion'
    )
    answers = models.ManyToManyField(
        'Answers',
        related_name='answers'
    )

    def __str__(self):
        return self.test_name


class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    id_right_answer = models.IntegerField()

    def __str__(self):
        return self.text


class Answers(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()

    def __str__(self):
        return self.text
