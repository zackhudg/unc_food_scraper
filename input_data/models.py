from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Input_Data(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    activated=models.BooleanField(default=False)

    startdate=models.DateField(default=datetime.date.today)
    enddate=models.DateField(default=datetime.date.today)

    swipes=models.PositiveIntegerField(default=1)

    lenoir=models.BooleanField(default=True)
    chase=models.BooleanField(default=False)

    breakfast=models.BooleanField(default=False)
    brunch=models.BooleanField(default=False)
    lunch=models.BooleanField(default=True)
    dinner=models.BooleanField(default=True)

    judgeoptions=models.BooleanField(default=False)

    #eventually add specific days of week as bools

    #id=userid

class Option_Name(models.Model):
    name=models.TextField(unique=True)

class Option(models.Model):
    optionname=models.ForeignKey(Option_Name, on_delete=models.CASCADE)
    calendar=models.ForeignKey(Input_Data, on_delete=models.CASCADE)

    needsjudgement=models.BooleanField(default=True)  #then, on render set to false
    score=models.BooleanField(default=False)


class Meal(models.Model):
    
    #many to one -> eventually when score not tied to this, make it many to many
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

    #selected=models.BooleanField(default=False) #instead just sort and then pick however many

    # meal=choice
    # location=choice
    # combine with meal
    #meals = many-to-one


# class Meal(models.Model):
    

#     at_lenoir=models.BooleanField(default=False)
#     at_chase=models.BooleanField(default=False)

    
    #collection of options

    #CAN SHARE MEALS BETWENE USERS IF SCORE NOT INVOLVED, many-many
    #do that later though maybe, get it to work for one rn

#food in db: needs user id and score    like go to food > then correlate id with score
#meal can have only options listed, no need for ids yet (i dont think)