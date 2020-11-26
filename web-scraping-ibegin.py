import requests
from bs4 import BeautifulSoup
import pymysql
pymysql.install_as_MySQLdb()

import compare as comp

def scrape_business_page(lnk):
    print()
    print("BUSINESS PAGE:")
    URL = lnk
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")
    name = soup.find('dd', class_='fn org name')
    business_name = name.text.strip()
    print(business_name)

    address = soup.find('dd', class_="street-address address.address")
    addy = address.text.split("#")
    business_address1 = addy[0].strip()
    print(business_address1)
    unit_number = addy[-1].strip()
    if unit_number.isnumeric():
        business_address2 = "Unit " + unit_number
    else:
        business_address2 = ""
    print(business_address2)

    city = soup.find('dd', class_="address.city")
    location = city.text.strip()
    print(location)

    address_state = soup.find('dd', class_="address.state")
    state_code = address_state.text.split(',')[0].strip()
    print(state_code)

    phone = soup.find('abbr', class_='tel phone')
    business_phone = phone.text.strip()
    print(business_phone)

    postal = soup.find('dd', class_="postal-code address.postalCode")
    postal_code = postal.text.strip()
    print(postal_code)

    return comp.compareData(business_name, business_phone, business_address1, business_address2, location, state_code,
                 postal_code)

def scrape_search(name, lst):
    URL = "https://www.ibegin.com/search/?cx=partner-pub-5473472811677186%3A4418038166&cof=FORID%3A10&ie=UTF-8&q=" + name.replace(" ", "+") + "&w=" + url_location.lower()
    print("SEARCH RESULTS:")
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    link = ""
    divs = soup.find_all('div', class_='business')
    for div in divs:
        small = div.find_all('small', class_='info')
        if len(small) > 0:
            url_address2 = address2DB.split(" ")
            search_address2 = url_address2[1].strip()
            full_address = url_address + " #" + search_address2
            if full_address in div.text:
                link = div.find('a')['href']
                lst.append(link)

    return link

bd_id = 49
nameDB, phoneDB, address1DB, address2DB, cityDB, stateDB, postalDB = comp.connect(bd_id)

# --- HARD CODED VALUES ---
# must be hard coded until its possible to retrieve data from database using bd_id from PHP files
url_name = nameDB
url_name = url_name.replace(" ", "+")
url_location = cityDB
url_phone = phoneDB
url_address = address1DB

# -----------------------------------------------------------------------------------------------

# --- FIRST SCRAPE THE SEARCH RESULTS PAGE ---
lst = []
link = scrape_search(url_name, lst)
if len(link) == 0:
    url_address2 = address2DB.split(" ")
    search_address = url_address2[1].strip()
    url_address_full = url_address + " " + search_address
    link = scrape_search(url_address_full, lst)

print("*** Starting list iteration ***")
if len(lst) > 1:
    # Iterate through the list of duplicates to see which one is most accurate
    count_max = 0
    for i in range(len(lst)):
        #print(lst[i])
        tup = scrape_business_page(lst[i])
        count_tup = 0
        for j in range(len(tup)):
            if tup[j] == 1:
                count_tup += 1
        #print(count_max, count_tup)
        if count_max < count_tup:
            count_max = count_tup
            link = lst[i]
            #print("link is now: ")
            #print(link)

if len(link) > 0:
    # -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---
    print()
    print("BUSINESS PAGE:")
    URL = link
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")
    name = soup.find('dd', class_='fn org name')
    business_name = name.text.strip()
    print(business_name)

    address = soup.find('dd', class_="street-address address.address")
    addy = address.text.split("#")
    business_address1 = addy[0].strip()
    print(business_address1)
    unit_number = addy[-1].strip()
    if unit_number.isnumeric():
        business_address2 = "Unit " + unit_number
    else:
        business_address2 = ""
    print(business_address2)

    city = soup.find('dd', class_="address.city")
    location = city.text.strip()
    print(location)

    address_state = soup.find('dd', class_="address.state")
    state_code = address_state.text.split(',')[0].strip()
    print(state_code)

    phone = soup.find('abbr', class_='tel phone')
    business_phone = phone.text.strip()
    print(business_phone)

    postal = soup.find('dd', class_="postal-code address.postalCode")
    postal_code = postal.text.strip()
    print(postal_code)

    comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                       postal_code, "iBEGIN")
else:
    print("*** ERROR: BUSINESS NOT FOUND ON WEBSITE ***")