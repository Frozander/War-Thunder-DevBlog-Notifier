from selenium import webdriver
from win10toast import ToastNotifier
import time
from os import sys

#Toaster
toaster = ToastNotifier()

# Driver Options and Path
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path="C:/Users/batub/Desktop/chromedriver/chromedriver.exe",chrome_options=options)

target_URL = 'https://warthunder.com/en/news/?tags=Development'

driver.get(target_URL)

#The Dirty Part
titles = []
new_titles = []
elapsed_time = 0
max_hours = 24

toaster.show_toast('DevBlog Notifier has Started!',
                   'We started to get the news for you!',
                   icon_path='./icon.ico',
                   duration=5)

def notifier():
    top_news = driver.find_elements_by_class_name('news-item__title')
    for news in top_news:
        titles.append(news.text)

    while True:
        
        if elapsed_time >= (3600 * max_hours):
            sys.exit()
        
        
        top_news = driver.find_elements_by_class_name('news-item__title')
        for news in top_news:
            new_titles.append(news.text)
        
        new_titles.sort()
        titles.sort()
        
        if new_titles == titles:
            new_titles.clear()
            time.sleep(3600)
            elapsed_time += 3600
        else:
            toaster.show_toast('New Devblog on War Thunder!',
                            'They released something new!',
                            icon_path='./icon.ico')
            titles.clear()
            titles = new_titles
            new_titles.clear()
    

try:
    notifier()
except KeyboardInterrupt:
    driver.close()
    print('Manually Exited!')
except SystemExit:
    driver.close()
    print('Max Time is passed!')
except:
    print('Unexcpected error!')
    
    
