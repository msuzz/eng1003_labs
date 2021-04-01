import pandas as pd

mydata = pd.read_csv('wk6-midsem-example-data.csv')

print(mydata.head())

# Section for question 2
#
# Finds us the sum of all values in column 887dee6e

q2 = mydata['887dee6e'].values
q2sum = 0

for i in range(len(q2)):
    q2sum += q2[i]

print('Sum of column 887dee6e: {:g}'.format(q2sum))

# Section for question 3
#
# Finds us the smallest positive number in column c9239322

q3 = mydata['c9239322'].values
q3smlPos = q3[0]  # index 0 is obviously smallest thus far

for i in range(1,len(q3)):  # start our count at one, as we assign index 0 above
    if (q3[i] > 0) and (q3[i] < q3smlPos):
        q3smlPos = q3[i]

print('Smallest positive number of column c9239322: {:g}'.format(q3smlPos))

# Section for question 4
#
# Finds us the mean of all strictly negative numbers in column 61f71333

q4 = mydata['61f71333'].values
q4negSum   = 0
q4negCount = 0
q4negMean  = 0

for i in range(len(q4)):
    if q4[i] < 0:  # only increment and sum negative numbers
        q4negSum += q4[i]
        q4negCount = q4negCount + 1

q4negMean = q4negSum / q4negCount  # get the mean
print('Mean of all negative numbers in column 61f71333: {:g}'.format(q4negMean))
