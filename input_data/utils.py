from bs4 import BeautifulSoup
import requests
from .models import Meal, Option


# meals=list()
# if data.breakfast:
#     if data.lenoir:
#         meals.append(Meal(meal='BRE',date=each_date,location='L').save())
#     if data.chase:
#         meals.append(Meal(meal='BRE',date=each_date,location='C').save())
# if data.brunch:
#     if data.lenoir:
#         meals.append(Meal(meal='BRU',date=each_date,location='L').save())
#     if data.chase:
#         meals.append(Meal(meal='BRU',date=each_date,location='C').save())
# if data.lunch:
#     if data.lenoir:
#         meals.append(Meal(meal='LUN',date=each_date,location='L').save())
#     if data.chase:
#         meals.append(Meal(meal='LUN',date=each_date,location='C').save())
# if data.dinner:
#     if data.lenoir:
#         meals.append(Meal(meal='DIN',date=each_date,location='L').save())
#     if data.chase:
#         meals.append(Meal(meal='DIN',date=each_date,location='C').save())
# for each_meal in meals:
#     #assign calendar to each mealtime
#     each_mealtime.calendar=data

#scraper
#needs to read thru data at each meal of the date and selected meals
#grab all the food, have user vote on the food
#score all meals
#let view pick up the best ones
def scrape(data, date):
    date = str(date)
    #just do both locations so one does not get ignored forever (checks if there is a meal created on a date and skips if so)
    # if data.lenoir:       
        #COPY PASTED FROM OG PROJECT
    url = 'https://dining.unc.edu/locations/top-of-lenoir/?date='+date
    scrape_helper(data, date, url, 'lenoir')
        
    # elif data.chase:
        #CHANGE THIS SFOR CHASE
    url = 'https://dining.unc.edu/locations/chase/?date='+date
    scrape_helper(data, date, url, 'chase')


def scrape_helper(data, date, url, location):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    ctabsnav = soup.find("div", class_="c-tabs-nav")    #gets meals offered (lunch, dinner)
    ctabs = soup.find_all("div", class_="c-tab")        #gets each content body of the meals

    if ctabsnav is None: 
        try:               # yes magic strings ikik
            Meal.objects.create(date=date,meal='none',location=location, calendar=data)
            return
        except Exception:
            pass

    meals_offered=ctabsnav.find_all("div")
    if meals_offered is None:       #unsure if this check is necessary
        return 

    index = 0
    indexes=dict()

    for each_meal in meals_offered:     #checks each meal for being one of the desired meals,   
        #I think i should actually just get them all? cuz potehrwise i have to do some weird filtering
        if each_meal.text.startswith("Breakfast"): 
            indexes[index] = each_meal.text.split()[0]  #stores index for later to find applicable sections
        if each_meal.text.startswith("Brunch"): 
            indexes[index] = each_meal.text.split()[0]
        if each_meal.text.startswith("Lunch"): 
            indexes[index] = each_meal.text.split()[0]
        if each_meal.text.startswith("Dinner"): 
            indexes[index] = each_meal.text.split()[0]
        index+=1
    
    #prefer to not do via index cuz its a pain, but I think i have to because the ctabs don't have any lunch or dinner etc identifiers themselves

    index = 0
    if ctabs is not None:
        for ctab in ctabs:
            
            if index not in indexes: #verifies correct mealtab being searched
                index += 1
                continue
            
            meal_string = indexes[index] #"Lunch" etc
            index += 1

            # current_meal = set()

            #TRY TO UNIQUE CHECK HERE MAYBE
            # if Meal.objects.filter(date=date,meal=meal_string.lower(),location=location).count() > 0:
            #     continue
            try:
                current_meal = Meal.objects.create(date=date,meal=meal_string.lower(),location=location, calendar=data)
            except Exception:
                pass

            stations = ctab.find_all("div", class_="menu-station")
            if stations is None:
                print("NO STATIONS FOUND")
                continue
            for station in stations:
                station_name = station.find("h4") 

                
                if station_name is None:
                    continue

                if station_name.text == "Deli":
                    # if "Deli" not in food:
                    #     set_food_score("Deli", food)
                    # if Option.objects.filter(option='Deli').count() == 0:
                    try:
                        Option.objects.create(option='Deli')  #creates object here, will iterate throug and get scores later
                    except Exception:
                        pass
                    current_meal.options.add(Option.objects.get(option='Deli'))
                    # current_meal.add("Deli")
                    # score += food["Deli"]

                if station_name.text not in {"Create","Nacho Bar", "The Griddle", "International Flavors", "The Kitchen Table", "Burritos & Bowls", "The Griddle", "Rotisserie", "The Grill", "Simply Prepared Grill"}: #subjec tto change
                    continue

                # print()
                # print(station_name.text)
                options = station.find_all("li", limit=4)

                if options is None:
                    continue

                for option in options:
                    current_option = option.text.strip()
                    try:
                    # if Option.objects.filter(option=current_option).count() == 0:
                        Option.objects.create(option=current_option)  #creates object here, will iterate throug and get scores later
                    except Exception:
                        pass
                    current_meal.options.add(Option.objects.get(option=current_option))

                    
                    # if current_option not in food:
                        # set_food_score(current_option, food)
                    # current_meal.add(current_option)
                    # score += food[current_option]


                
                # key = x+"-"+meal_string #only pulls "lunch" from lunch 11-2 for example
                # meals[key] = (score, current_meal)

        

    #indexes.clear()    #What is this for?
    

    #pass

def set_food_score(option):
    #so like we have to provide a screen where option name is displayed and a 'yes/no', then save
    #that to a new modelobject 
    #set custom superlike score maybe eventually
    
    pass



#FIRST, MAKE ALL OPTIONS WITHOUT SCORE. THEN, ITER THRU IN THE NEXT VIEW and assign scores