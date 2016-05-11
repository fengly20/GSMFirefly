#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
@script name: main.py 
@author: Leyang Feng
@date last updated: 
@purpose: 
@note: 
@TODO:

"""

# -----------------------------------------------------------------
# 0. standard import
from __future__ import print_function
import re
import urllib2
import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import base64
import email

# -----------------------------------------------------------------
# 1. construct the urls and url reading stuff 
url_date = '6/03/2016'
url = 'http://www.recreation.gov/campsiteCalendar.do?page=matrix&contractCode=NRSO&parkId=70968&calarvdate=' + url_date
hdr = {'User-Agent': 'Mozilla/5.0'}

# -----------------------------------------------------------------
# 2. read in the url 
# read the page and convert to line by line text
request = urllib2.Request( url, headers = hdr )
response = urllib2.urlopen( request )    
html = response.read() 
html = html.splitlines() 
    
# -------------------------------------------------------------
# 3. find the campsite name line
# how it works: first I find the campsite name line, extract campsite name from that line. 
# then I know the infor I want is in the following 3 lines, so I save next lines into another list
campsite_name_line_index_list = []    
reg_pattern = '<div class=\'siteListLabel'
for line in html:
    reg_results = re.search( reg_pattern, line )
    if reg_results:
        line_index = html.index( line )
        campsite_name_line_index_list.append( line_index )
# extract campsite name
campsite_name_list = []
reg_pattern = r'>....</a>'
for index in campsite_name_line_index_list:
    reg_results = re.search( reg_pattern, html[ index ] )
    if reg_results:
        campsite_name = reg_results.group()
        campsite_name = campsite_name[ 1 : 5 ]
        campsite_name_list.append( campsite_name )

# ------------------------------------------------------------
# 4. extract the lines contains availability info 
# if the campsite name line index = i, I only wanted i+3, i+4, i+5. due to the structure of the page. 
fri_line_index_list = []
sat_line_index_list = []
sun_line_index_list = []
for index in campsite_name_line_index_list:
    line_1 = index + 3
    fri_line_index_list.append( line_1 )
    line_2 = index + 4
    sat_line_index_list.append( line_2 )
    line_3 = index + 5
    sun_line_index_list.append( line_3 )

msg_list = []
for i in range( 0, len( campsite_name_list ) ):
    fri_line_index = fri_line_index_list[ i ]        
    fri_line = html[ fri_line_index ]
    fri_line_length = len( fri_line )
    if fri_line_length > 35:
        msg = 'Site ' + campsite_name_list[ i ] + ' on Fri is available !'
        msg_list.append( msg )
        
    sat_line_index = sat_line_index_list[ i ]        
    sat_line = html[ sat_line_index ]
    sat_line_length = len( sat_line )
    if sat_line_length > 35:
        msg = 'Site ' + campsite_name_list[ i ] + ' on Sat is available !'
        msg_list.append( msg )
        
    sun_line_index = sun_line_index_list[ i ]        
    sun_line = html[ sun_line_index ]
    sun_line_length = len( sun_line )
    if sun_line_length > 35:
        msg = 'Site ' + campsite_name_list[ i ] + ' on SUN is available !'
        msg_list.append( msg )
print( msg_list )
# -----------------------------------------------------------
# 5. if there are available sites send a email
if len( msg_list ) > 0:
    
    # set up the auth process
    SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    CLIENT_SECRET_FILE = 'client_secret.json'
    credential_path = 'toYourClientJason/client_secret.json'
    store = oauth2client.file.Storage( credential_path )
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    credentials = tools.run_flow( flow, store )
    
    # build a gmail service
    http = credentials.authorize( httplib2.Http() )
    gmail = discovery.build( 'gmail', 'v1', http=http )
    
    # construct the message
    message_text = 'check the page \n http://www.recreation.gov/campsiteCalendar.do?page=calendar&contractCode=NRSO&parkId=70968&calarvdate=06/03/2016&sitepage=true&startIdx=0'
    to = 'xxxxx'
    sender = 'xxxxx'
    subject = 'Campsite available'    
    message = email.mime.Text.MIMEText( message_text )
    message[ 'to' ] = to
    message[ 'from' ] = sender
    message[ 'subject' ] = subject
    message = { 'raw': base64.urlsafe_b64encode( message.as_string() ) }   
    
    # end the message
    gmail.users().messages().send(userId=sender, body=message).execute()
    
    
    

    
    

    