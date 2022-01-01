# Wind Forecast Webscraping

As a beach volleyball player, I often need to know what the wind forecast will be. SailFlow.com is easily the best wind foreacast service I have used.  
Since I check it frequently--opening the page, scrolling through the week, evaluating the wind speeds, and remembering the conditions--and the process of doing so
ends up taking a lot of time, I want to automate the process.  As SailFlow does not offer an API, the best option is to resort
to webscraping. This application is a command line script that uses Selenium for Python to scrape web data from SailFlow and print out
a playable/not-playable verdict for the next five days.  The script uses my general guidelines for determining playability: days with 
average winds more than 25mph or gusts greater than 25mph are considered unplayable, while anything else is considered playable.  

## Installation

- Ensure Python 3.7 is installed on your computer.  
- Ensure the appropriate version of Selenium for Python is installed. 
- Clone this repository to your computer.  
- Install Google Chrome and note version number.  
- Open a web browser and navigate to https://sites.google.com/chromium.org/driver/downloads
- Download the Chromedriver appropriate for your version of Chrome.  
- Extract the chromedriver.exe file to a convenient location on your hard drive.  Note the path. 

## Configuration

- Open a web browser and navigate to https://www.sailflow.com/map#38.633,-106.047,4,1
- Find a weather station closest to your favorate beach volleyball location. 
- Click Forecast-> Complete Report
- Copy the url.  It should be in the format 'sailflow.com/spot/######'
- In the project folder, open 'scraper.py'
- Set 'target' variable to the SailFlow url you copied. 
- Set the 'PATH' variable to the location of the chromedriver.exe file.  
- Save and close the file. 

## Usage

- Run 'forecaster.py' in a terminal.  A new Chrome window will briefly open and close before the output is displayed in the terminal.  

## Future Improvements

This is very much a tool I personally use extremely frequently, is very much tailored to my needs, and is very rough around the edges. 
It works well as a data gathering tool, but wasn't originally designed to be user-friendly.  Improvements would take the form of quality
of life improvements for users:

- Create a UI to display data.  
- Integrate a location/zip code search into UI. 
- Add configuration tools (set custom playability conditions) to UI.  
