from bs4 import BeautifulSoup
import requests
from .models import Meal, Option_Name

def scrape(data, date):

    date = str(date)

    url = 'https://dining.unc.edu/locations/top-of-lenoir/?date='+date
    scrape_helper(data, date, url, 'lenoir')
        
    url = 'https://dining.unc.edu/locations/chase/?date='+date
    scrape_helper(data, date, url, 'chase')


def scrape_helper(data, date, url, location):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    ctabsnav = soup.find("div", class_="c-tabs-nav")    #gets which meals are offered (lunch, dinner)
    ctabs = soup.find_all("div", class_="c-tab")        #gets the content body of each meal

    if ctabsnav is None: 
        try:               # magic strings
            new_meal = Meal.objects.create(date=date,meal='none',location=location)
            new_meal.calendar.add(data)
            return
        except Exception:
            pass

    meals_offered=ctabsnav.find_all("div")
    if meals_offered is None:
        return 

    index = 0
    indexes=dict()

    for each_meal in meals_offered:     #checks each meal for being one of the desired meals,   
        if each_meal.text.startswith("Breakfast"): 
            indexes[index] = each_meal.text.split()[0]  #stores index for later to find applicable sections
        if each_meal.text.startswith("Brunch"): 
            indexes[index] = each_meal.text.split()[0]
        if each_meal.text.startswith("Lunch"): 
            indexes[index] = each_meal.text.split()[0]
        if each_meal.text.startswith("Dinner"): 
            indexes[index] = each_meal.text.split()[0]
        index+=1
    
    index = 0
    if ctabs is not None:
        for ctab in ctabs:
            
            if index not in indexes: #verifies correct mealtab being searched
                index += 1
                continue
            
            meal_string = indexes[index] #"Lunch" etc
            index += 1

            try:
                current_meal = Meal.objects.create(date=date,meal=meal_string.lower(),location=location)
            except Exception:
                current_meal = Meal.objects.get(date=date,meal=meal_string.lower(),location=location)
            current_meal.calendar.add(data)


            stations = ctab.find_all("div", class_="menu-station")
            if stations is None:
                continue
            for station in stations:
                station_name = station.find("h4") 
                
                if station_name is None:
                    continue

                if station_name.text == "Deli":
                    try:
                        Option_Name.objects.create(name='Deli')  #creates object here, will iterate throug and get scores later
                    except Exception:
                        pass
                    current_meal.options.add(Option_Name.objects.get(name='Deli'))


                if station_name.text not in {"Create","Nacho Bar", "The Griddle", "International Flavors", "The Kitchen Table", "Burritos & Bowls", "The Griddle", "Rotisserie", "The Grill", "Simply Prepared Grill"}: #subject to change
                    continue
                options = station.find_all("li", limit=4)

                if options is None:
                    continue

                for option in options:
                    current_option = option.text.strip()
                    try:
                        Option_Name.objects.create(name=current_option)  #creates object here, will iterate thru and get scores later
                    except Exception:
                        pass
                    current_meal.options.add(Option_Name.objects.get(name=current_option))