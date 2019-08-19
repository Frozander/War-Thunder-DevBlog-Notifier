from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from win10toast import ToastNotifier
import time
import pprint
from os import sys

target_URL = 'https://warthunder.com/en/news/?tags=Development'
#Change this value to represent your driver location
driver_path = 'C:/Users/batub/Desktop/chromedriver/chromedriver.exe'

#Toaster
toaster = ToastNotifier()

#Driver Options
options = Options()
options.add_argument('headless')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
# Driver Initialization
driver = webdriver.Chrome(executable_path=driver_path,options=options)
driver.get(target_URL)

#The Dirty Part
titles = []
new_titles = []
elapsed_time = 0
max_hours = 24
pp = pprint.PrettyPrinter(indent=4)

#Initialization notification
toaster.show_toast('Notifier Started',
                    'We will get you the news!',
                    icon_path='./icon.ico',
                    duration=5)

#We get every title from the first page of the news and add them to our list
top_news = driver.find_elements_by_class_name('news-item__title')
for news in top_news:
    titles.append(news.text)

while True:
    
    #If desired working time is passed, break the loop
    if elapsed_time >= (3600 * max_hours):
        break
    
    #Refresh the page in every loop (This happens once an hour, so no ban risk)
    driver.refresh()
    
    #Get the news titles again and put them in a different list
    top_news = driver.find_elements_by_class_name('news-item__title')
    for news in top_news:
        new_titles.append(news.text)
    
    #Sort them, just in case (Probably is not required)
    new_titles.sort()
    titles.sort()
    
    #Get the difference between two lists for boolean transform and printing the new articles
    comparison = set(new_titles).difference(titles)
    
    #If there is no difference between two lists, clear the second (check) list, wait for an hour and repeat
    #If there is a difference, notify user, print the differences, replace first(control) list with second and clear it.
    if not(bool(comparison)):
        new_titles.clear()
        time.sleep(3600)
        elapsed_time += 3600
    else:
        pp.pprint("Here are the changes:")
        pp.pprint(comparison)
        toaster.show_toast('New Devblog on War Thunder!',
                        'They released something new!',
                        icon_path='./icon.ico')
        titles.clear()
        titles = new_titles
        new_titles.clear()

driver.close()
    
