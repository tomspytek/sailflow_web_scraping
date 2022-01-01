"""Clean scraped weather data and use it to create a list of Day objects.

Classes:
    Day
    
Functions:
    create_days(list,list,list)
    
"""

import matplotlib.pyplot as plt


class Day():
    """
    Class for storing wind data for a day.
    
    Data given in 1-hr increments from 12AM to 11PM. 
    """
    
    def __init__(self,day_of_the_week='', time_list=[],
                 wind_list=[], gust_list=[], direction_list=[]):
        """Initialize the Day class."""
        self.day_of_the_week = day_of_the_week
        self.time_list = time_list
        self.wind_list = wind_list
        self.gust_list = gust_list
        self.direction_list = direction_list
        self.weekday = self.check_weekday()
    
    def check_weekday(self):
        """Return True if weekday, False if not."""
        weekdays = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
        if self.day_of_the_week in weekdays:
            return True
        else:
            return False
        
    def get_wind_data(self):
        """Return avg wind vals as list of ints."""
        return self.wind_list
    
    def get_gust_data(self):
        """Return gust vals as list of ints."""
        return self.gust_list
    
    def get_direction_data(self):
        """Return wind direction vals as list of strs."""
        return self.direction_list
    
    def get_time(self):
        """Return time vals as list of ints."""
        return self.time_list
    
    def get_day(self):
        """Return day of the week as str."""
        return self.day_of_the_week
    
    def plot_data(self):
        """Plot avg wind and gust information."""
        hours = self.time_list
        avg_wind = self.wind_list
        gusts = self.gust_list
        plt.figure(figsize=(18,3))
        plt.plot(hours,avg_wind,'b',hours,gusts,'p')
        plt.show()

    
def get_five_days(days):
    """Remove current day from days str list.
    
    Current day is always the first item in the list. 
    :param days: 1d list of strs
    :return: 1d list of strs
    """
    return days[1:6]

def convert_to_full_day_names(scraped_days):
    """Convert list of day abbreviation to list of full names.
    
    SailFlow chart uses abbreviations such as "Sun" for "Sunday," "Thu" for
    "Thursday," etc. This function converts from the abbreviation to the full 
    name.  
    :param scraped_days: 1d list of strs
    :return: 1d list of strs
    
    """
    ref = {'Mon':'Monday', 'Tue':'Tuesday', 'Wed':'Wednesday', 
           'Thu':'Thursday', 'Fri':'Friday', 'Sat':'Saturday',
           'Sun':'Sunday'}
    full_days = []
    for day in scraped_days:
        comma_loc = day.index(',')
        abbr_name = day[:comma_loc]
        full_days.append(ref[abbr_name])
    return full_days

def get_day_indices(hours):
    """Locate list index for the end of each day.
    
    :param hours: 1d list of ints
    :return: dictionary of day/int key/vals
    """ 
    today_end = hours.index('12AM')
    day1_end = hours.index('12AM', today_end+1)
    day2_end = hours.index('12AM', day1_end+1)
    day3_end = hours.index('12AM', day2_end+1)
    day4_end = hours.index('12AM', day3_end+1)
    day5_end = hours.index('12AM', day4_end+1)
    days_indices = {
        'today_end':today_end, 
        'day1_end':day1_end,
        'day2_end':day2_end, 
        'day3_end':day3_end, 
        'day4_end':day4_end, 
        'day5_end':day5_end}
    return days_indices

def divide_hours_into_days(hours, indices):
    """Divide list of hours into lists of hours for today and next five days.
    
    :param hours: 1d list of ints
    :param indices: 1d list of ints
    :return: tuple of 1d lists
    """
    #today = hours[:indices['today_end']]
     
    day1_hours = hours[indices['today_end']:indices['day1_end']]
    day2_hours = hours[indices['day1_end']:indices['day2_end']]
    day3_hours = hours[indices['day2_end']:indices['day3_end']]
    day4_hours = hours[indices['day3_end']:indices['day4_end']]
    day5_hours = hours[indices['day4_end']:indices['day5_end']]
    hours_divided = (day1_hours,day2_hours,
                     day3_hours,day4_hours,
                     day5_hours)
    return hours_divided

def divide_wind_data_into_days(wind_data_list, indices):
    """Divide list of wind speed into lists for today and next five days.
    
    :param hours: 1d list of ints
    :param indices: 1d list of ints
    :return: tuple of 1d lists
    """
    #today_data = wind_data_list[:indices['today_end']]
     
    day1_data = wind_data_list[indices['today_end']:indices['day1_end']]
    day2_data = wind_data_list[indices['day1_end']:indices['day2_end']]
    day3_data = wind_data_list[indices['day2_end']:indices['day3_end']]
    day4_data = wind_data_list[indices['day3_end']:indices['day4_end']]
    day5_data = wind_data_list[indices['day4_end']:indices['day5_end']]
    wind_data_list_divided = (day1_data,day2_data,
                              day3_data,day4_data,
                              day5_data)
    return wind_data_list_divided

def divide_data(hours,undivided_wind_data):
    """Return the hours and wind data divided into days.
    
    :param hours: 1d list of ints
    :param undivided_wind_data: 1d list of ints
    :return: tuple of two tuples of 1d lists
    """
    indices = get_day_indices(hours)
    divided_hours = divide_hours_into_days(hours,indices) #tuple
    divided_wind_data = divide_wind_data_into_days(
        undivided_wind_data, indices)#tuple
    
    return divided_hours, divided_wind_data

def extract_avg_wind(avg_gust_dir):
    """Extract and return the average wind val from scraped SailFlow string.
    
    avg_gust_dir is a str with format 'avg wind val (gust val) mph direction'.
    Extract just the avg wind val. 
    :param avg_gust_dir: str
    :return: int
    """
    avg_start = avg_gust_dir.index(' ')
    avg_end = avg_gust_dir.index('(')
    avg_wind_str = avg_gust_dir[avg_start+1:avg_end]
    avg_wind_int = int(avg_wind_str)
    return avg_wind_int

def extract_gusts(avg_gust_dir):
    """Extract and return the gust val from scraped SailFlow string.
    
    avg_gust_dir is a str with format 'avg wind val (gust val) mph direction'.
    Extract just the gust val. 
    :param avg_gust_dir: str
    :return: int
    """
    paren_start = avg_gust_dir.index('(')
    paren_end = avg_gust_dir.index(')')
    paren = avg_gust_dir[paren_start+1:paren_end]
    gust_start = paren.rindex(' ')
    gust_str = paren[gust_start+1:]
    gust_int = int(gust_str)
    return gust_int

def extract_direction(avg_gust_dir):
    """Extract and return the wind direction from scraped SailFlow string.
    
    avg_gust_dir is a str with format 'avg wind val (gust val) mph direction'.
    Extract just the wind direction. 
    :param avg_gust_dir: str
    :return: int
    """
    direction_start = avg_gust_dir.rindex(' ')
    direction = avg_gust_dir[direction_start+1:]
    return direction    

def clean_wind_data(avg_gust_dir):
    """Return cleaned average wind, gust, and direction data.
    
    Use the extract_* functions to extract the wind, gust, and direction data
    from the str scraped from SailFlow. 
    avg_gust_dir is a str with format 'avg wind val (gust val) mph direction'.
    :param avg_gust_dir: 1d list of strs
    :return: tuple of 1d lists of ints
    """
    avg = []
    gust = []
    direction = []
    for data_str in avg_gust_dir:
        avg.append(extract_avg_wind(data_str))
        gust.append(extract_gusts(data_str))
        direction.append(extract_direction(data_str))
    return avg, gust, direction 

def create_days(d,h,rd):
    """Create and return list of Day objects.
    
    :param d: 1d list of strs
    :param h: 1d list of strs
    :param rd: 1d list of strs
    :return: 1d list of Days
    """    
    days = d
    hours = h
    undivided_wind_data = rd
    
    days_list = get_five_days(days)
    full_day_names = convert_to_full_day_names(days_list)   
    #breaking apart hours and wind_data into each day--indexed by day  
    divided_data = divide_data(hours, undivided_wind_data) 
    divided_hours = divided_data[0]
    divided_wind = divided_data[1]
    output_days = [] 
    for i in range(len(full_day_names)):  
        day_of_the_week = full_day_names[i]
        time_list = divided_hours[i]
        clean_wind = clean_wind_data(divided_wind[i])     
        avg_wind_list = clean_wind[0]
        gust_list = clean_wind[1]
        direction_list = clean_wind[2]  
        current_day = Day(day_of_the_week = day_of_the_week, 
                         time_list = time_list, wind_list = avg_wind_list,
                         gust_list = gust_list,
                         direction_list = direction_list) 
        output_days.append(current_day)
    return output_days
    














    