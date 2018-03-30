
# coding: utf-8

# In[57]:


import sqlite3
import re
import requests
import csv
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
from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool, FuncTickFormatter, FixedTicker, ColumnDataSource, DatetimeTickFormatter 




# In[2]:


#This is publicly accessible data, so I didn't need an authorization/key.

#The API itself doesn't contain the data, so I'm pointing the request directly to the URL of the data file
#The path of the CSV file changes weekly.  IF the one written below doesn't run, the last digit must be changed to either 1 or 0.
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
#conn.close()


# In[5]:


#Use Pandas to further manipulate data
#pandas used for truncating unnecessary time from date/time value in csv file
import pandas as pd
#use datetime to manipulate the date and time in the date_occured column of data source
import datetime
datetime
datetime.datetime 
 
#Setting dtypes because I kept getting a dtype error
dtypes = [] 

#Converting columns in data file to DataFrame & dropping unneeded columns
df = pd.read_sql_query("SELECT date_occured, 1 as crime_count FROM crime_stats ORDER BY date_occured;", conn)
#Dropping rows of data of crimes before 2017
df = df[1725:-1]

#Pandas object column to datetime
df['updt_dt'] = pd.to_datetime(df['date_occured'])
df['updt_dt'] = df['updt_dt'].dt.date
#print(df)

df.head()
 


# In[56]:


#Visualization with Bokeh
type(df)
#Pull the dates and stats into their own list to pass to bokeh for the x,y axis values.
updt_dt = [row[-1] for row in df]
crime_count = [row[0] for row in df]

#Enable Bokeh to plot to Jupyter notebook
output_notebook()
output_file('crime_stats.html')


# In[14]:


updt_dt = df[['updt_dt']]
crime_count = df[['crime_count']]
list=['date_occured', 'crime_count', 'updt_dt', 'index'];
source= ColumnDataSource(df)
source
source.column_names


# In[53]:


#updt_dt = df[['updt_dt']].values
#crime_count = df[['crime_count']].values
#Bokeh plotting
p = figure(x_axis_label= "Date Occured", y_axis_label = "Number of Crimes", x_axis_type='datetime', x_range=['updt_dt'][:10],
           y_range=[0,100], plot_height=400, plot_width=800, title="Crimes in Louisville 2017",
           toolbar_location=None, tools="")

#p.line(df.index, df['updt_dt'])
#With a figure defined we then declare the type of chart (vbar) and then pass it the data to plot
p.line('updt_dt', 'crime_count', color='#4BC246', source=source)
p.xaxis.formatter=DatetimeTickFormatter(
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    ) 
p.xaxis.major_label_orientation = pi/4
p.yaxis.major_label_orientation = "horizontal"
p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)

