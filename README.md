# strava-scraper

Dependencies<br>

A Firefox browser and geckodriver installed

Python dependencies
```
pip install -r requirements.txt
```

<b>To scrape data from strava</b>

<b>Step 1.</b> Login to strava to set login cookies

```
python <path-to-repo>/scraper login
```
==be sure to check the 'remember me' box before logging in.==


<b>Step 2.</b>

Load all activity ids of a strava athlete, with the athlete's name and strava athlete id(from the url after "https://strava.com/")
Example:
```
python scraper.py collect -n "Alex Dowsett" -i /pros/505408
```

== This step may take a while ==
<b>Step 3.</b> Scrape data with the athlete's name and athlete id. 

Example:
```
python scraper.py download "Alex Dowsett" /pros/505408
```

The data is saves in the "data" folder, under the athlete's name.


Tip - Strava implements rate limiting. As a result, all the data may not be fetched, by using the above command. Set the above command as a cron job every few hours to fetch all of the data.
