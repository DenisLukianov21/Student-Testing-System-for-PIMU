from django import forms
from .models import Test


class CheckBoxForm(forms.Form):
    tests = Test.objects.all()
    answers_query = None
    for test in tests:
        answers_query = test.answers.all()
    answer = forms.ModelMultipleChoiceField(queryset=answers_query,
                                            widget=forms.CheckboxSelectMultiple)
