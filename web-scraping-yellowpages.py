import requests
from bs4 import BeautifulSoup
import pymysql
pymysql.install_as_MySQLdb()

import compare as comp


def scrape_business_page(link):
    print()
    print("BUSINESS PAGE:")
    URL = "https://www.yellowpages.ca/" + link
    # URL = "https://www.yellowpages.ca/bus/Ontario/Toronto/Tim-Hortons/100435156.html"
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    names = soup.find_all('span', class_='merchantName jsShowCTA')
    names2 = soup.find_all('span', class_='merchantNamejsShowCTA')
    if names != []:
        for name in names:
            business_name = name.text
        print(business_name)
    elif names2 != []:
        for name in names2:
            business_name = name.text
        print(business_name)

    address = soup.find_all('div', class_='merchant__item merchant__address merchant__address__mobile')
    for addy in address:
        s = addy.text.strip().split("\n")[0]
    a = s
    state_code = a.split(",")[2][1:3].strip()
    postal_code = a.split(",")[2][4:]
    business_address1 = a.split(",")[0].split("-")[1]
    business_address2 = "Unit " + a.split(",")[0].split("-")[0]
    location = a.split(",")[1].strip()
    print(business_address1)
    print(business_address2)
    print(location)
    print(state_code)
    print(postal_code)

    phones = soup.find_all('span', class_='mlr__sub-text')
    for phone in phones:
        business_phone = phone.text.strip()
    print(business_phone)

    print(comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                       postal_code, "YELLOWPAGES"))


def scrape_search(count):
    URL2 = "https://www.yellowpages.ca/search/si/" + str(count) + "/" + url_name + "/" + url_location
    print(URL2)
    page2 = requests.get(URL2)

    soup2 = BeautifulSoup(page2.content, 'html.parser')

    divs2 = soup2.find_all('div', class_='listing__right hasIcon')
    link2 = ""
    for div2 in divs2:
        span2 = div2.find_all('span', class_='jsMapBubbleAddress')
        if len(span2) > 0:
            span2 = span2[0]
            print(span2.text)
            if url_address.lower() in span2.text.lower():
                link2 = div2.find('a', class_='listing__name--link listing__link jsListingName')['href']
    return link2

bd_id = 49
nameDB, phoneDB, address1DB, address2DB, cityDB, stateDB, postalDB = comp.connect(bd_id)


d = {"Ontario": "ON", "Quebec": "QC", "Nova Scotia": "NS", "New Brunswick": "NB", "Manitoba": "MB", "British Columbia": "BC", "Prince Edward Island": "PE"
             ,"Saskatchewan": "SK", "Alberta" : "AB", "Newfoundland": "NL", "Labrador": "NL"}
province = d[stateDB]


# --- HARD CODED VALUES ---
# must be hard coded until its possible to retrieve data from database using bd_id from PHP files
#url_name = "23e2"
url_name = nameDB
url_name = url_name.replace(" ", "+")
url_location = cityDB + "+" + province
#url_location = "Toronto+ON"
#url_location = url_location.replace(" ", "+")
url_phone = phoneDB
url_address = address1DB
#url_address = "222 Jarvis St"

# ------------------------------------------------------------------------------------------------
count = 1
s = True
URL = "https://www.yellowpages.ca/search/si/" + str(count) + "/" + url_name + "/" + url_location
print("SEARCH RESULTS:")
print(URL)
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

divs = soup.find_all('div', class_='listing__right hasIcon')
link = ""
pg = soup.find('span', class_='pageCount')
pg = pg.text.split("/")[1].strip()

for div in divs:
    span = div.find_all('span', class_='jsMapBubbleAddress')
    if len(span) > 0:
        span = span[0]
        print(span.text)
        if url_address.lower() in span.text.lower():
            link = div.find('a', class_='listing__name--link listing__link jsListingName')['href']
w = 0
if link == "":
    link2=""
    while s:
        count += 1
        print()
        print(count)
        link2 = scrape_search(count)
        if count == int(pg) and len(link2) == 0:
            link2 = "search/si/1/" + url_phone + "/" + url_location
            #print("NOT ON WEBSITE")
            #w = 1
            s= False
        elif len(link2) > 0:
            s = False

if count > 1:
    print("link:")
    print(link2)

# -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---

if w != 1:
    scrape_business_page(link2)


