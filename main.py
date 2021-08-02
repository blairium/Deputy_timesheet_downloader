

'''
This script utilises selenium and BeautifulSoup4 to download timesheet data from Deputy then uses pandas to save that data as a csv.

I wrote this script to help employees access their timesheet information more easily so that they can calculate underpayments more easily.

I intend to add more data processing at some point to calculate things like hours worked, weekend hours worked, overtime etc and to compare pay 
against the award rate. I decided to release it before these things were finished because it's still useful in this form.

To use, install the required packages thrught the command

'pip install -r requirements.txt'

then run script. Enter Email and password when prompted, you'll also be prompted to add your workplaces subdomain and country code.
e.g if you access deputy via https://myworkplace.au.deputy.com your subdomain is myworkplace.au


'''



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import os
from datetime import date
import pandas as pd
from getpass import getpass

def get_timesheets():
    today = date.today()
    day_date = today.strftime("%d_%m_%Y")


    try:
        print('Creating browser instance')
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        driver = webdriver.Firefox(options=fireFoxOptions)
        # Web driver path
        WEBDRIVER_PATH = os.getcwd()
        # Web driver declaration
        driver.get(WEBDRIVER_PATH)


        workplace = input('Enter workplace deputy subdomain including country code: ')#workplace's deputy subdomain including country code
                
        # Website with login

        URL = "https://once.deputy.com/my/login"
        # Web driver going into website
        driver.get(URL)
        # Create a variable so you are able to check if login was successful
        login_title = driver.title

        while login_title == driver.title:
                
                    # Create a payload with the credentials
            payload = {'username':input('Enter Email Address: '), 
                    'password':getpass()
                    }
            print('Logging in')
            # Sending credentials 
            driver.find_element_by_id('login-email').send_keys(payload['username'])
            driver.find_element_by_id('login-password').send_keys(payload['password'])
            driver.find_element_by_id('btnLoginSubmit_ctl').click()

            #Check login
            if login_title == driver.title:
                print("Login failed, try again")
        print('Login sucessfull!')

        driver.get('https://{}.deputy.com/#profile'.format(workplace))


        time.sleep(5)

        css_selector = '#pnlMyTimesheetRepeater > div:nth-child(3) > a:nth-child(1)'

        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        driver.find_element_by_css_selector(css_selector).click()
        #driver.find_element_by_xpath(xpath).click()

        time.sleep(3)
        print('Grabbing shifts')
        shifts = []

        for element in driver.find_elements_by_class_name("m-horizontalRosterCard-wrapper"):
            shifts.append(element.text)
        
        shift = []
        for i in range(1,len(shifts)):
            #print(line)
            line = str(shifts[i]).split('\n')
            shift.append(line)
            
        print('processing timesheet data')
        cols = ['day', 'date', 'shift','time','break','location','status','type']
        timesheets = pd.DataFrame(shift,columns=cols)

        leave_taken =  timesheets[timesheets['location'] == 'APPROVED']

        timesheets = timesheets[timesheets['break'] != 'View']
        timesheets = timesheets[timesheets['break'] != 'Leave Request']
        timesheets = timesheets[timesheets['location'] != 'APPROVED']
        timesheets.pop('type')
        timesheets.pop('shift')
        timesheets[['start time', 'finish time']] = timesheets['time'].str.split('-', 1, expand=True)
        timesheets['break'] = timesheets['break'].str.split(' Meal', 1, expand=True)[0]
        timesheets.pop('time')


        leave_taken.to_csv('Deputy_leave_data_{}.csv'.format(day_date))
        timesheets.to_csv('Deputy_timesheet_data_{}.csv'.format(day_date))
        print('Raw Data saved as csv')
    finally:
        
        try:
            driver.close()
        except:
            pass

    return timesheets

if __name__ == "__main__":
    get_timesheets()