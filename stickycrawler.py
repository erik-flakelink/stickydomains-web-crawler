# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


#opens chrome window
options = webdriver.ChromeOptions()
#options.add_argument("headless")
options.add_argument("--log-level=3")
browser = webdriver.Chrome(chrome_options=options)

term_dict = ["wawreusaeryaye1.org","2.com","1.com"]
results = {}


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

for i in results:
    print(i, results[i])

