from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from win10toast import ToastNotifier
import time
import pprint
from os import sys

#Toaster
toaster = ToastNotifier()

# Driver Options and Path
options = Options()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path="C:/Users/batub/Desktop/chromedriver/chromedriver.exe",options=options)

target_URL = 'https://warthunder.com/en/news/?tags=Development'

driver.get(target_URL)

#The Dirty Part
titles = []
new_titles = []
elapsed_time = 0
max_hours = 24
pp = pprint.PrettyPrinter(indent=4)

toaster.show_toast('Notifier Started',
                    'We will get you the news!',
                    icon_path='./icon.ico',
                    duration=5)

top_news = driver.find_elements_by_class_name('news-item__title')
for news in top_news:
    titles.append(news.text)

while True:
    
    if elapsed_time >= (3600 * max_hours):
        break
    
    top_news = driver.find_elements_by_class_name('news-item__title')
    for news in top_news:
        new_titles.append(news.text)
    
    new_titles.sort()
    titles.sort()
    
    comparison = set(new_titles).difference(titles)
    
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
    
