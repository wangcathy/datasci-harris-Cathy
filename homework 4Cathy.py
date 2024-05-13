# PPHA 30537
# Spring 2024
# Homework 4

# Cathy

# Cathy Wang
# WangCathy

# Due date: Sunday May 12th before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.

##################

# Question 1: Explore the data APIs available from Pandas DataReader. Pick
# any two countries, and then 
#   a) Find two time series for each place
#      - The time series should have some overlap, though it does not have to
#        be perfectly aligned.
#      - At least one should be from the World Bank, and at least one should
#        not be from the World Bank.
#      - At least one should have a frequency that does not match the others,
#        e.g. annual, quarterly, monthly.
#      - You do not have to make four distinct downloads if it's more appropriate
#        to do a group of them, e.g. by passing two series titles to FRED.


#   b) Adjust the data so that all four are at the same frequency (you'll have
#      to look this up), then do any necessary merge and reshaping to put
#      them together into one long (tidy) format dataframe.


#   c) Finally, go back and change your earlier code so that the
#      countries and dates are set in variables at the top of the file. Your
#      final result for parts a and b should allow you to (hypothetically) 
#      modify these values easily so that your code would download the data
#      and merge for different countries and dates.
#      - You do not have to leave your code from any previous way you did it
#        in the file. If you did it this way from the start, congrats!
#      - You do not have to account for the validity of all the possible 
#        countries and dates, e.g. if you downloaded the US and Canada for 
#        1990-2000, you can ignore the fact that maybe this data for some
#        other two countries aren't available at these dates.


#   d) Clean up any column names and values so that the data is consistent
#      and clear, e.g. don't leave some columns named in all caps and others
#      in all lower-case, or some with unclear names, or a column of mixed 
#      strings and integers. Write the dataframe you've created out to a 
#      file named q1.csv, and commit it to your repo.

import pandas as pd
from pandas_datareader import wb, data as pdr
import datetime

COUNTRIES = ['BRA', 'JPN']  
INDICATORS = {
    'GDP': 'NY.GDP.PCAP.CD',  
    'CPI': {'BRA': 'BRACPIALLMINMEI', 'JPN': 'JPNCPIALLMINMEI'}  
}
START_DATE = datetime.datetime(2010, 1, 1)
END_DATE = datetime.datetime(2020, 12, 31)

def download_wb_data(country, indicator, start, end):
    data = wb.download(indicator=indicator, country=[country], start=start.year, end=end.year)
    data.reset_index(inplace=True)
    data['year'] = pd.to_datetime(data['year'], format='%Y').dt.to_period('Y').dt.to_timestamp()
    return data

def download_fred_data(series_code, start, end):
    data = pdr.DataReader(series_code, 'fred', start, end)
    data = data.resample('A').mean().reset_index()
    data['DATE'] = pd.to_datetime(data['DATE']).dt.to_period('Y').dt.to_timestamp()
    return data

data_frames = {}
for country in COUNTRIES:
    gdp_data = download_wb_data(country, INDICATORS['GDP'], START_DATE, END_DATE)
    cpi_data = download_fred_data(INDICATORS['CPI'][country], START_DATE, END_DATE)
    combined = pd.merge(gdp_data, cpi_data, how='left', left_on='year', right_on='DATE')
    data_frames[f'gdp_cpi_{country}'] = combined

final_df = pd.concat(data_frames.values(), axis=1)
final_df.columns = [col if 'country' not in col else col.split('_')[0] for col in final_df.columns]
final_df.drop(columns=['country', 'DATE'], axis=1, inplace=True)

final_df.to_csv('q1.csv', index=False)
print(final_df)


# Question 2: On the following Harris School website:
# https://harris.uchicago.edu/academics/design-your-path/certificates/certificate-data-analytics
# There is a list of six bullet points under "Required courses" and 12
# bullet points under "Elective courses". Using requests and BeautifulSoup: 
#   - Collect the text of each of these bullet points
#   - Add each bullet point to the csv_doc list below as strings (following 
#     the columns already specified). The first string that gets added should be 
#     approximately in the form of: 
#     'required,PPHA 30535 or PPHA 30537 Data and Programming for Public Policy I'
#   - Hint: recall that \n is the new-line character in text
#   - You do not have to clean up the text of each bullet point, or split the details out
#     of it, like the course code and course description, but it's a good exercise to
#     think about.
#   - Using context management, write the data out to a file named q2.csv
#   - Finally, import Pandas and test loading q2.csv with the read_csv function.
#     Use asserts to test that the dataframe has 18 rows and two columns.

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://harris.uchicago.edu/academics/design-your-path/certificates/certificate-data-analytics'

response = requests.get(url)
response.raise_for_status()  

soup = BeautifulSoup(response.text, 'html.parser')

csv_doc = ['type,description']

def extract_courses(section_title):
    courses = []
    heading = soup.find('h3', string=section_title)  
    if heading:
        element = heading.next_sibling
        while element and element.name != 'h3':  
            if element.name == 'ul':  
                courses.extend([li.get_text(strip=True) for li in element.find_all('li')])
            element = element.next_sibling
    return courses

required_courses = extract_courses('Required courses')
elective_courses = extract_courses('Elective courses')

for item in required_courses:
    csv_doc.append(f"required,{item}")

for item in elective_courses:
    csv_doc.append(f"elective,{item}")

df = pd.DataFrame([x.split(',', 1) for x in csv_doc], columns=['Type', 'Course'])
df.to_csv('q2.csv', index=False)
df_test = pd.read_csv('q2.csv')
print(df_test)


