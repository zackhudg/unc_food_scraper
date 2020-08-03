from django import forms
from .models import Input_Data, Option, User
from django.contrib.auth.forms import UserCreationForm

class DateInputType(forms.DateInput):
    input_type='date'

class InputForm(forms.ModelForm):
    class Meta:
        model = Input_Data
        exclude=['user', 'activated']
        widgets={
            'startdate': DateInputType(),
            'enddate': DateInputType()
        }

class TinderSwipeForm(forms.ModelForm):
    class Meta:
        model = Option
        fields=['score']
        labels = {
            'score':''
        }    
    
class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        help_texts = {
            'username': None,
            'password1': None,
        }
