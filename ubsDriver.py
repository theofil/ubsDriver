#!/usr/bin/python
import csv
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

"""
This script reads your UBS account statement which is previously exported (by you) 
in CSV format and calculates the monthly expenses as function of time printing out 
in text and in a time graph the calculated averages.
"""

### Initialization
csvFileName = "/tmp/export.csv"   # Put here path+filename to the CSV file
excludeDebits = ['1170.00']       # Put here any reoccurring debits you don't want to consider, e.g., your rent
fd = ""                           # First day DD.MM.YYYY (leave empty to use default from CSV record)
ld = "30.07.2017"                 # Last day DD.MM.YYYY (leave empty to use default from CSV record)
makePlot = True                   # Create a graphic showing expenses as function of time

### --------------------------------------------------------------------
### No need to read what's below in order to just make use of the script
### --------------------------------------------------------------------

### convert string of type YYYY.MM.DD to a date(YYYY, MM, DD) object
def StringToDate(myday):
    date_   = myday[0:2]
    month_  = myday[3:5]
    year_   = myday[6:10]
    return date(int(year_), int(month_), int(date_))

### read only the first line of the csv to get info
csvfile = open(csvFileName, 'rb')
reader = csv.reader(csvfile, delimiter=';', quotechar=' ')
firstLine  = reader.next()
secondLine =  reader.next()
currency = secondLine[5]
if fd == "": fd = secondLine[6] # first day string
if ld == "": ld = secondLine[7] # last day string
firstDay = StringToDate(fd)
lastDay  = StringToDate(ld)
print "record from",fd,"to",ld 
print "currency = ", currency

### access the CSV file and sum up the expenses 
totMonths = (lastDay.year - firstDay.year)*12 + lastDay.month - firstDay.month
print "calculating expenses for a total period of ", (lastDay - firstDay).days, "corresponding to totMonths = ", totMonths
print "excluded debits = ",excludeDebits

montlySum    = np.zeros(totMonths+1)
monthYear    = []
sum = 0

with open(csvFileName, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar=' ')
    for row in reader:
	if row[-3]!="" and row[-2]!="Credit": 
            value  = row[-3].replace("'","")
            date_   = row[9][0:2]
            month_  = row[9][3:5]
            year_   = row[9][6:10]
            tradeDate = date(int(year_), int(month_), int(date_))
            prefix = ""
	    acceptValue = True
            if value in excludeDebits: 
		prefix = "     "
                acceptValue = False

            if tradeDate > lastDay: acceptValue = False  # trivial check
            if tradeDate < firstDay: acceptValue = False # trivial check
 
            MY = str(tradeDate.month) + "-" + str(tradeDate.year)
            if MY not in monthYear: monthYear += [MY]

            monthIndex = (tradeDate.year - firstDay.year)*12 + tradeDate.month - firstDay.month
            if monthIndex > totMonths:acceptValue = False
            if acceptValue: 
		sum += float(value)
                montlySum[monthIndex] =  montlySum[monthIndex] + float(value)  
		    
if abs(np.sum(montlySum) - sum)>0.01: print "DEBUG:", sum, " --- ", np.sum(montlySum) 
monthYear = list(reversed(monthYear))

### print the monthly expenses and average
for ii in xrange(totMonths+1):
     print monthYear[ii],"  ", montlySum[ii]	

print "per 30 days average = ",(sum/float((lastDay - firstDay).days))*30.

### plot debits as function of time (per month)
if(makePlot):
    plt.rc('xtick', labelsize=15) 
    plt.rc('ytick', labelsize=15) 
    plt.plot(xrange(totMonths+1)  , montlySum, "bs--")
    plt.ylabel("["+currency+"]")
    plt.xlabel("[month index]")
    plt.xticks(xrange(totMonths+1), monthYear, rotation='vertical')
    plt.margins(0.05)
    plt.subplots_adjust(bottom=0.2)
    plt.show()
