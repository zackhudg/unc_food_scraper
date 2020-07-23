from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Input_Data, Meal, Option
from .forms import InputForm, TinderSwipeForm
import calendar
import datetime
import heapq
from .utils import scrape
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

#, RawInputForm


# Create your views here.

def signup_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.username, "WAS REDIRECTED")
        return HttpResponseRedirect('/')
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)

        input_data = Input_Data.objects.create(user=user)

        login(request, user) 
        print("FORM WAS VALIDATED")
        return HttpResponseRedirect('/')
    print("FORM WAS NOT VALIDATED")
    return render(request, 'signup.html', {'form': form})

def signin_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    form = AuthenticationForm(request=request, data=request.POST or None)
    if form.is_valid():
        print("SIGNIN VALID")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("USER IS NOT NONE")
            login(request, user)
            return HttpResponseRedirect('/')
    # if form.is_valid():
    #     form.save()
    print("SIGNIN INVALID")
    return render(request, 'signin.html', {'form': form})   


def signout_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/signin')


def form_view(request, *args, **kwargs):
    cal = calendar.Calendar(firstweekday=6)
    startdate = datetime.date.today()
    enddate = datetime.date.today()

    #.itermonthdays(year,month) (returns somethin like 0 0 0 0 1 2 3 ... 31 0 0 )

    # print(request.GET)
    # print(request.POST)
    #request.POST.get('name of form)

    # form = RawInputForm() #default = request.GET
    # if request.method == "POST":
    #     form = RawInputForm(request.POST)
    #     if  form.is_valid():
    #         print(form.cleaned_data)
    #         User_Input.objects.create(**form.cleaned_data)
    #     else:
    #         print(form.errors)
    dates_checked = set()
    best_meals=list()

    def getMealDictionary(date, month_index):
        if data.startdate <= date <= data.enddate and date not in dates_checked:
            dates_checked.add(date)
            # print(date.isoformat()) 
            meals = Meal.objects.filter(date=date) #try to procure this all at once instead of daily
            # meals = Meal.objects.filter(date__range=[data.startdate, data.enddate])
            todays_meals_dict = dict()
            if not data.breakfast:
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
            for each in meals:
                print(each.id, each.date, each.meal, each.location)
                score = 0
                for option in each.options.all():
                    if option.score:
                        print(option.option)
                        score+=1
                if each.meal not in todays_meals_dict: 
                    todays_meals_dict[each.meal] = (score, each.location, False)
                        # for each in best_meals:
                            # print("CHOSEN:")
                            # print (each[2], each[3])
                else:
                    (compare_score, compare_location, chosen) = todays_meals_dict[each.meal]
                    if score > compare_score:
                        todays_meals_dict[each.meal] = (score, each.location, False)
                if len(best_meals) < data.swipes-1:
                    best_meals.append((score, month_index, date, each.meal))
                elif len(best_meals) < data.swipes:
                    best_meals.append((score, month_index, date, each.meal))
                    best_meals.sort()
                elif score > best_meals[0][0]:
                    best_meals[0]=(score, month_index, date, each.meal)
                    best_meals.sort()
            return todays_meals_dict
        return None


    dates_in_calendar = list()
    data = Input_Data.objects.get(user=request.user)
    print("DATA:", data)
    form=InputForm(request.POST or None, instance=data)   #auto_id="%s" not necessary abymore but eh
    if form.is_valid():
        print("VALID")
        #form=InputForm(request.POST, instance=data)
        data = form.save()

        if data.judgeoptions:
            for each in Option.objects.all():
                each.needsjudgement=True
                each.save()

        for year in range(data.startdate.year, data.enddate.year+1):
            for month in range(data.startdate.month, data.enddate.month+1):
                # dates_in_month = list(cal.itermonthdates(year, month))
                # dates_in_calendar.append(dates_in_month)
                #print(dates_in_month[0])
                for each_date in cal.itermonthdates(year, month):
                    if data.startdate <= each_date <= data.enddate:
                        #MAKE SURE NOT REPEAT OURSELVES HERE
                        #use unique_constraint then try unique_togetehr
                        #dont make a meal unless it exists though... do this in scrape
                        
                        
                        #all meals at times have been made. now we scrape at each day
                        meals_today = Meal.objects.filter(date=each_date) 
                        if meals_today.count() > 0:
                            continue
                        scrape(data, each_date)

        return HttpResponseRedirect('scrape/')

            # for each in dates_in_month:
            #     #use dates in month to make b,b,l,d if true in data
            #     if data.breakfast:
            #         breakfast = each
            #         Meal.objects.create
        
        #example: [[0,0,1,2...31,0],[0,1,2....,31,0,0,0]]

        # if data is None:
        #     data = form.save()
        #     print(data)
        # else:
        #     print(data.swipes)
        #     data.swipes=22
        #     print(data.swipes)
    else:
        print("INVALID")


    # get dates
    # startdate = data.startdate
    # enddate = data.enddate
    graydates_pre=0
    # graydates_post=0

    month_index=0
    #I could do the first one manually so i dont have to check if first month every time
    for year in range(data.startdate.year, data.enddate.year+1):
        for month in range(data.startdate.month, data.enddate.month+1):
            dates_in_month = {date:getMealDictionary(date, month_index) for date in cal.itermonthdates(year, month)}
            # print("BEST_MEALS:  ", best_meals)             
            if month==data.startdate.month:
                for each in dates_in_month:
                    if each < data.startdate:
                        graydates_pre+=1
            # if month==data.enddate.month:
            #     for each in dates_in_month:
            #         if each > data.enddate:
            #             graydates_pre+=1
            dates_in_calendar.append(dates_in_month)
            month_index+=1
            #print(dates_in_month[0])
            # for each_date in dates_in_month:
            #     if data.startdate <= each_date <= data.enddate:
                    #MAKE SURE NOT REPEAT OURSELVES HERE
                    #use unique_constraint then try unique_togetehr
                    #dont make a meal unless it exists though... do this in scrape
                    
                    
                    #all meals at times have been made. now we scrape at each day
                    # scrape(data, each_date)
                    #so now all options have been assigned to meals. next is to score them in the next view

    for each_tuple in best_meals:
        (score, month_index, date, meal) = each_tuple
        dates_in_calendar[month_index][date][meal] = dates_in_calendar[month_index][date][meal][:2]+(True,)
    #                     # SCRAAAAPE

                    


        #get food scores at those meals


    #select which swipes to use
    

    
    # meals_context=list(meals.values())

    # counter=0
    # print(meals_context)
    # for each in meals:
    #     current = meals_context[counter]
    #     current['score']=0
    #     for option in each.options.all():
    #          if option.score:
    #              current['score'] += 1
        
    #     counter += 1
    # print(meals_context)

    #days = list(cal.itermonthdays(startdate.year, startdate.month))
    context = {
        #'meal_scores':meal_scores,
        'form': list(form),
        'dates_in_calendar': dates_in_calendar,
        'data':data,
        'graydates_pre':graydates_pre,
        # 'graydates_post':graydates_post
        #need meal data (score, selected) ie: Lunch: 10 o or Dinner: 0 x
        #i think i have to make each month a dictionary, with keys pointing to the dict objects? or just with location/scores?
        #a la [{Aug-1:}]
    }


    return render(request, "form.html", context)

# def scrape_view(request, *args, **kwargs):
#     data=Input_Data.objects.first()

#     #get dates
#     # startdate = data.startdate
#     # enddate = data.enddate

#     for year in range(data.startdate.year, data.enddate.year+1):
#         for month in range(data.startdate.month, data.enddate.month+1):
#             dates_in_month = list(cal.itermonthdates(year, month))
#             dates_in_calendar.append(dates_in_month)
#             #print(dates_in_month[0])
#             for each in dates_in_month:
#                 if data.startdate < each < data.enddate:
    

    #get meals at those dates
        #get food scores at those meals


    #select which swipes to use

def scrape_view(request, *args, **kwargs):
    data = Input_Data.objects.first()
    cal = calendar.Calendar(firstweekday=6)

    # for year in range(data.startdate.year, data.enddate.year+1):
    #     for month in range(data.startdate.month, data.enddate.month+1):
    #         # dates_in_month = list(cal.itermonthdates(year, month))
    #         # dates_in_calendar.append(dates_in_month)
    #         #print(dates_in_month[0])
    #         for each_date in cal.itermonthdates(year, month):
    #             if data.startdate <= each_date <= data.enddate:
    #                 #MAKE SURE NOT REPEAT OURSELVES HERE
    #                 #use unique_constraint then try unique_togetehr
    #                 #dont make a meal unless it exists though... do this in scrape
                    
                    
    #                 #all meals at times have been made. now we scrape at each day
    #                 scrape(data, each_date)


    # all_option_forms = list()

    # for each_option in Option.objects.all():
    #     all_option_forms.append(each_option)

    # if request.POST
    # option_form = TinderSwipeForm(request.POST or None, instance=each_option)
    # print(option_form.is_bound)

    OptionFormSet = forms.modelformset_factory(Option, form=TinderSwipeForm, extra=0)
    valid_options=Option.objects.filter(needsjudgement=True)
    if valid_options.count() == 0:
        return HttpResponseRedirect('/')
    option_form = OptionFormSet(request.POST or None, queryset=valid_options)
    
    if option_form.is_valid():
        print("VALID")
        option_form.save()
        for each in valid_options:
            print(each.option)
            each.needsjudgement=False
            print(each.needsjudgement)
            each.save()
        return HttpResponseRedirect('/')
    else:
        print("INVALID")

    # data = Input_Data.objects.first()
    # form=InputForm(request.POST or None, instance=data)
    # if form.is_valid():
    #     #form=InputForm(request.POST, instance=data)
    #     data = form.save()
    #     return HttpResponseRedirect('scrape/')
    
    context={
        'all_option_forms':option_form
    }    
    return render(request, "tinder.html", context)

    # {2019-08-28: {breakfast: (5, chase), lunch:(6, lenoir)},
    #  2019-08-29: }