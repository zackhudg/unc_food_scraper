from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Input_Data, Meal, Option
from .forms import InputForm, TinderSwipeForm, UserCreateForm
import calendar
import datetime
import heapq
from .utils import scrape
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.

def signup_view(request, *args, **kwargs):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    form = UserCreateForm(request.POST or None)     #Using custom create form that removes the abundant help text
    if form.is_valid():                             #User has submitted the form w/ acceptable data
        form.save()                                 #updates db
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        input_data = Input_Data.objects.create(user=user)   #assigns each new user their own preferences
        login(request, user) 
        return HttpResponseRedirect('/')

    return render(request, 'signup.html', {'form': form})


def form_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/auth/login')

    cal = calendar.Calendar(firstweekday=6)
    startdate = datetime.date.today()
    enddate = datetime.date.today()

    dates_checked = set()
    best_meals=list()

    def getMealDictionary(date, month_index):       #assigns the highest scoring meals to each date to be used in templates
        if data.startdate <= date <= data.enddate and date not in dates_checked:
            dates_checked.add(date)
            meals = Meal.objects.filter(date=date) #TODO try to procure this all at once instead of daily, fewer db access
            todays_meals_dict = dict()

            if not data.breakfast:                          #removes meals that dont meet user's prefs
                meals = meals.exclude(meal='breakfast')
            if not data.brunch:
                meals = meals.exclude(meal='brunch')
            if not data.lunch:
                meals = meals.exclude(meal='lunch')
            if not data.dinner:
                meals = meals.exclude(meal='dinner')
            if not data.lenoir:
                meals = meals.exclude(location='lenoir')
            if not data.chase:
                meals = meals.exclude(location='chase')

            for each in meals:              #finds highest scoring meals for the date
                if each.meal == "none":     #magic words are fun
                    continue
                score = 0
                for option_name in each.options.all(): 
                    try:
                        option = Option.objects.get(optionname=option_name, calendar=data)  #see models.py
                    except:
                        option = Option.objects.create(optionname=option_name, calendar=data)
                    if option.score:
                        score+=1
                        
                if each.meal not in todays_meals_dict: 
                    todays_meals_dict[each.meal] = (score, each.location, False)
                else:
                    (compare_score, compare_location, chosen) = todays_meals_dict[each.meal]
                    if score > compare_score:
                        todays_meals_dict[each.meal] = (score, each.location, False)

            for meal in todays_meals_dict:          #selects the top {{number of swipes}} highest scoring meals to highlight in template
                score = todays_meals_dict[meal][0]
                if data.swipes < 1:
                    continue
                elif len(best_meals) < data.swipes-1:
                    best_meals.append((score, month_index, date, meal))
                elif len(best_meals) < data.swipes:
                    best_meals.append((score, month_index, date, meal))
                    best_meals.sort()
                elif score > best_meals[0][0]:
                    best_meals[0]=(score, month_index, date, meal)
                    best_meals.sort()

            return todays_meals_dict
        return None


    dates_in_calendar = list()
    data = Input_Data.objects.get(user=request.user)
    form=InputForm(request.POST or None, instance=data)

    if form.is_valid():         #webscrape to gain meal data      
        data = form.save()

        if data.judgeoptions:
            for each in Option.objects.filter(calendar=data):
                each.needsjudgement=True
                each.save()

        for year in range(data.startdate.year, data.enddate.year+1):
            for month in range(data.startdate.month, data.enddate.month+1):
                for each_date in cal.itermonthdates(year, month):
                    if data.startdate <= each_date <= data.enddate:
                        meals_today = Meal.objects.filter(date=each_date) 
                        if meals_today.count() > 0:
                            continue                #so we dont scrape if db already has the data
                        scrape(data, each_date)

        data.activated=True #enables the calendar view
        data.save()

    graydates_pre=0
    month_index=0

    for year in range(data.startdate.year, data.enddate.year+1):        #creates the calendar data for template
        for month in range(data.startdate.month, data.enddate.month+1):
            dates_in_month = {
                date:getMealDictionary(date, month_index) for date in cal.itermonthdates(year, month)
                }        
            if month==data.startdate.month:
                for each in dates_in_month:
                    if each < data.startdate:
                        graydates_pre+=1
            dates_in_calendar.append(dates_in_month)
            month_index+=1
           
    for each_tuple in best_meals:                                   #highlights the best meals in template
        (score, month_index, date, meal) = each_tuple
        dates_in_calendar[month_index][date][meal] = dates_in_calendar[month_index][date][meal][:2]+(True,)

    if form.is_valid():                     #sends user to the judge options page
        
        return HttpResponseRedirect('judge/')


    if data.activated:
        context = {
            'form': list(form),
            'dates_in_calendar': dates_in_calendar,
            'data':data,
            'graydates_pre':graydates_pre,
        }
        return render(request, "calendar.html", context)

    else:   #only used when user first signs up
        context={
            'form':list(form),
            'data':data,
        }
        return render(request, "form.html", context)


def judge_view(request, *args, **kwargs):

    OptionFormSet = forms.modelformset_factory(Option, form=TinderSwipeForm, extra=0)   #allows for looping of the judge option form
    valid_options = Option.objects.filter(calendar=Input_Data.objects.get(user=request.user), needsjudgement=True)
    
    if valid_options.count() == 0:
        return HttpResponseRedirect('/')

    option_form = OptionFormSet(request.POST or None, queryset=valid_options)
    
    if option_form.is_valid():
        option_form.save()
        for each in valid_options:
            each.needsjudgement=False
            each.save()
        return HttpResponseRedirect('/')

    context={
        'all_option_forms':option_form
    }    
    return render(request, "tinder.html", context)