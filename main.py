from undetected_chromedriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
from telegram import Bot
import time
import csv


BOT_TOKEN = 'Your bot token'
CHAT_ID = 'your chat id' 
records=open("records.csv","a+",encoding="utf-8",newline="")
fieldnames = ['City Name', 'Property Links']
writer = csv.DictWriter(records, fieldnames=fieldnames)
if records.tell()==0:
    writer.writeheader()


async def send_message(home_link,city):
    bot = Bot(token=BOT_TOKEN)
    while(1):
        try:
            await bot.send_message(chat_id=CHAT_ID, text=f'Check out new home in {city}, Canada\n follow this url: {home_link}')
        except:
            continue
        else:
            break  

def read_records():
    records.seek(0)
    reader=csv.DictReader(records)
    existing_homes=[i["Property Links"] for i in reader]
    return existing_homes



def get_new_listings(city):

    while(1):
        try:
            city_search = WebDriverWait(driver, 2*60).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='txtMapSearchInput']")))
            city_search.clear()
            city_search.send_keys(city)
            city_search.send_keys(Keys.ENTER)
            time.sleep(10)
            latest_homes = WebDriverWait(driver, 2*60).until(
                EC.element_to_be_clickable((By.ID, 'mapSidebarBodyCon')))
            
            homes=set()
            home_links=latest_homes.find_elements(By.XPATH, "//a[contains(@href, '/real-estate/')]")
            for i in home_links:
                homes.add(i.get_attribute("href"))

            existing_homes=read_records()
            for home in homes:
                if home in existing_homes:
                    print("homes is not new")
                else:
                    print("its new")
                    writer.writerow({'City Name': city, 'Property Links': home})
                    asyncio.run(send_message(home,city))

        except:
            print("Couldnt load the dom refreshing to load again")
            driver.refresh()
            time.sleep(5)
            continue
        else:
            break
        
    



url="https://www.realtor.ca/map"
chrome_options = ChromeOptions()
prefs = {
    "profile.default_content_setting_values.notifications": 2, 
    "profile.default_content_setting_values.geolocation": 2     
    }
chrome_options.add_experimental_option("prefs", prefs)

driver = Chrome(driver_executable_path=r"C:\Users\MOHSIN ARIF\Downloads\chromedriver.exe",
                options=chrome_options
                )
driver.get(url)
driver.maximize_window()
time.sleep(60) # its bcuz site takes time to load

cities=["toronto","quebec","ottawa"]
while(1):
    for city in cities:
        print(f"city name: {city}\n")
        get_new_listings(city)
    time.sleep(2*60)    
    driver.refresh()
        

