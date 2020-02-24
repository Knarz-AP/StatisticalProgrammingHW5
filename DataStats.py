# Assignment Information
print("Data 51100- Spring 2020")
print("Alec Peterson")
print("Programming Assignment #5")

# Imports
import pandas as pd
import numpy as np
import re

# Read data and make dataframe
dataset = pd.read_csv('cps.csv')
relevant_data = dataset[
    ['School_ID', 'Short_Name', 'Is_High_School', 'Zip', 'Student_Count_Total', 'College_Enrollment_Rate_School',
     'Grades_Offered_All', 'School_Hours']].sort_index()

# Grab lowest/highest grades offered
relevant_data['Lowest_Grade_Offered'] = relevant_data.apply(lambda x: x['Grades_Offered_All'][0:2], 1).str.replace(",",
                                                                                                                   '')
relevant_data['Highest_Grade_Offered'] = relevant_data.apply(lambda x: x['Grades_Offered_All'][-2:], 1).str.replace(",",
                                                                                                                    '')

# hours, find and replace missing data
def start_time(x):
    if str(x[0]) == 'nan':
        return 0
    else:
        return int(re.findall(r'[1-9]', x[0])[0])


time = relevant_data[['School_Hours']].apply(start_time, axis=1)
relevant_data = relevant_data.assign(Starting_Hour=time)

# Replace the missing numeric values with the mean for that column
for num in relevant_data.select_dtypes(['int64', 'float64']).columns:
    relevant_data[num].fillna(relevant_data[num].mean(), inplace=True)

# Display the first 10 rows of this dataframe
relevant_data = relevant_data.drop(['Grades_Offered_All', 'School_Hours'], axis=1)
print(relevant_data.head(10))

# Mean and standard deviation of College Enrollment Rate for High Schools
mean_college = relevant_data.groupby('Is_High_School')['College_Enrollment_Rate_School'].mean()
std_college = relevant_data.groupby('Is_High_School')['College_Enrollment_Rate_School'].std()
print("College Enrollment Rate for High Schools = ", mean_college[1].round(2), "(sd=", std_college[1].round(2), ")", "\n")

# Mean and standard deviation of Student_Count_Total for non-High Schools
mean_count = relevant_data.groupby('Is_High_School')['Student_Count_Total'].mean()
std_count = relevant_data.groupby('Is_High_School')['Student_Count_Total'].std()
print("Total Student Count for non-High Schools = ", mean_count[0].round(2), "(sd=", std_count[0].round(2), ")", "\n")

# Distribution of starting hours for all schools
seven_am = []
eight_am = []
nine_am = []

for n in relevant_data['Starting_Hour']:
    if n == 7:
        seven_am.append(n)
    if n == 8:
        eight_am.append(n)
    if n == 9:
        nine_am.append(n)

print("Distribution of Starting Hours")
print("7am: ", len(seven_am))
print("8am: ", len(eight_am))
print("9am: ", len(nine_am), "\n")

# Number of schools outside of the Loop Neighborhood (i.e., outside of zip codes 60601, 60602, 60603, 60604, 60605, 60606, 60607, and 60616)
zipcodes = [60601, 60602, 60603, 60604, 60605, 60606, 60607, 60616]
out_loop = []
for zips in relevant_data['Zip']:
    if zips not in zipcodes:
        out_loop.append(zips)

print("Number of schools outside the loop: ", len(out_loop))