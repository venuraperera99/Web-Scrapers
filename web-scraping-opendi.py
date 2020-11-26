import requests
from bs4 import BeautifulSoup
import pymysql
pymysql.install_as_MySQLdb()

import compare as comp

def scrape_business_page(lnk):
    print()
    print("BUSINESS PAGE:")
    URL = link
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")
    name = soup.find('h1', class_='has-sub yxt-name')
    business_name = name.text.strip()
    print(business_name)

    address = soup.find('span', class_="mui-pull-left")
    addy = address.text.strip().split(",")
    business_address = addy[0]
    if address1DB + " " + address2DB == business_address:
        business_address2 = address2DB
    else:
        business_address2 = ""
    business_address1 = address1DB
    print(business_address1)
    print(business_address2)
    location = addy[1].strip()
    print(location)
    state_code = addy[2].strip()
    print(state_code)

    phone = soup.find('span', class_="yxt-phone-main")
    business_phone = phone.text.strip()
    print(business_phone)

    postal = soup.find_all('span', class_="mui-pull-left")[1]
    postal_code = postal.text.strip()
    print(postal_code)

    comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                 postal_code, "OPENDI")

def scrape_search(name, lst):
    URL = "https://www.opendi.ca/search?what=" + name + "&where=" + url_address.replace(" ", "+")
    print("SEARCH RESULTS:")
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    link = ""
#    divs = soup.find_all('div', class_='serp-listing serp-listing-mobile serp-listing--exact js-detail- mui-row									mui-divider-bottom						')
    divs = soup.find_all('div', class_='serp-listing__content mui-row no-margin')
    for div in divs:
        span = div.find('span', class_="yxt-address is_block")
        if url_address in span.text:
            link = div.find('a')['href']
            lst.append(link)

    return link

bd_id = 49
nameDB, phoneDB, address1DB, address2DB, cityDB, stateDB, postalDB = comp.connect(bd_id)

# --- HARD CODED VALUES ---
# must be hard coded until its possible to retrieve data from database using bd_id from PHP files
url_name = nameDB
#url_name = "tim hortons"
url_name = url_name.replace(" ", "+")
url_location = cityDB
url_phone = phoneDB
url_address = address1DB
#url_address = "170 University Ave"

# -----------------------------------------------------------------------------------------------

# --- FIRST SCRAPE THE SEARCH RESULTS PAGE ---
lst = []
link = scrape_search(url_name, lst)
if len(link) == 0:
    name_lst = url_name.split("+")
    for i in name_lst:
        link = scrape_search(i, lst)
        if len(link) > 0:
            break


if len(link) > 0:
    # -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---
    print()
    print("BUSINESS PAGE:")
    URL = link
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")
    name = soup.find('h1', class_='has-sub yxt-name')
    business_name = name.text.strip()
    print(business_name)

    address = soup.find('span', class_="mui-pull-left")
    addy = address.text.strip().split(",")
    business_address = addy[0]
    if address1DB + " " + address2DB in business_address:
        business_address2 = address2DB
    else:
        business_address2 = ""
    business_address1 = address1DB
    dds = soup.find_all('dd', class_='mui-text-left')
    city_plus_state = (dds[1].find_all('span')[2].text.strip().split(","))
    print(business_address1)
    if len(addy) > 1 and "Unit" in addy[1]:
        business_address2 = addy[1].strip()
    elif len(addy) > 1:
        location = addy[1].strip()
    print(business_address2)
    location = city_plus_state[0]
    print(location)
    state_code = ""
    if len(addy) > 2:
        state_code = addy[2].strip()
        print(state_code)
    elif len(city_plus_state) > 1:
        state_code = city_plus_state[1].strip()
        print(state_code)
    phone = soup.find('span', class_="yxt-phone-main")
    business_phone = phone.text.strip()
    print(business_phone)

    postal = soup.find_all('span', class_="mui-pull-left")[1]
    postal_code = postal.text.strip()
    print(postal_code)

    comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                       postal_code, "OPENDI")
else:
    print("*** ERROR: BUSINESS NOT FOUND ON WEBSITE ***")