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
    div = soup.find('div', class_="bus pd-r l-h-30 w100-i")
    span = div.find_all('span')

    name = soup.find('span', class_='fl st')
    business_name = name.text.strip()
    print(business_name)

    address = span[2].text
    addy2 = address.strip()
    if "Unit" in addy2:
        addy = addy2.split("#")
        business_address2 = "Unit " + addy[1]
        addy0 = addy2.split(",")
        business_address1 = addy0[0]
    else:
        addy = addy2.split("-")
        business_address2 = ""
        if len(addy) > 1:
            business_address2 = "Unit " + addy[0].strip()
            business_address1 = addy[1].strip()
        else:
            business_address1 = addy[0].strip()
    print(business_address1)
    print(business_address2)

    location = span[3].text.strip()
    print(location)
    state_code = span[4].text.strip()
    print(state_code)

    phone = soup.find('div', class_="bus pd-r l-h-30 w100-i")
    business_phone = phone.text.split("Phone")[1][1:13].strip()
    print(business_phone)

    postal = span[5].text
    postal_code = postal.strip()
    print(postal_code)

    comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                 postal_code, "CDNPAGES")

def scrape_search(name, pg, lst):
    URL = "https://www.cdnpages.ca/s/" + str(pg) + "/" + name + "/" + url_location.replace(" ", "+")
    print("SEARCH RESULTS:")
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    link = ""
    divs = soup.find_all('div', class_='bus w100-i')
    for div in divs:
        span = div.find_all('span')
        if url_address in span[2].text or postalDB in span[5]:
            link = div.find('a')['href']
            lst.append(link)

    return link


def scrape_next(name, pg):
    URL = "https://www.cdnpages.ca/s/" + str(pg) + "/" + name + "/" + url_location.replace(" ", "+")

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    span = soup.find('span', id="paging")
    attr = span.find_all('a')
    a = attr[-1]

    link = ""
    if a != None or a.text == "Next":
        link = a['href']
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
#url_address = "2672 Trout Lake Rd"

# -----------------------------------------------------------------------------------------------

# --- FIRST SCRAPE THE SEARCH RESULTS PAGE ---
lst = []
name_lst = url_name.split("+")
pg = 1
url_s = "https://www.cdnpages.ca/s/" + str(pg) + "/" + url_name + "/" + url_location.replace(" ", "+")
link = scrape_search(url_name, pg, lst)
next_links = scrape_next(url_name, pg)
pg += 1
while len(link) == 0 and len(next_links) > 0:
    print("*** PAGE: " + str(pg))
    link = scrape_search(url_name, pg, lst)
    pg += 1
    next_links = scrape_next(url_name, pg)
    if len(link) > 0:
        break
    if len(link) == 0 and len(next_links) == 0:
        print("*** BUSINESS NOT ON WEBSITE ***")
        break

#print("*** LINK:\n" + link)

#link = "https://www.cdnpages.ca/Business/Canada+Business+Services/2497960"
if len(link) > 0:
    # -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---
    print()
    print("BUSINESS PAGE:")
    URL = link
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")
    div = soup.find('div', class_="bus pd-r l-h-30 w100-i")
    span = div.find_all('span')


    name = soup.find('span', class_='fl st')
    business_name = name.text.strip()
    print(business_name)

    address = span[2].text
    addy2 = address.strip()
    if "Unit" in addy2:
        addy = addy2.split("#")
        business_address2 = "Unit " + addy[1]
        addy0 = addy2.split(",")
        business_address1 = addy0[0]
    else:
        addy = addy2.split("-")
        business_address2 = ""
        if len(addy) > 1:
            business_address2 = "Unit " + addy[0].strip()
            business_address1 = addy[1].strip()
        else:
            business_address1 = addy[0].strip()
    print(business_address1)
    print(business_address2)

    location = span[3].text.strip()
    print(location)
    state_code = span[4].text.strip()
    print(state_code)

    phone = soup.find('div', class_="bus pd-r l-h-30 w100-i")
    business_phone = phone.text.split("Phone")[1][1:13].strip()
    print(business_phone)

    postal = span[5].text
    postal_code = postal.strip()
    print(postal_code)

    comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                       postal_code, "CDNPAGES")
else:
    print("*** ERROR: BUSINESS NOT FOUND ON WEBSITE ***")