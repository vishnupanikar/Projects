#Imports
import os
import requests
from bs4 import BeautifulSoup

#getting the data and converting it into html format
source = requests.get('https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data').text
soup = BeautifulSoup(source,'lxml')

#finding the required table using table id
table = soup.find('table' , id = 'thetable')

#Extracting Country Names
table_head = table.find_all('th')
table_head = table_head[11:]
table_head = [i[1] for i in enumerate(table_head) if i[0]%2 == 0]
country = [i.a.text for i in table_head]

#Extracting the Count of Cases, Deaths and recovery
table_data = table.find_all('td')
table_data = table_data[:-2]
td = [i.text.split('\n')[0] for i in table_data if '[' not in i.text]


def clean(data):
	data = data.split(',')
	data = ''.join(data)
	return data

for i in enumerate(td):
	td[i[0]] = clean(i[1])

def convert_to_numbers(data):
	try:
		data = int(data)
	except Exception as exp_obj:
		data = 0
		print('Unknown Character Found....so returning 0')
	finally:
		return data

for i in enumerate(td):
	td[i[0]] = convert_to_numbers(i[1])

#Writing Data into a csv file
import csv
fopen = open('global_covid19.csv','w')
csv_fopen = csv.writer(fopen)

csv_fopen.writerow(['Country','Cases','Deaths','Recovered'])

country_index = 0

for i in range(0,len(td),3):
    Country = country[country_index]
    Cases = td[i]
    Deaths = td[i+1]
    Recovered = td[i+2]
    country_index += 1
    csv_fopen.writerow([Country,Cases,Deaths,Recovered])

fopen.close()
