# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import requests



#opens chrome window
options = webdriver.ChromeOptions()
options.add_argument("headless") #makes it so that you don't see the browser pop up
options.add_argument("--log-level=3") #clears all the clutter 
options.add_argument('--ignore-certificate-errors') #just in case necessary
options.add_argument('--allow-running-insecure-content') #just in case necessary
browser = webdriver.Chrome(chrome_options=options)


"""Modify the term_dict to lookup your domains!"""
term_dict = ["wawreusaeryaye1.org","2.com","1.com"]
results = {}
creation_date = {}
parked_list = {}

#use ICANN to lookup availability and year of creation
def ICANN_lookup(term_dict):
    for i in term_dict:
        term = i

        #opens the ICANN lookup
        browser.get("https://lookup.icann.org/en")
 
        #finds the text box by it's ID
        element = browser.find_element(By.ID,"input-domain")

        #inputs your domain into the text box
        element.send_keys(term, Keys.ENTER)


        timeout = 10 #waits 10 seconds before timeout

        #try except block for checking if page has loaded
        try:
            WebDriverWait(browser,timeout).until(lambda browser : browser.find_elements(By.XPATH,"//*[contains(text(), 'The requested domain was not found')]") or browser.find_elements(By.CLASS_NAME,"information-panel--heading"))
        except TimeoutException:
            print("Loading took too much time!")

        #try except block for detecting if a website has been taken
        try:
            element = browser.find_element(By.CLASS_NAME, "information-panel--heading")
            results[term] = "Taken"
        except:
            results[term] = "Available"

        #finds year of creation
        if results[term] == "Taken":
            dateElem = browser.find_element(By.CSS_SELECTOR,".date.registry-created")
            creation_date[term] = dateElem.text
        else:
            creation_date[term] = "Not created yet"

#checks if a domain is parked
def parked(term_dict):


    for i in term_dict:
        if results[i] == "Taken":
            
            try:
                response = requests.get(f'https://{i}')
                if response.status_code == 404:
                    parked_list[i] = "Parked"
                else:
                    parked_list[i] = "Taken"
            except:
                parked_list[i] = "Parked"
        else:    
            parked_list[i] = "Available"

#prints the information you have crawled 
def print_all(term_dict,results,creation_date,parked):
    for i in term_dict:
        print(f"{i, results[i]},{parked_list[i]},Created on: {creation_date[i]} \n")

#play around down here to find the information you need
ICANN_lookup(term_dict)
parked(term_dict)
print_all(term_dict,results,creation_date,parked)

