# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#opens chrome window
browser = webdriver.Chrome()

"""Put the website(s) you wish to crawl in the term dictionary"""
term_dict = []
results = {}

for i in term_dict:
    term = i

    #opens the ICANN lookup
    browser.get("https://lookup.icann.org/en")
 
    #finds the text box by it's ID
    element = browser.find_element(By.ID,"input-domain")

    #inputs your domain into the text box
    element.send_keys(term, Keys.ENTER)

    timeout = 100 #waits 100 seconds before timeout

    #try except block for checking if page has loaded
    try:
        myElem = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "information-panel--heading")))
    except TimeoutException:
        print("Loading took too much time!")

    #try except block for checking if page is taken or available 
    try:
        element = driver.find_element(By.CLASS_NAME, "information-panel--heading")
        results[term] = "Taken"
    except:
        results[term] = "Available"

#printing results to the console
for i in results:
    print(i, results[i])

