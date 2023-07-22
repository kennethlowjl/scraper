import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import re
import csv

# Create a CSV file and write headers
with open('sg_used_cars.csv','w',newline='') as f:
    header = ['name','price','depre','mileage','engine_cap','reg_date','power','owners']
    writer = csv.writer(f)
    writer.writerow(header)

# Function to store links of each car's details
def store_links(soup):
    links = []
    for item in soup.findAll('strong'): # Loop over each 'strong' tags
        try:
            link = item.find('a') # Find 'a' tag within 'strong'
            if 'info' in link['href']: # If 'info' in href, it's a valid link
                links.append(link['href'])
        except:
            continue # Continue to next tag if exception occurs
    return links # Return all valid links

# Function to get car name
def get_name(soup):
    try:
        name = soup.find('div',{'id':'toMap'}).text.strip() # Find 'div' tag with id 'toMap'
    except:
        name = 'NA'
    return name

# Function to get car price
def get_price(soup):
    try:
        price = soup.find('td',{'class':'font_red'}).text.strip()[1:] # Find 'td' tag with class 'font_red'
    except:
        price = 'NA'
    return price

# Function to get car depreciation per year
def get_depre(soup):
    try:
        depre = re.findall(r'\d+,\d+',soup.findAll('tr',{'class':'row_bg'})[1].find('td',{'class':None}).text)[0] # Regex pattern to find depreciation
    except:
        depre = 'NA'
    return depre

# Function to get car mileage
def get_miles(soup):
    try:
        mileage = re.findall(r'\d+,\d+',soup.find('div',{'class':'row_info'}).text.strip())[0] # Regex pattern to find mileage
    except:
        mileage = 'NA'
    return mileage

# Function to get car engine capacity
def get_engcap(soup):
    try:
        engine_cap = re.findall(r'\d+,*\d+',soup.findAll('div',{'class':'row_info'})[4].text)[0] # Regex pattern to find engine capacity
    except:
        engine_cap = 'NA'
    return engine_cap

# Function to get car registration date
def get_regdate(soup):
    try:
        reg_date = re.findall(r'\d{2}-\w{3}-\d{4}',soup.findAll('tr',{'class':'row_bg'})[1].findAll('td',{'class':None})[-1].text)[0] # Regex pattern to find registration date
    except:
        reg_date = 'NA'
    return reg_date

# Function to get car power
def get_power(soup):
    try:
        power = re.findall(r'\d+\.\d+',soup.findAll('div',{'class':'row_info'})[-2].text)[0] # Regex pattern to find power
    except:
        power = 'NA'
    return power

# Function to get number of car owners
def get_owners(soup):
    try:
        owners = soup.findAll('div',{'class':'row_info'})[-1].text
    except:
        owners = 'NA'
    return owners

# Function to visit each car's link and extract required details
def access_link(links):
    info = []
    for link in links:
        front = 'https://www.sgcarmart.com/used_cars/'
        url = front + link
        html = requests.get(url) # Requesting each link
        soup = bs(html.text,'lxml') # Parsing HTML
        # Extracting required details
        name = get_name(soup)
        price = get_price(soup)
        depre = get_depre(soup)
        mileage = get_miles(soup)
        eng_cap = get_engcap(soup)
        reg_date = get_regdate(soup)
        power = get_power(soup)
        owners = get_owners(soup)
        info.append([name,price,depre,mileage,eng_cap,reg_date,power,owners]) # Appending details to info list
        sleep(2)
    
    return info

# Function to save extracted info into CSV
def save_info(info):
    
    with open('sg_used_cars.csv','a',newline='') as f:

        writer = csv.writer(f)
        for row in info:
            writer.writerow(row) # Write each row of info into CSV

# Main Program
url = 'https://www.sgcarmart.com/used_cars/listing.php?BRSR={}00&RPG=100&AVL=2&VEH=12'
page_count = 0
for page in range(10):
    html = requests.get(url.format(page)) # Access each page
    soup = bs(html.text,'lxml') # Parse HTML
    links = store_links(soup) # Extract links
    info = access_link(links) # Visit each link and extract details
    save_info(info) # Save details into CSV
    page_count += 1
    print(page_count)
    sleep(5)
