# Deputy Timesheet Downloader

This python script downloads employee timesheet and leave data from the timesheet manager deputy.com.
I wrote this script because while empoyers can easily download a csv of an employees timesheet data Deputy doesn't make that same data easily available to employees.

This script uses a headless browser to download the timesheet and leave data and save each as a csv. 

To install clone the repository, navigate to the directory and run

'''
pip install -r requirements.txt
'''
to install Selenium, BeautifulSoup4 and pandas if not installed. You will also need to download the webdriver from [Mozilla](https://github.com/mozilla/geckodriver/releases) and add it to the folder, Then run
'''
python main.py
'''
Which will prompt you for your deputy username and password as well at the deputy subdomain of your workplace including the country code. i,e. if your workspace address is
'https://mywork.au.deputy.com' then you would enter mywork.au
The script will then create two csv files, one for timesheets and one for leave.