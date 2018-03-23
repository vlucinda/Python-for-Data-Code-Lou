
# coding: utf-8

# In[30]:


import sqlite3
import re
import requests
import csv
#pandas are for truncating unnecessary time from date/time value in csv file
import pandas as pd
#datetime sets column as datetimeindex
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
#Allows pandas to read dates in csv file's date_occured column
from math import pi
from itertools import chain
from collections import namedtuple
from bokeh.io import show, output_notebook
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, FuncTickFormatter, FixedTicker, ColumnDataSource



# In[2]:


#This is publicly accessible data, so I didn't need an authorization/key.
token = ''
header = headers = {'Content-type': 'application/json'}

#The API itself doesn't contain the data, so I'm pointing the request directly to the URL of the data file.
CSV_URL = 'https://data.louisvilleky.gov/sites/default/files/Crime_Data_2017_1.csv'

#The session request streams the downloading of files, instead of having to download them individually.
with requests.Session() as s:
    download = s.get(CSV_URL)
# Decodes data into desired format
    decoded_content = download.content.decode('utf-8')
#Takes decoded data and makes it into rows, with commas as delimiters.
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)



# In[3]:


#list of column headers in csv file
my_list[:1]


# In[4]:


#Create SQL database

#create connection to database
conn = sqlite3.connect("mydatabase.db")  
 
#cursor object allows interaction with the database    
cursor = conn.cursor()

#I used a DROP TABLE statement because I kept getting an error message that the crime_stats table already existed
cursor.execute("DROP TABLE IF EXISTS crime_stats;")
conn.commit()

# create a table--call it crime_stats
cursor.execute("""CREATE TABLE crime_stats 
(incident_number varchar(255), date_reported varchar(255), date_occured varchar(255), uor_desc varchar(255), 
crime_type varchar(255), nibrs_code varchar(255), ucr_hierarchy varchar(255), att_comp varchar(255), 
lmpd_division varchar(255), lmpd_beat varchar(255), premise_type varchar(255), block_address varchar(255), city varchar(255), 
zip_code varchar(255), id varchar(255))""")
conn.commit()

#insert multiple records; question marks indicate the number of column headings from the csv file being inserted 
crime_stats = my_list
for row in crime_stats:
    cursor.execute("INSERT INTO crime_stats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)

# Save (commit) the changes
conn.commit()


# Close the connection if we are done with it.
conn.close()


# In[9]:


#SQl queries

conn = sqlite3.connect("mydatabase.db")
# will return results in rows
cursor = conn.cursor()
 
#SQL Query 1 counts occurences in crime_type column and renames the sum crime_count; Limit 10 is for ???  
sql = "SELECT date_occured, COUNT(crime_type) as crime_count FROM crime_stats GROUP BY date_occured LIMIT 10"
#SQL Qery 2 counts occurences in crime_type column and orders them by date occured.  For some reason there are earlier dates in the 2017 file.
#Is there a way in SQL to ignore dates earlier than 2017-01-01?
sql = "SELECT date_occured, 1 as crime_count FROM crime_stats ORDER BY date_occured"
cursor.execute(sql)
#Using fetchall in lieu of fetchmany because data sample is small
results = cursor.fetchall()

print ("\nHere's a listing of all the crimes in Louisville in 2017:\n")
for row in results:
    print(row)
 


# In[61]:


#Aggregating data with Pandas 
 
import datetime
datetime
datetime.datetime 
 
#Setting dtypes because I kept getting a dtype error
dtypes = [datetime.datetime, str, float] 
df = pd.read_csv(CSV_URL, sep=',', parse_dates=True, dtype=dtypes)
df

#Use Pandas DataFrame to convert date_occured column to DateTime object
df["date_occured"] = pd.to_datetime(df["date_occured"], format='%y,%m,%d')
#Analysis is not concerned with the time that crimes occured, so I want to strip the time from the datetime object
df['date_minus_time'] = df['date_occured'].apply( lambda df : 
datetime.datetime(year=df.year, month=df.month, day=df.day))

df.set_index(df['date_minus_time'],inplace=True)
print(df.index)

#Then group by day occured
df.set_index('date_minus_time').groupby(pd.Grouper('D')).sum().dropna()
df['counts'] = df.groupby(level=0).transform('count')
df.resample('D', how={'counts': lambda x: x[0] if len(x) else 0, 
                          'label' : lambda x: list(set(x))})

# Group the data frame by date_occured extract a number of stats from each group
df.groupby(['date_occured', 'counts']).agg({'duration':sum,   # find the sum of the durations for each group
                                     'date_occured': 'count', # find the number of date_occured entries
                                          })


# In[ ]:


#Returns DateTimeIndex with times to midnight.
#pd.DatetimeIndex(df.t).normalize()




# In[ ]:


#Visualization
type(crime_stats)
#Pull the dates and stats into their own list to pass to bokeh for the different axis and plot values.
date_occured = [row[2] for row in crime_stats]
crime_type = [row[4] for row in crime_stats]

#Set to open charts in the notebook. 
output_notebook()

#what does the :10 mean?
#Every plot starts with a figure object that defines some generic information relative to the plots display
p = figure(x_range=date_occured[:10], plot_height=400, plot_width=800, title="Crimes By Date",
           toolbar_location=None, tools="")

#With a figure defined we then declare the type of chart (vbar) and then pass it the data to plot
p.vbar(x=date_occured[:10], top=crime_type[:10], width=0.9, color='#4BC246')
#We can also manipulate attribute values on our figure from above after declaration 
p.xaxis.major_label_orientation = pi/4
p.yaxis.major_label_orientation = "horizontal"
p.xgrid.grid_line_color = None
p.y_range.start = 0
#Once we have provided the data and any formatting information that's needed we can call the show function for the specific figure
show(p)

