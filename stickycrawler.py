# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests




#configuring the chrome window, change the executable path to the path of your chrome driver!
service = Service(executable_path=r'Change me!')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless") #makes it so that you don't see the browser pop up
chrome_options.add_argument("--log-level=3") #clears all the clutter 
chrome_options.add_argument('--ignore-certificate-errors') #just in case necessary
chrome_options.add_argument('--allow-running-insecure-content') #just in case necessary
browser = webdriver.Chrome(service=service,options=chrome_options)

#contains all of the functions necessary to make the lookup work
class lookup():
    def __init__(self,term_dict):
        self.term_dict = term_dict #list of domains to crawl
        self.results = {} #availability of domain
        self.creation_date = {} #The year the domain was first created
        self.parked_list = {} #checks if domain is parked

    #use ICANN to lookup availability and year of creation
    def ICANN_lookup(self):
        for i in self.term_dict:
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
                self.results[term] = "Taken"
            except:
                self.results[term] = "Available"

            #finds year of creation
            if self.results[term] == "Taken":
                dateElem = browser.find_element(By.CSS_SELECTOR,".date.registry-created")
                self.creation_date[term] = dateElem.text[0:4]
            else:
                self.creation_date[term] = "Not created yet"

    #checks if a domain is parked
    def parked(self):


        for i in self.term_dict:
            if self.results[i] == "Taken":
            
                try:
                    response = requests.get(f'https://{i}')
                    if response.status_code == 404:
                        self.parked_list[i] = "Parked"
                    else:
                        self.parked_list[i] = "Taken"
                except:
                    self.parked_list[i] = "Parked"
            else:    
                self.parked_list[i] = "Available"

    #prints the information you have crawled 
    """Run this after you have obtained all other information!"""
    def print_all(self):
        for i in self.term_dict:
                print(f"{i, self.results[i]},{self.parked_list[i]},Created in: {self.creation_date[i]} \n")


#play around down here to find the information you need

"""Modify the term_dict to lookup your domains!"""
lookup1 = lookup(["wawreusaeryaye1.org","2.com","1.com"])

lookup1.ICANN_lookup()
lookup1.parked()
lookup1.print_all()

