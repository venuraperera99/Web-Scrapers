import requests
from bs4 import BeautifulSoup
import pymysql
pymysql.install_as_MySQLdb()

import compare as comp


def scrape_business_page(link):
    print()
    print("BUSINESS PAGE:")
    URL = "https://" + link
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    name = soup.find('h1', class_='top-bname')
    business_name = name.text.strip()
    print(business_name)

    address = soup.find_all('span', class_="bot-d")
    business_address = address[5].text.strip().split(",")[0]
    location = address[5].text.strip().split(",")[1].strip()
    state_code = address[5].text.strip().split(",")[2].strip()
    print(business_address)
    print(location)
    print(state_code)


    phone = soup.find('span', class_='bot-d htc-link hidden-mob')
    business_phone = phone.text.strip()
    print(business_phone)

    postal = soup.find_all('span', class_="loc-div")
    postal_code = postal[2].text.strip()
    print(postal_code)

    full_adr = "" + address1DB + " " + address2DB

    if business_address == full_adr:
        business_address1, business_address2 = address1DB, address2DB
    business_address1, business_address2 = address1DB, address2DB

    print(comp.compare(business_name, business_phone, business_address1, business_address2, location, state_code,
                       postal_code, "CYBO"))

def scrape_next(url_search):
    URL = url_search

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    link = soup.find('a', class_='mob-pag-next noselect ellipsis')

    return link

def scrape_search(url_next):
    if len(url_next) == 0:
        return "123"
    URL2 = "https://www.cybo.com/search/" + url_next['href']
    print(URL2)
    page2 = requests.get(URL2)

    soup2 = BeautifulSoup(page2.content, 'html.parser')

    attr2 = soup2.find_all('a', class_='r_cybo float_left result_link_box')

    for a2 in attr2:
        span2 = a2.find('span', class_='e-add ellipsis')
        if url_address in span2.text:
            link2 = a2.find('a')['href']
            link2 = link2[2:]
    return link2


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
#url_address = "2377 Yonge St"

# ------------------------------------------------------------------------------------------------

# --- FIRST SCRAPE THE SEARCH RESULTS PAGE ---
count = 1
s = True
URL = "https://www.cybo.com/search/?search=" + url_name + "&address=&phone=&web=&email=&searchcity=" + url_location + "&tok=qd445r-d77517b4c464eb4d53d1&ns=y&wt=drill&udrill=&pl=" + url_location.lower() + "&i=CA&t=c&lat=&lng="
print("if you get an error with this script. Click the link below, enter the captcha and run the script again.")
print("SEARCH RESULTS:")
print(URL)
link_next = scrape_next(URL)
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

attr = soup.find_all('a', class_='r_cybo float_left result_link_box')
link = ""
for a in attr:
    span = a.find('span', class_='e-add ellipsis')
    if url_address in span.text:
        print(a)
        print(a.find('a'))
        link = a.find('a')['href']
        link = link[2:]
if link == "":
    while s:
        count += + 1
        print()
        print(count)
        link_next = scrape_next(URL)
        link = scrape_search(link_next)
        if link == "123":
            continue
        elif len(link) > 0:
            s = False
print("link:")
print(link)

# -- NEXT SCRAPE THE ACTUAL BUSINESS PAGE ---
scrape_business_page(link)


