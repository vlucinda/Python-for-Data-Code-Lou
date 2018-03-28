# Python-for-Data-Code-Lou

First, a thank you to our wonderful mentors who always welcomed questions and were generous with encouragement.  I am optimistic about my ability to learn thanks to my time with you.

Description of Project

My Python for data project utilizes publically accessible data from the Louisville Metro Police Department held in a csv file.  The csv file lists 2017 Crime Stats in the Louisville Metro Area. The data includes a row for each instance that a crime occured that year.  It also includes many (~1725) older 'cold' cases that officers worked on in 2017. I edited out in pre-2017 cases in my visualization and analysis.  I was able to sum the total crimes that occured on a given date and visualize the crime rate over the course of 2017.

The project uses SQLite to create a database of the file's contents and Bokeh to visualize it. I used Jupyter Notebook for coding.

The file's path changes weekly, so if the code doesn't work properly, the problem can be remedied by changing the last digit from a 0 to a 1 or vice versa. I have made a comment in the file to aid users.  I also discovered that jupyter notebooks must be started as: jupyter notebook --NotebookApp.iopub_data_rate_limit=10000000 in the command line in order to avoid errors related to data limits.

That crime goes up during a full moon is a belief held by many.  I have heard numerous service industry employees and police officers insist that this assertion is true.  My goal with this project was to look at the crime rate over the course of the year 2017 and see if the data reflected this common belief. 

Analysis
