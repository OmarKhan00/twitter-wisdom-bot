'''
Selenium Tutorial (https://www.youtube.com/watch?v=Xjv1sY630Uc&list=PLzMcBGfZo4-n40rB1XaJ0ak1bemvlqumQ&index=1)
'''

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context
prompt = "Dumbest celebrity quotes that have aged poorly"#"Imran Khan Famous Quotes"


def get_results(driver):
    '''
    Returns a list of links on the current page.

            Parameters:
                    driver (webdriver.Chrome()): a webdriver instance

            Returns:
                    list_of_links (list): a list of web elements with each element containing a link
    '''

    try: 
        results_page = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        list_of_search_results = results_page.find_elements_by_class_name("MjjYud")
        list_of_links = []
        for search_result in list_of_search_results:
            link = search_result.find_element_by_tag_name("a")
            list_of_links.append(link)
            # print(link.get_attribute("href"))
    finally:
        # print("Results page rendered")
        return list_of_links

    

def get_quotes_from_this_page(driver, list_of_links: list, dict_of_quotes: dict, temp_list_of_quotes: list, index: int):
    '''
    Returns a dictionary of all the quotes on that link page.

            Parameters:
                    driver (webdriver.Chrome()): a webdriver instance
                    list_of_links (list): a list of web elements with each element containing a link
                    dict_of_quotes (dict): a dictionary of all the quotes and their respective sources
                    temp_list_of_quotes (list): a temporary list to store all formatted quotes before passing them into dictionary
                    index (int): an integer to keep track of the number of quotes added to the dictionary

            Returns:
                    dict_of_quotes (dict): an updated dictionary of all the quotes and their respective sources
                    temp_list_of_quotes (list): an updated temporary list to store all formatted quotes before passing them into dictionary
                    index (int): an updated integer to keep track of the number of quotes added to the dictionary

    '''

    source = None
    for link in list_of_links:
        try:
            try: 
                results_page = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "search"))
                )
            except:
                print("Could not load google results page")

            if not source:
                source = link.get_attribute("href")
            link.click()
            delay = 30 # seconds
            # test = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "“")]')))
            # print("Page is ready!")
            driver.implicitly_wait(delay)
            unformatted_quotes = driver.find_elements_by_xpath('//*[contains(text(), "“") and contains(text(), "”")]')
            if not unformatted_quotes:
                unformatted_quotes = driver.find_elements_by_xpath('//*[contains(@href, "quote")]')
            if not unformatted_quotes:
                unformatted_quotes = driver.find_elements_by_tag_name('blockquote')
                # print(f"Yep, I have at least an element -> {unformatted_quotes[0].text}")
            if unformatted_quotes:
                # print(f"The element you are looking for -> {unformatted_quotes[0].text}")
                for unformatted_quote in unformatted_quotes:
                    if len(unformatted_quote.text) > 50 and "quote" not in unformatted_quote.text.lower():
                        print(f"Unformatted text -> {unformatted_quote.text}")
                        # if "“" in unformatted_quote.text:
                        #     formatted_quote = unformatted_quote.text.split('“')[1]
                        #     formatted_quote = formatted_quote.split('”')[0]
                        if "“" in unformatted_quote.text[0]:
                            formatted_quote = unformatted_quote.text.replace("“", "")
                            formatted_quote = formatted_quote.replace('”', "")                        
                        else:
                            formatted_quote =  unformatted_quote.text
                        formatted_quote = formatted_quote.upper()
                        if formatted_quote[-1] != "." and formatted_quote[-1] != "?" and formatted_quote[-1] != "!":
                            formatted_quote = "".join([formatted_quote, "."])
                        formatted_quote = re.sub(u"(\u2018|\u2019)", "'", formatted_quote)
                        formatted_quote = re.sub(u"(\u2013|\u2014|\u201c)", " ", formatted_quote)
                        formatted_quote = re.sub(u"(\u2026)", "...", formatted_quote)
                        formatted_quote = re.sub(u"(\n)", " ", formatted_quote)
                        if formatted_quote not in temp_list_of_quotes and len(formatted_quote) > 40:
                            temp_list_of_quotes.append(formatted_quote)
                            dict_of_quotes[index] = {'quote': formatted_quote, 'source': source}
                            index += 1

            print(temp_list_of_quotes)
            driver.back()
            delay += 2
            driver.implicitly_wait(delay)

        except:
            # driver.back()
            print("Requests taking too long")
            return dict_of_quotes, temp_list_of_quotes, index


    return dict_of_quotes, temp_list_of_quotes, index

def get_all_quotes(prompt: str, number_of_pages: int):
    '''
    The main overarching function, which executes all the other tasks.

            Parameters:
                    number_of_pages (int): an integer defining the number of pages to use from the google search results

            Returns:
                    N/A (string): message to confirm the collection of quotes
    '''

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True  
    profile=webdriver.ChromeOptions()
    profile.add_argument('--ignore-certificate-errors')
    profile.add_argument('--disable-web-security')

    driver = webdriver.Chrome(executable_path=PATH, desired_capabilities=caps, options=profile)

    url = "http://www.google.com"
    driver.get(url)

    time.sleep(2)

    search_bar = driver.find_element_by_name("q")
    search_bar.clear()
    search_bar.send_keys(prompt)
    search_bar.send_keys(Keys.RETURN)
    dict_of_quotes = {}
    temp_list_of_quotes = []
    index = 0
    delay = 40
    for i in range(number_of_pages):
        print(f"Page {i+1}")
        list_of_links = get_results(driver)
        dict_of_quotes, temp_list_of_quotes, index  = get_quotes_from_this_page(driver, list_of_links, dict_of_quotes, temp_list_of_quotes, index)
        print("We have reached here!")
        try: 
            results_page = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.ID, "search"))
                )
            page_navigation = driver.find_element_by_id("main") 
            next_page_btn = page_navigation.find_element_by_id("pnnext")
            next_page_btn.click()
            delay += 5
        except:
            print("Can not locate the main search results page")

    with open("assets/quotes/quotes2.json", "w") as outfile:
        json.dump(dict_of_quotes, outfile, separators=(',', ':'), indent=4)

    time.sleep(2)
    print(dict_of_quotes.values)
    driver.quit()

    return "Quotes successfully collected"

if __name__ == "__main__":
    get_all_quotes(prompt, 3)