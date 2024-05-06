# PPHA 30537
# Spring 2024
# Homework 3

# Cathy Wang

# Cathy Wang
# wangcathy

# Due date: Sunday May 5th before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.

##################

#NOTE: All of the plots the questions ask for should be saved and committed to
# your repo under the name "q1_1_plot.png" (for 1.1), "q1_2_plot.png" (for 1.2),
# etc. using fig.savefig. If a question calls for more than one plot, name them
# "q1_1a_plot.png", "q1_1b_plot.png",  etc.

# Question 1.1: With the x and y values below, create a plot using only Matplotlib.
# You should plot y1 as a scatter plot and y2 as a line, using different colors
# and a legend.  You can name the data simply "y1" and "y2".  Make sure the
# axis tick labels are legible.  Add a title that reads "HW3 Q1.1".

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
#1.1
plt.savefig("HW3_Q1_1.png")

x = pd.date_range(start='1990/1/1', end='1991/12/1', freq='MS')
y1 = np.random.normal(10, 2, len(x))  
y2 = np.sin(x.day) + 10  
fig, ax = plt.subplots()
ax.scatter(x, y1, color='blue', label='Scatter (y1)')  
ax.plot(x, y2, color='red', label='Line (y2)')  
ax.legend()
ax.set_xlabel('Date')
ax.set_ylabel('Values')
ax.set_title('Plot of y1 and y2 over Time')
plt.gcf().autofmt_xdate() 

plt.show()

# Question 1.2: Using only Matplotlib, reproduce the figure in this repo named
# question_2_figure.png.
x_values = range(10, 19)  

y_values_blue = [x + 2 for x in x_values]  
y_values_red = [-x + 32 for x in x_values]  

plt.figure(figsize=(6, 4))  
plt.plot(x_values, y_values_blue, label='Blue', color='blue')  
plt.plot(x_values, y_values_red, label='Red', color='red') 
plt.title('X marks the spot')  
plt.xlabel('X axis') 
plt.ylabel('Y axis') 
plt.legend()  
plt.show()

# Question 1.3: Load the mpg.csv file that is in this repo, and create a
# plot that tests the following hypothesis: a car with an engine that has
# a higher displacement (i.e. is bigger) will get worse gas mileage than
# one that has a smaller displacement.  Test the same hypothesis for mpg
# against horsepower and weight.

import statsmodels.formula.api as smf

mpg_data = pd.read_csv('/Users/mac/Downloads/mpg.csv')

mpg_data.dropna(subset=['mpg', 'displacement', 'horsepower', 'weight'], inplace=True)
model = smf.ols('mpg ~ displacement + horsepower + weight', data=mpg_data).fit()
plt.scatter(mpg_data['weight'], mpg_data['mpg'], color='blue', label='Actual MPG')
predicted_mpg = model.predict(mpg_data[['displacement', 'horsepower', 'weight']])
plt.plot(mpg_data['weight'], predicted_mpg, 'r-', label='Predicted MPG')
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.title('MPG vs Weight with Regression Line')
plt.legend()
plt.show()

# Question 1.4: Continuing with the data from question 1.3, create a scatter plot 
# with mpg on the y-axis and cylinders on the x-axis.  Explain what is wrong 
# with this plot with a 1-2 line comment.  Now create a box plot using Seaborn
# that uses cylinders as the groupings on the x-axis, and mpg as the values
# up the y-axis.

mpg_data = pd.read_csv('/Users/mac/Downloads/mpg.csv')
plt.scatter(mpg_data['cylinders'], mpg_data['mpg'])
plt.xlabel('Cylinders')
plt.ylabel('MPG')
plt.title('MPG vs Cylinders')
plt.show()
#The scatter plot displays mpg values across different cylinder counts. 
#This graph reveals that as the number of cylinders increases, mpg tends to decrease.
sns.boxplot(x='cylinders', y='mpg', data=mpg_data)
plt.title('MPG Distribution by Cylinder Count')
plt.show()
fig.savefig('mpg_relationships.png') 
# Question 1.5: Continuing with the data from question 1.3, create a two-by-two 
# grid of subplots, where each one has mpg on the y-axis and one of 
# displacement, horsepower, weight, and acceleration on the x-axis.  To clean 
# up this plot:
#   - Remove the y-axis tick labels (the values) on the right two subplots - 
#     the scale of the ticks will already be aligned because the mpg values 
#     are the same in all axis.  
#   - Add a title to the figure (not the subplots) that reads "Changes in MPG"
#   - Add a y-label to the figure (not the subplots) that says "mpg"
#   - Add an x-label to each subplot for the x values
# Finally, use the savefig method to save this figure to your repo.  If any
# labels or values overlap other chart elements, go back and adjust spacing.
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

axs[0, 0].scatter(mpg_data['displacement'], mpg_data['mpg'])
axs[0, 0].set_xlabel('Displacement')

axs[0, 1].scatter(mpg_data['horsepower'], mpg_data['mpg'])
axs[0, 1].set_xlabel('Horsepower')

axs[1, 0].scatter(mpg_data['weight'], mpg_data['mpg'])
axs[1, 0].set_xlabel('Weight')

axs[1, 1].scatter(mpg_data['acceleration'], mpg_data['mpg'])
axs[1, 1].set_xlabel('Acceleration')

for ax in axs.flat:
    ax.label_outer()

fig.suptitle('Changes in MPG')
plt.show()

# Question 1.6: Are cars from the USA, Japan, or Europe the least fuel
# efficient, on average?  Answer this with a plot and a one-line comment.

average_mpg = mpg_data.groupby('origin')['mpg'].mean()
average_mpg.plot(kind='bar')
plt.ylabel('Average MPG')
plt.title('Fuel Efficiency by Country')
plt.show()
#"The bar chart shows that the average fuel efficiency of American cars 
#is lower than that of Japanese and European cars
#demonstrating significant regional differences in vehicle efficiency.

# Question 1.7: Using Seaborn, create a scatter plot of mpg versus displacement,
# while showing dots as different colors depending on the country of origin.
# Explain in a one-line comment what this plot says about the results of 

sns.scatterplot(x='displacement', y='mpg', hue='origin', data=mpg_data)
plt.title('MPG vs Displacement by Origin')
plt.show()

#The different colored dots illustrate how the country of origin affects
# a car's displacement and fuel efficiency, further confirming that American
# cars tend to have higher displacement and lower fuel efficiency.


# Question 2: The file unemp.csv contains the monthly seasonally-adjusted unemployment
# rates for US states from January 2020 to December 2022. Load it as a dataframe, as well
# as the data from the policy_uncertainty.xlsx file from homework 2 (you do not have to make
# any of the changes to this data that were part of HW2, unless you need to in order to 
# answer the following questions).
#    2.1: Merge both dataframes together
unemp_data = pd.read_csv('/Users/mac/Downloads/unemp.csv')
policy_data = pd.read_excel('/Users/mac/Downloads/policy_uncertainty.xlsx')

unemp_data['DATE'] = pd.to_datetime(unemp_data['DATE'])
unemp_data['year'] = unemp_data['DATE'].dt.year
unemp_data['month'] = unemp_data['DATE'].dt.month

state_mapping = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire',
    'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina',
    'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
    'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}
unemp_data['STATE'] = unemp_data['STATE'].map(state_mapping)
unemp_data.rename(columns={'STATE': 'state'}, inplace=True)

df_merged = pd.merge(unemp_data, policy_data, on=['state', 'year', 'month'], how='inner')


#    2.2: Calculate the log-first-difference (LFD) of the EPU-C data
#    2.2: Select five states and create one Matplotlib figure that shows the unemployment rate
#         and the LFD of EPU-C over time for each state. Save the figure and commit it with 
#         your code.
df_merged['log_EPU_C'] = np.log(df_merged['EPU_Composite'])
df_merged['EPU_C_LFD'] = df_merged.groupby('state')['log_EPU_C'].diff()


states = ['California', 'Texas', 'New York', 'Florida', 'Illinois']
fig, axs = plt.subplots(5, 1, figsize=(10, 20))

for i, state in enumerate(states):
    state_data = df_merged[df_merged['state'] == state]
    axs[i].plot(state_data['DATE'], state_data['unemp_rate'], label='Unemployment Rate', color='blue')  # Adjust column name
    axs[i].plot(state_data['DATE'], state_data['EPU_C_LFD'], label='Log First Difference of EPU-C', color='red', linestyle='--')
    axs[i].set_title(f'{state} Unemployment and EPU-C LFD')
    axs[i].legend()
    axs[i].set_xlabel('Date')
    axs[i].set_ylabel('Values')

plt.tight_layout()
plt.show()

#    2.3: Using statsmodels, regress the unemployment rate on the LFD of EPU-C and fixed
#         effects for states. Include an intercept.
states = ['California', 'Texas', 'New York', 'Florida', 'Illinois']
fig, axs = plt.subplots(len(states), 1, figsize=(10, 15))
#    2.4: Print the summary of the results, and write a 1-3 line comment explaining the basic
#         interpretation of the results (e.g. coefficient, p-value, r-squared), the way you 
#         might in an abstract.
import statsmodels.api as sm

model = smf.ols('unemp_rate ~ EPU_C_LFD + C(state) + intercept', data=df_merged)  # Adjust column name
results = model.fit()

print(results.summary())
print("The regression model estimates the impact of the log-first-difference of EPU-C on the unemployment rate, including fixed effects for states. The significance of the coefficients, reflected in the p-values, and the proportion of variance explained, indicated by the R-squared value, help understand the relationship's strength and relevance.")

