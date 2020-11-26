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

def scrape_search(name, pg, lst):
    URL = "http://www.salespider.com/c2_69_a0_11366/" + url_location.lower().replace(" ", '+') + "-" + state + "?q=" + name + "&p=" + str(pg)
    print("SEARCH RESULTS:")
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    link = ""
    divs1 = soup.find_all('div', class_='_result_container')

    for i in range(len(divs1)):
        div = divs1[i].find('div', class_='businessDirectoryCssBrowseResp_description')
        if div == None:
            continue
        print(div.text)
        if url_address in div.text:
            print("*** LINK: ")
            link = divs1[i].find('a')['href']
            lst.append(link)
            print("http://www.salespider.com" + str(link))

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
url_state = stateDB
url_address = "11219 Financial Centre Pkwy"

# -----------------------------------------------------------------------------------------------

# --- FIRST SCRAPE THE SEARCH RESULTS PAGE ---
lst = []
name_lst = url_name.split("+")
bool = True
dict = {"Ontario": "ON", "Quebec": "QC", "Nova Scotia": "NS", "New Brunswick": "NB", "Manitoba": "MB",
        "British Columbia": "BC", "Prince Edward Island": "PE", "Saskatchewan": "SK", "Alberta": "AB",
        "Newfoundland": "NL", "Labrador": "NL"}
state = dict[stateDB]
pg = 1
#link = scrape_search(url_name, pg, lst)
while bool or pg < 9:
    print("*** PAGE: " + str(pg))
    link = scrape_search(url_name, pg, lst)
    pg += 1
    if len(link) > 0:
        bool = False
        break
    if pg > 9:
        print("*** BUSINESS NOT ON WEBSITE ***")
        bool = False



#link = "http://www.salespider.com/b-385208333/cpap-clinic"
if len(link) > 0:
    # -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---
    print()
    print("BUSINESS PAGE:")
    URL = link
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print("SCRAPED DATA:")
    name = soup.find('div', class_='site_mobile_section_heading site_resp_ShowMobileUnder985')
    business_name = name.text.strip()
    print(business_name)

    address = soup.find('div', class_='_address').find_all('div')[0]
    addy = address.text.strip().split(",")
    business_address2 = ""
    business_address1 = addy[0].strip()
    if len(addy) > 1:
        business_address2 = addy[1].strip()
    print(business_address1)
    print(business_address2)


    addy2 = soup.find('div', class_='_address').find_all('div')[1].text.strip().split(",")
    location = addy2[0]
    print(location)
    state_plus_postal = addy2[1].strip().split(" ")
    state_code = state_plus_postal[0]
    print(state_code)

    phone = soup.find('h3', class_="business_directory_displayInline").find('a')
    business_phone = phone.text.strip()
    print(business_phone)

    postal = state_plus_postal[1] + " " + state_plus_postal[2]
    postal_code = postal.strip()
    print(postal_code)

    comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                       postal_code, "SALESPIDER")
else:
    print("*** ERROR: BUSINESS NOT FOUND ON WEBSITE ***")