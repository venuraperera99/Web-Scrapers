import requests
from bs4 import BeautifulSoup
import pymysql
pymysql.install_as_MySQLdb()

import compare as comp

def scrape_business_page(lnk):
    # -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---
    print()
    print("PAGE:")
    URL = lnk
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")

    name = soup.find('span', class_='header-text')
    business_name = name.text.strip()
    print(business_name)

    div1 = soup.find('div', id="item_place")
    addresss = div1.find('div').text
    state_code = ""

    # Dealing with address
    address = addresss.split(",")
    addy = address[0]
    business_address2 = ""
    if "Unit" in addy:
        addr = addy.split("Unit")
        business_address2 = "Unit " + addr[1].replace("#", "").strip()
        business_address1 = addr[0].strip()
        print(business_address1)
        print(business_address2)
    elif "#" in addy:
        addr = addy.split("#")
        business_address2 = "Unit " + addr[1].strip()
        business_address1 = addr[0].strip()
        print(business_address1)
        print(business_address2)
    elif "-" in addy:
        addr = addy.split("-")
        business_address2 = "Unit " + addr[0].strip()
        business_address1 = addr[1].strip()
        print(business_address1)
        print(business_address2)
    else:
        business_address1 = addy.strip()
        print(business_address1)


    return business_address1

def scrape_next(name, postal, pg):
    URL = "https://www.yalwa.ca/q/?query=" + name + "&area=" + postal.replace(" ", "+") + "&geoid=&page=" + str(pg)

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    div = soup.find('div', class_="paging")
    link = ""

    if div == None:
        print("NO NEXT")
        return link
    attr = div.find_all('a')
    a = attr[-1]

    if a != None or a.text == "Next":
        link = a['href']
    return link


def scrape_search(name, postal, pg):
    URL = "https://www.yalwa.ca/q/?query=" + name + "&area=" + postal.replace(" ", "+") + "&geoid=&page=" + str(pg)
    print("SEARCH RESULTS:")
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    link = ""
    divs = soup.find_all('div', class_='resultRow')
    for div in divs:
        span = div.find('span', class_="textHeader")
        if span == None:
            continue
        if name.replace("+", " ") in span.text.strip():
            link = div.find('a')['href']
            #print("LINKKK:" + link)
            scraped = scrape_business_page(link)
            if url_address in scraped:
                return link

    return link


bd_id = 38
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
#url_postal = "M2J 5A7"
#url_address = "240 Alton Towers Circle"

# -----------------------------------------------------------------------------------------------

# --- FIRST SCRAPE THE SEARCH RESULTS PAGE ---

def scrape(name):
    link = ""
    pg = 0
    link = scrape_search(name, url_postal, pg)
    link_next = scrape_next(name, url_postal, pg)
    while len(link) == 0:
        pg += 1
        link = scrape_search(name, url_postal, pg)
        link_next = scrape_next(name, url_postal, pg)
        print(link)
        if len(link) > 0:
            return link
        if len(link) == 0 and len(link_next) == 0:
            return link
    return link

link = scrape(url_name)
if len(link) == 0:
    perms = url_name.split("+")
    name = ""
    for i in range(len(perms)):
        name += perms[i]
        print(name)
        link = scrape(name)
        if len(link) == 0 and name == url_name:
            print("BUSINESS NOT ON WEBSITE")
            break
        if len(link) > 0:
            break

print(link)
#link = "https://toronto.yalwa.ca/ID_136419410/CPAP-Clinic-Toronto.html"
if len(link) > 0:
    # -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---
    print()
    print("BUSINESS PAGE:")
    URL = link
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")


    name = soup.find('span', class_='header-text')
    business_name = name.text.strip()
    print(business_name)

    div1 = soup.find('div', id="item_place")
    addresss = div1.find('div').text
    state_code = ""

    # Dealing with address
    address = addresss.split(",")
    addy = address[0]
    business_address2 = ""
    if "Unit" in addy:
        addr = addy.split("Unit")
        business_address2 = "Unit " + addr[1].replace("#", "").strip()
        business_address1 = addr[0].strip()
        print(business_address1)
        print(business_address2)
    elif "#" in addy:
        addr = addy.split("#")
        business_address2 = "Unit " + addr[1].strip()
        business_address1 = addr[0].strip()
        print(business_address1)
        print(business_address2)
    elif "-" in addy:
        addr = addy.split("-")
        business_address2 = "Unit " + addr[0].strip()
        business_address1 = addr[1].strip()
        print(business_address1)
        print(business_address2)
    else:
        business_address1 = addy.strip()
        print(business_address1)


    # Dealing with the rest
    if len(address) == 3:
        # Location and Postal Code
        addy2 = address[1]
        location_and_postal = addy2.split(" ")
        location = location_and_postal[1].strip()
        postal = location_and_postal[2] + " " + location_and_postal[3]
        postal_code = postal.strip()
        print(location)
        print(postal_code)
    elif len(address) == 4:
        # Unit
        addy2 = address[1]
        if "Unit" in addy2:
            business_address2 = addy2.replace("#", "").strip()
            print(business_address2)

        # Location and Postal Code
        addy2 = address[2]
        location_and_postal = addy2.split(" ")
        location = location_and_postal[1].strip()
        print(location)
        postal = location_and_postal[2] + " " + location_and_postal[3]
        postal_code = postal.strip()
        print(postal_code)

    elif len(address) == 5:
        # Location
        addy2 = address[1]
        location = addy2.strip()
        print(location)
        # State Code
        addy2 = address[2]
        state_code = addy2.strip()
        print(state_code)
        # Location and Postal Code
        addy2 = address[3]
        location_and_postal = addy2.split(" ")
        postal = location_and_postal[2] + " " + location_and_postal[3]
        postal_code = postal.strip()
        print(postal_code)

    business_phone = ""

    print(comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                       postal_code, "YALWA"))
else:
    print("*** ERROR: BUSINESS NOT FOUND ON WEBSITE ***")