import requests
from bs4 import BeautifulSoup
import pymysql
import re
pymysql.install_as_MySQLdb()

import compare as comp


def scrape_search(name, lst):
    URL = "https://find-open.ca/search?what="+ name +"&where=" + url_location.replace(" ", "+") + "&r=10&latlon="
    print("SEARCH RESULTS:")
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    link = ""
    divs = soup.find_all('div', class_='col-sm-7 col-xs-8 smaller-col-sm-7')
    for div in divs:
        span = div.find('span', class_="thoroughfare")
        if url_address in span.text:
            link = div.find('h2', 'field-content').find('a')['href']
            lst.append(link)
    print(link)
    return link

def scrape_search_next(link, lst):
    #URL = "https://find-open.ca" + str(link)
    URL = link
    print("SEARCH RESULTS:")
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    link = ""
    divs = soup.find_all('div', class_='col-sm-7 col-xs-8 smaller-col-sm-7')
    for div in divs:
        span = div.find('span', class_="thoroughfare").text
        span2 = div.find('div', class_="hidden-xs")
        p1 = re.sub('\ |\?|\.|\-|\/|\(|\)', '', url_phone)
        p2 = re.sub('\ |\?|\.|\-|\/|\(|\)', '', span2.text.strip())
        if url_address in span or p1 in p2:
            link = div.find('h2', 'field-content').find('a')['href']
            lst.append(link)
    return link

def scrape_next(url_search):
    URL = url_search

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    li = soup.find('li', class_='next')

    link = ""

    if li != None:
        link = li.find('a')['href']

    return link


bd_id = 37
nameDB, phoneDB, address1DB, address2DB, cityDB, stateDB, postalDB = comp.connect(bd_id)

# --- HARD CODED VALUES ---
# must be hard coded until its possible to retrieve data from database using bd_id from PHP files
url_name = nameDB
#url_name = "tim hortons"
url_name = url_name.replace(" ", "+")
url_location = cityDB
url_phone = phoneDB
url_address = address1DB
url_postal = postalDB
#url_address = "2 Bloor St"

# -----------------------------------------------------------------------------------------------


def scrape(name, loc):
    url_s = "https://find-open.ca/search?what=" + name + "&where=" + loc.replace(" ","+") + "&r=10&latlon="

    link = ""
    link_next = scrape_next(url_s)  # pg2
    lst = []
    link = scrape_search_next(url_s, lst)  # pg1
    while len(link) == 0 and len(link_next) > 0:
        url_s = "https://find-open.ca" + link_next  # pg2
        link_next = scrape_next(url_s)  # pg3
        link = scrape_search_next(url_s, lst)
        if len(link) == 0 and len(link_next) == 0:
            print("HOLOAF")
            return link
    return link

# --- FIRST SCRAPE THE SEARCH RESULTS PAGE ---
link = scrape(url_name, url_location)
if len(link) == 0:
    link = scrape(url_name, url_postal)
if len(link) == 0 and url_location in url_name:
    link = scrape(url_name.replace(url_location, "").strip(), url_postal)
if len(link) == 0:
    perms = url_name.split("+")
    name = ""
    for i in range(len(perms)):
        name += perms[i]
        link = scrape(name, url_location)
        if len(link) == 0 and name == url_name:
            print("BUSINESS NOT ON WEBSITE")
            break
        if len(link) > 0:
            break



#link = "https://find-open.ca/toronto/23e2-digital-marketing-1007911"
if len(link) > 0:
    # -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---
    print()
    print("BUSINESS PAGE:")
    URL = "https://find-open.ca" + link
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")
    name = soup.find('li', class_='active last')
    business_name = name.text.strip()
    print(business_name)

    address = soup.find('span', class_="thoroughfare")
    addy = address.text.strip().split(",")
    business_address1 = addy[0]
    print(business_address1)
    if len(addy) > 1:
        business_address2 = addy[1].strip()
    else:
        business_address2 = ""
    print(business_address2)

    city = soup.find('span', class_="locality")
    location = city.text.strip().replace(",", "")
    print(location)

    state = soup.find('span', class_="state")
    state_code = state.text.strip().replace(",", "")
    print(state_code)

    phone = soup.find('div', class_="hidden-xs company-phone")
    business_phone = phone.text.strip()[3:]
    print(business_phone)

    postal = soup.find('span', class_="postal-code")
    postal_code = postal.text.strip()
    print(postal_code)

    comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                       postal_code, "OPENDI")
else:
    print("*** ERROR: BUSINESS NOT FOUND ON WEBSITE ***")