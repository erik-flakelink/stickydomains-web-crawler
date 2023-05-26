# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# create webdriver object
driver = webdriver.Chrome()

term_dict = ["1.com", "1.net", "1.org", "2.com", "2.net", "2.org", "3.com", "3.net", "3.org", "4.com", "4.net", "4.org", "5.com", "5.net", "5.org", "6.com", "6.net", "6.org", "7.com", "7.net", "7.org", "8.com", "8.net", "8.org", "9.com", "9.net", "9.org", "10.com", "10.net", "10.org"]
results = {}

for i in term_dict:
    term = i

    #opens the ICANN lookup
    driver.get("https://lookup.icann.org/en")
 
    #finds the text box by it's ID
    element = driver.find_element(By.ID,"input-domain")

    #inputs "g.org" into the text box
    element.send_keys(term, Keys.ENTER)

    time.sleep(3)
    try:
        element = driver.find_element(By.CLASS_NAME, "information-panel--heading")
        results[term] = "Taken"
    except:
        results[term] = "Available"

for i in results:
    print(i, results[i])
