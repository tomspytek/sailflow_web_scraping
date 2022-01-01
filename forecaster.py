"""Generate a beach volleyball playability forecast for the next five days.

Automatically retrieve and analyze wind data for the next five days.  Applies
generally-accepted criteria for playability on the beach (see analyze_* 
functions for specifics.)
   
Functions:
    get_forecast()
"""

import scraper as sc
import data_cleaner as dc
import statistics as stat
     
def gust_stats(data):
    """Return avg and max gust.
    
    :param data: 1d list of ints
    :return: tuple of ints
    """     
    mean_gust = stat.mean(data)
    max_gust = max(data)
    return(mean_gust,max_gust)

def wind_stats(data):
    """Return avg and max wind.
    
    :param data: 1d list of ints
    :return: tuple of ints
    """     
    mean_wind = stat.mean(data)
    max_wind = max(data)
    return(mean_wind,max_wind)
    
def analyze_wind(data): 
    """Print analysis of wind conditions.
    
    Takes a list of wind data and determines if it meets playability 
    criteria.
    
    :param data: 1d list of ints
    :return: str
    """     
    mean_wind = wind_stats(data)[0]
    max_wind = wind_stats(data)[1]
    
    if max_wind > 25:
        return 'Unplayably high winds'
    if mean_wind < 10:
        return 'Low wind'
    elif mean_wind < 15:
        return 'Moderate wind'
    elif mean_wind < 20:
        return 'Moderately high wind'
    else:
        return 'Unplayably high winds'
    
def analyze_gusts(wind,gust):
    """Print analysis of gust data.
    
    Takes a list of wind and gust data and determines if they meet playability 
    criteria.
    
    :param wind: 1d list of ints
    :param gust: 1d list of ints
    :return: str
    """     
    mean_wind = wind_stats(wind)[0]
    mean_gust = gust_stats(gust)[0]
    max_gust = gust_stats(gust)[1]
    diff = mean_gust - mean_wind
    if diff < 5 or mean_gust < 15:
        return('No gusts')
    if max_gust > 25:
        return 'Unplayably gusty'
    elif diff < 10:
        return('Gusty')
    else:
        return('Very Gusty')

def get_target_range(weekday,hours,l):
    """Return list of ints sliced based on day of the week.
    
    Takes a list of integer data and returns data from 5PM onwward for weekdays
    or 9AM onward and 3PM onward for weekends.  
    
    :param weekday: bool
    :param hours: list of ints
    :l: list of ints
    :return: tuple of 1d list of ints
    """  
    if weekday:
        start1730 = hours.index('5PM')
        target_range = l[start1730:start1730+5]
        return target_range
    else:
        start0930 = hours.index('9AM')
        start1630 = hours.index('3PM')
        target_range_0 = l[start0930:start0930+7]
        target_range_1 = l[start1630:start1630+7]
        return (target_range_0, target_range_1)
    
def weekday_analysis(day):
    """Print result of analysis of wind data for a weekday.
    
    Uses analyze_wind and analyze_gusts functions to determine playability 
    for a weekday.
    
    :param day: Day object
    :return: None
    """  
    day_name = day.get_day()
    hours = day.get_time()
    wind = day.get_wind_data()
    gusts = day.get_gust_data()

    target_wind = get_target_range(True, hours, wind)
    target_gusts = get_target_range(True, hours, gusts)

    wind_verdict = analyze_wind(target_wind)
    gusts_verdict = analyze_gusts(target_wind,target_gusts)
    output = F'{day_name}: {wind_verdict}, {gusts_verdict}'
    print(output)

def weekend_analysis(day):
    """Print result of analysis of wind data for a weekend day.
    
    Uses analyze_wind and analyze_gusts functions to determine playability 
    for a weekend day.
    
    :param day: Day object
    :return: None
    """      
    day_name = day.get_day()
    hours = day.get_time()
    wind = day.get_wind_data()
    gusts = day.get_gust_data()
    
    morn_wind, aft_wind = get_target_range(False, hours, wind)
    morn_gusts, aft_gusts = get_target_range(False, hours, gusts)
    morn_wind_verdict = analyze_wind(morn_wind)        
    morn_gusts_verdict = analyze_gusts(morn_wind,morn_gusts)
    aft_wind_verdict = analyze_wind(aft_wind)        
    aft_gusts_verdict = analyze_gusts(aft_wind,aft_gusts)
    
    morn_output = (F'{day_name} After 9AM: '
                   + F'{morn_wind_verdict}, ' 
                   + F'{morn_gusts_verdict}')
    aft_output = (F'{day_name} After 3PM: '  
                   + F'{aft_wind_verdict}, ' 
                   + F'{aft_gusts_verdict}')
    print(morn_output)
    print(aft_output)



def generate_days():
    """Return list of Day objects.
    
    Scrapes SailFlow for wind data, cleans the data, and stores it in a list of
    Day objects for use in analysis. 
    
    :return: list of Day objects. 
    """   
    days, hours, raw_data = sc.scrape()
    cleaned = dc.create_days(days,hours,raw_data)
    return cleaned

def get_forecast():
    """Print the forecast for the next five days.
    
    Generates a list of Day objects, analyzes them based on whether they are 
    weekdays or weekends, and prints the playability forecast. 
    
    :return: None
    """   
    days = generate_days()
    for day in days:
        if day.check_weekday() == True:
            weekday_analysis(day)
        else:
            weekend_analysis(day)        
        
if __name__ == '__main__':
    get_forecast()
