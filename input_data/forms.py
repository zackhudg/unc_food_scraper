from django import forms
from .models import Input_Data, Option

class DateInputType(forms.DateInput):
    input_type='date'

class InputForm(forms.ModelForm):
    class Meta:
        model = Input_Data
        exclude=['user']
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
    


# class RawInputForm(forms.Form):
#     dates=forms.DateField()
#     swipes=forms.IntegerField()