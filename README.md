# Strava-Analysis

Dependencies<br>
• Selenium(https://selenium-python.readthedocs.io/installation.html)<br>
• requests<br>

Functionality:

To perform <b>analysis</b> go to the Analysis folder

Run python Analysis/analyse.py --help

<b>To scrape data from strava</b>
<ul>
<b>Step 1.</b> Login to strava to set login cookies

Run python Data and Scraping/scraper.py login


<b>Step 2.</b> Scrape data with given athlete name and athlete id. 

Example - python scraper.py Download "Alex Dowsett" /pros/505408

Tip - Strava implements rate limiting. As a result, all the data may not be fetched, by using the above command. Set the above command as a cron job every few hours to fetch all of the data.

</ul>
