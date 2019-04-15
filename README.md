# GSMFirefly

## brief

A routine I used for monitoring campsite availability in Elkmont Campground, TN. An email (using Gmail API) will be sent to user once campsites are available. 

Hard-coded parameters buried in the code file -- use caution when making changes, including but not limited to, campsite id (the url), start date, from/to in email settings, and all paths. 

Python version is 3.6. A few more libraries are needed: `selenium`, `BeautifulSoup`, `pandas`, `numpy`. 

Since using Gmail API, the Google authentication related libraries are needed, refere [this link](https://developers.google.com/gmail/api/quickstart/python) for details and get-started guide. The `credentials.json` has to exist as well.  

Since using `Selenium` to inspect dynamic pages, a `webdriver` is needed. Refers to known issues for webdriver selection.  


# known issues 

* The Firfox webdriver `geckodriver` is used in the main routine. `safaridriver` that came with the MacOS works fine when testing but produces error when running as cron job (for me). `chromedriver` seems to fail when doing the page navigating. 

# set up cron job in MacOS 

In terminal, type 

```bash
$ env EDITOR=nano crontab -e
```

Add a line as: 

```
*/2 * * * * /path_to_python/python /path_to_script/main.py
```

Then save the file. 

`*/2` means running the script every 2 minitues. 

Use the line to check your cron jobs:

```
$ crobtab -l
```
