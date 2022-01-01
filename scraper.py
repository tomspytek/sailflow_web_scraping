"""Scrape wind data from target SailFlow page.

Must specify desired target page and PATH to Chrome driver file.
   
Functions:
    scrape()
    
Variables:
    target
    PATH
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#EDIT THESE VARIABLES
#TARGET IS A SAILFLOW FORECAST URL
target = ''
#PATH IS THE PATH TO YOUR CHROMEDRIVER.EXE FILE
PATH = ''

def scrape_days(driver):
    """Scrape the day of the week from target SailFlow page.
    
    :param driver: Chrome webdriver object
    :return: 1d list of strs
    """ 
    days_path = '//table[@class="jw-fxt-table ui-draggable"]/tbody/tr[1]'
    days_row = driver.find_element_by_xpath(days_path)
    days = days_row.find_elements_by_tag_name('td')
    days_list = [day.text for day in days]
    return days_list
    
def scrape_hours(driver):
    """Scrape the time values from target SailFlow page.
    
    :param driver: Chrome webdriver object
    :return: 1d list of strs
    """ 
    hours_path = '//table[@class="jw-fxt-table ui-draggable"]/tbody/tr[2]'
    hours_row = driver.find_element_by_xpath(hours_path)
    hours = hours_row.find_elements_by_tag_name('td')
    hours_list = [hour.text for hour in hours]
    return hours_list

def scrape_wind_info(driver):
    """Scrape the avg wind, gust, and direction info from target SailFlow page.
    
    :param driver: Chrome webdriver object
    :return: 1d list of strs
    """ 
    wind_path = '//table[@class="jw-fxt-table ui-draggable"]/tbody/tr[3]'
    wind_row = driver.find_element_by_xpath(wind_path)
    wind_info = wind_row.find_elements_by_tag_name('td')
    wind_list = [wind_str.get_attribute('title') for wind_str in wind_info]
    return wind_list

    
def scrape():
    """Return wind data scraped from target SailFlow page.
    
    return: tuple of 1d lists of strs   
    """
    driver = webdriver.Chrome(PATH)
    driver.get(target)
    
    try:
        xpath = '//table[@class="jw-fxt-table ui-draggable"]/tbody'
        forecast_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        days = scrape_days(driver) 
        hours = scrape_hours(driver) 
        undivided_wind_info = scrape_wind_info(driver) 
    finally:
        driver.quit()
    return days, hours, undivided_wind_info



