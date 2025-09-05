from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

class UserLoginForm(AuthenticationForm):
    pass

from .models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'duration', 'is_active']

from .models import Question

class QuestionForm(forms.ModelForm):
    # Make correct_answer a dropdown from option1 to option4
    CHOICES = (
        ('option1', 'A'),
        ('option2', 'B'),
        ('option3', 'C'),
        ('option4', 'D'),
    )

    correct_answer = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control modern-input'}))

    class Meta:
        model = Question
        fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_answer']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control modern-input', 'rows':2}),
            'option1': forms.TextInput(attrs={'class':'form-control modern-input'}),
            'option2': forms.TextInput(attrs={'class':'form-control modern-input'}),
            'option3': forms.TextInput(attrs={'class':'form-control modern-input'}),
            'option4': forms.TextInput(attrs={'class':'form-control modern-input'}),
        }
