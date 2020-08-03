from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Input_Data(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)    #ties prefs to user

    activated=models.BooleanField(default=False)                            #allows for calendar view in homepage

    startdate=models.DateField(default=datetime.date.today)
    enddate=models.DateField(default=datetime.date.today)

    swipes=models.PositiveIntegerField(default=1)                           #how many meals selected

    lenoir=models.BooleanField(default=True)                                #dining locations
    chase=models.BooleanField(default=False)

    breakfast=models.BooleanField(default=False)
    brunch=models.BooleanField(default=False)
    lunch=models.BooleanField(default=True)
    dinner=models.BooleanField(default=True)

    judgeoptions=models.BooleanField(default=False)                         #resets scores for foods

    #eventually add specific days of week, each station in the dining halls as bools


class Option_Name(models.Model):
    name=models.TextField(unique=True)                                      #just the food name

class Option(models.Model):
    optionname=models.ForeignKey(Option_Name, on_delete=models.CASCADE)     #ForeignKey = many_to_one
    calendar=models.ForeignKey(Input_Data, on_delete=models.CASCADE)

    needsjudgement=models.BooleanField(default=True)                        #then, upon render set to false
    score=models.BooleanField(default=False)                                #user's assigned score


class Meal(models.Model):
    calendar = models.ManyToManyField(Input_Data)
    options = models.ManyToManyField(Option_Name)

    MEAL_CHOICES=[
        ('breakfast','breakfast'),
        ('brunch', 'brunch'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
        ('none', 'none')
    ]
    LOCATION_CHOICES=[
        ('lenoir', 'lenoir'),
        ('chase', 'chase')
    ]

    date=models.DateField(null=True)
    meal=models.TextField(
        choices=MEAL_CHOICES, null=False
    )
    location=models.TextField(
        choices=LOCATION_CHOICES,
        null=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date','meal','location'], name='unique_meal_at_location')
        ]
        ordering = ['date', 'meal']