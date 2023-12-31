# -*- coding: utf-8 -*-
"""abi276_Hands_on_Data_Curation_and_ETL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ML_7AdbxZMHsKCc0VktbRz1IozfvR45u

# Hands-on 5: Data-Engineering I - Data Curation

*Note: This lab session is graded. Complete all the exercises, run your code and upload the ipynb file under assignment Hands-on5*

**Deadline is Today (02/21), 11:59 PM**

## Preamble: Python Libraries
- Collection of different modules
- Modules contain bundle of codes that can be repeatedly used in other programs
- Typically the library code are available through functions
- Some libraries are pre-installed in Anaconda and some have to be installed when you use them for the first time
- You should always check documentation and examples provided by the library
"""

# Generate a random number between 1, 100

import random

print (random.randint(1,100))

# Compute logarithm of a number

import math

print (math.log(100))
print (math.log(100, 10))

# Import only a function / object from Library

from math import log
print (log(100,10))

"""## Data Collection for Weather Analysis

Let's say we want to perform statistical analysis on weather data for EstesPark, Colorado for the month of August 2023. The data is present at the website:  https://www.estesparkweather.net/archive_reports.php?date=202308

We need to automatically scrape the website, extract relevant data, transform it and store it somewhere for further analysis.

We would need the following Python libraries :

**BeautifulSoup:** It is a powerful Python library for pulling out data from HTML/XML files. It creates a parse tree for parsed pages that can be used to extract data from HTML/XML files.

**Requests:** It is a Python HTTP library. It makes HTTP requests simpler. we just need to add the URL as an argument and the get() gets all the information from it.

**Pandas:** This is the library for loading and transforming data in Tablular format

While "requests" is available by default, we would need to install **BeautifulSoup and Pandas**.

## 0. Open the website and look at the source

1. Goto : https://www.estesparkweather.net/archive_reports.php?date=202308 (This is the data for the month of August 2023).
2. Check the page carefully, what kind of data do you need to extract? What kind of values do they contain? Will the data help in your analysis going forward?
3. Check the source (Typically RightClick->View Page Source). Where is your data of interest in the source? What HTML schema/format does data follow?

## 1. Import libraries (install if needed)
"""

# Check if beautifulsoup and pandas are already installed
# If not, install it and then import

try:
    from bs4 import BeautifulSoup
    import pandas
    print ("BeautifulSoup and Pandas are already installed and imported")
except:
    import sys
    !conda install --yes --prefix {sys.prefix} bs4
    !conda install --yes --prefix {sys.prefix} pandas
    from bs4 import BeautifulSoup
    import pandas
    print ("BeautifulSoup and Pandas were not found. Installed them and imported")

import requests

"""## 2. Read the webpage and parse it with BeautifulSoup"""

opened_webpage = requests.get("https://www.estesparkweather.net/archive_reports.php?date=202308")
print ("Webpage opened successfully...")

# Initialize a BeautifulSoup object to read and parse the webpage read
# This is like calling the __init__ function in BeautifulSoup
bs = BeautifulSoup(opened_webpage.content, "html.parser")
print ("Webpage loaded and parsed successfully...")

"""## 3. Perform ETL

In the previous class, we discussed ETL, which is a popular data pipeline paradigm. Briefly, the steps are:

**a. Extract:** Get Data from Different Sources Efficiently

**b. Transform:** Perform transformations / calculations on data

**c. Load:** Load the data into the target storage

### 3.1. Extract

Let's extract the data of our interest from the webpage. See, how we are
"""

# Define an empty list where the data will be kept
raw_data = []

# Find all the tables in the webpage page that we have just parsed
table = bs.find_all("table")

for row in table:
    line = row.text
    raw_data.append(line)

print(raw_data)

"""### 3.2. Transform

As we can see, the data is not in a great shape. But the good news is that we have everything in the form of a list. We can now use basic python operations that we discussed in the first and second hands-on to transform our data

But before that, let's ask this question. In what way I could transform the data so that it could be useful for further analysis?

Well, we wish we had the data in the following table format...

![Screenshot%202023-02-07%20at%204.04.44%20PM.png](attachment:Screenshot%202023-02-07%20at%204.04.44%20PM.png)

In general, a good file format to save this kind of tabular data is **Comma Separated Values (CSV)**

Now let's work towards transforming our data. Our steps could be:

- Define a list of columns and store the column names in the list
- Extract one row from raw data at a time, make a dictionary (key-value pair) out of it, where the keys are the column names and values are the entries
- Convert the data into a dataframe (which is kind of a table object) so that we could do some cleaning and apply additional transformation operations
"""

column_names = ["Average and Extremes", "Average temperature",
           "Average humidity","Average dewpoint",
           "Average barometer","Average windspeed",
           "Average gustspeed","Average direction",
           "Rainfall for month","Rainfall for year",
           "Maximum rain per minute","Maximum temperature",
           "Minimum temperature","Maximum humidity",
           "Minimum humidity","Maximum pressure",
           "Minimum pressure","Maximum windspeed",
           "Maximum gust speed","Maximum heat index"]

final_data = []

for l in raw_data:
    entries = l.split("\n")
    row = {} # empty dictionary for every row
    for entry in entries:
        for column_name in column_names:
            if column_name in entry:
                entry = entry.replace(column_name,"")
                row[column_name] = entry
                break # stops the inner loop here because we already find a match
    final_data.append(row)

# Sanity check - let's print the first 5 rows
print(final_data[:5])

"""#### Convert to DataFrame

A DataFrame is a data structure that organizes data into a 2-dimensional table of rows and columns, much like a spreadsheet. DataFrames are one of the most common data structures used in modern data analytics because they are a flexible and intuitive way of storing and working with data.

We use **Pandas** to convert our data into dataframe
"""

final_data = pandas.DataFrame(final_data)

# Print a few elements in the dataframe
final_data

"""At this point we have transformed our data into a decent form. We can choose to store it or do a bit more cleaning and then store.

Some basic cleaning that we can do:

- Does the data contain any duplicate rows? If yes, remove them.
- Does the data contain any NULL entries? If yes, then replace the entry with a default value (we can even remove the row completely).

And some basic statistical analysis before storing the data

#### Duplication Checks and Cleaning
"""

number_of_duplicates = final_data.duplicated().sum()
print (f" Number of duplicates before : {number_of_duplicates}")

# Delete duplicate rows
final_data = final_data.drop_duplicates()

number_of_duplicates = final_data.duplicated().sum()
print (f" Number of duplicates after removing : {number_of_duplicates}")

"""#### Inspecting data and checking noisy entries"""

final_data.info()

"""We can see that the data has 33 rows overall and but 32 non-null entries. Let's delete the row with NULL entries"""

final_data = final_data.dropna()
final_data

"""**[Additional Transformations]** We can remove unnecessary strings (e.g. "F" for fahrenheit) and "%" Symbol and convert these columns into integer/float

"""

# Define a function for cleaning
def clearn_string_and_convert(s):
    s = s.replace("%","")
    s = s.replace("°F","")
    s = s.replace("in.","")
    s = s.replace("mph","")
    # s = s.split(" ")
    converted = float(s)
    return converted

final_data["Average temperature"] = final_data["Average temperature"].apply(clearn_string_and_convert)
final_data["Average humidity"] = final_data["Average humidity"].apply(clearn_string_and_convert)
final_data["Average dewpoint"] = final_data["Average dewpoint"].apply(clearn_string_and_convert)
final_data["Average barometer"] = final_data["Average barometer"].apply(clearn_string_and_convert)
final_data["Average windspeed"] = final_data["Average windspeed"].apply(clearn_string_and_convert)
final_data["Average gustspeed"] = final_data["Average gustspeed"].apply(clearn_string_and_convert)

final_data

"""**[Optional]** Describe some of your columns"""

final_data["Average temperature"].describe()

"""**[Optional]** Plot a histogram of a column"""

hist = final_data["Average temperature"].hist(bins=5)

"""We will look into visualizations in the next hands-on

### 3.3 Load

Now, let's store the DataFrame table that we created on our local disk so that we can use it later. We choose to convert it to a CSV format. It is quite simple with Pandas dataframes.
"""

final_data.to_csv("EstesPark_Weather_January_2023.csv")

"""## Exercise E1: ETL data for January 2023

- Repeat the steps shown in section 2 and 3 above for January 2006.
- Extract January 2006 data from https://www.estesparkweather.net/archive_reports.php?date=200601
- Perform transform steps in the same way as shown in 3.2 and save the data on your laptop.
- Describe "Average temperature" using `describe()` function shown under 3.2. What differences do you see between August 2023 and January 2023.
- **Optional**: Try the same exercise for an earlier month (say a month in 2006). What difference in statistics do you see. Can you say that global warming is real based on the data?
"""

#imports
import requests
import pandas
from bs4 import BeautifulSoup

#process for cleaning data
def clearn_string_and_convert(s):
    s = s.replace("%","")
    s = s.replace("°F","")
    s = s.replace("in.","")
    s = s.replace("mph","")
    # s = s.split(" ")
    converted = float(s)
    return converted


#acess the website (source code)
opened_webpage=requests.get("https://www.estesparkweather.net/archive_reports.php?date=202301")
bs = BeautifulSoup(opened_webpage.content, "html.parser")
#save only the tables from the website
raw_data=[]
table=bs.find_all("table")
for row in table:
  line=row.text
  raw_data.append(line)
#break up the different parts of the table into rows and coloums
column_names = ["Average and Extremes", "Average temperature",
           "Average humidity","Average dewpoint",
           "Average barometer","Average windspeed",
           "Average gustspeed","Average direction",
           "Rainfall for month","Rainfall for year",
           "Maximum rain per minute","Maximum temperature",
           "Minimum temperature","Maximum humidity",
           "Minimum humidity","Maximum pressure",
           "Minimum pressure","Maximum windspeed",
           "Maximum gust speed","Maximum heat index"]
final_data=[]
for i in raw_data:
  entries=i.split("\n")
  row={}
  for entry in entries:
      for column_name in column_names:
        if column_name in entry:
          entry=entry.replace(column_name,"")
          row[column_name]=entry
          break
  final_data.append(row)
#tranform into a data table display
final_data = pandas.DataFrame(final_data)
#clean data (remove any unessacry symbols, make numbers operatable, remove null values, etc.)
final_data = final_data.drop_duplicates()
final_data = final_data.dropna()
final_data["Average temperature"] = final_data["Average temperature"].apply(clearn_string_and_convert)
final_data["Average humidity"] = final_data["Average humidity"].apply(clearn_string_and_convert)
final_data["Average dewpoint"] = final_data["Average dewpoint"].apply(clearn_string_and_convert)
final_data["Average barometer"] = final_data["Average barometer"].apply(clearn_string_and_convert)
final_data["Average windspeed"] = final_data["Average windspeed"].apply(clearn_string_and_convert)
final_data["Average gustspeed"] = final_data["Average gustspeed"].apply(clearn_string_and_convert)
#display a information about the average temperture column
final_data["Average temperature"].describe()

"""## [Optinal] Exercise E2: Commit and push this ipynb file into your github repository

After completing E1, add, commit and push this ipynb file into your github repository that you created in Hands_on4. Share your github link in the comment secion of the assignment in Canvas.

## Question: How much extra time did you need?
"""