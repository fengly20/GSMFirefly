#%%
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import time 

#%%
url = 'https://www.recreation.gov/camping/campgrounds/232487/availability'

#%%
#driver = webdriver.Safari()
#driver = webdriver.Chrome('/path_to_driver/chromedriver')
driver = webdriver.Firefox(executable_path='/path_to_driver/geckodriver')
driver.get(url) 
time.sleep(4)
element = driver.find_element_by_id('single-date-picker')
element.send_keys('05/31/2019')

loadmore_button = driver.find_element_by_class_name('load-more-btn')
#loadmore_button = driver.find_element_by_class_name('rec-button-tertiary-alt.load-more-btn')
loadmore_button.location_once_scrolled_into_view
loadmore_button.click()
loadmore_button.location_once_scrolled_into_view
loadmore_button.click()
loadmore_button.location_once_scrolled_into_view
loadmore_button.click()
loadmore_button.location_once_scrolled_into_view
loadmore_button.click()
loadmore_button.location_once_scrolled_into_view
loadmore_button.click()
loadmore_button.location_once_scrolled_into_view
loadmore_button.click()
loadmore_button.location_once_scrolled_into_view
loadmore_button.click()
loadmore_button.location_once_scrolled_into_view
loadmore_button.click()
time.sleep(4)

tb = driver.find_element_by_id('availability-table')
soup = BeautifulSoup(tb.get_attribute('outerHTML'),features="lxml")
tb = soup.find_all('table')[0]
driver.close()

#%%
df = pd.read_html(str(tb), header=0)[0]
df = df.drop(columns=['Loop'])
df = df.replace('R', np.nan)
df = df.replace('X', np.nan)
df = df.dropna(thresh=2)
nrow = len(df.index)

#%%
if nrow > 0:
    SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    creds = None
    
    if os.path.exists('/path_to_token/token.pickle'):
        with open('/path_to_token/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/path_to_credentials/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('/path_to_token/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('gmail', 'v1', credentials=creds)
    
    message_text = 'www.recreation.gov/camping/campgrounds/232487/availability'
    message = MIMEText(message_text)
    message['to'] = 'towhom@xx.xx'
    message['from'] = 'fromwhom@gmail.com'
    message['subject'] = 'Campsite available'
    message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    service.users().messages().send(userId='fromwhom@gmail.com', body=message).execute()
        