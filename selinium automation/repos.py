import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import glob
import configparser as cp 
import csv
import sys, re
import time
import traceback
import zipfile
import random




options = Options()
options.add_argument('--log-level=3')
options.add_argument("start-maximized")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# user_agent_string = "My_User_Agent_String" # please chagne the string to user agent
# opts.add_argument("user-agent=%s" % ( user_agent_string ) ) # adding the user agent 

args = sys.argv
# print(args)
search_string = args[1]


# https://stackoverflow.com/questions/54035436/headless-is-not-an-option-in-chrome-webdriver-for-selenium-python

# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=options, executable_path='chromedriver.exe')


directory = '.\\Repos-Links\\{0}\\'.format( search_string.replace('\\', '|') )
if not os.path.exists(directory):
    os.makedirs(directory)

# outname = directory = '.\\Completed\\{0}\\repos.txt'.format( search_string.replace('/', '') )
# if os.path.exists(outname) == False:
#     with open(outname,"w",newline="") as wd:
#         wr = csv.writer(wd)
#         wr.writerow(["Par"])
#     wd.close()



# search_string = str(input("Please enter the search term to download repos: ")).replace('\n', '')
# print(f"Gathering all the repos for the string = {search_string}.")






def make_search():
    # http://github.com/search?q=big+data&type=
    print(f"GET: http://github.com/search?q={ search_string.replace(' ', '+') }&type=")
    driver.get(f"http://github.com/search?q={ search_string.replace(' ', '+') }&type=")
    print("The requested search url is loaded.")



def grab_repos_name():
    return [ div.text.replace("\n","") for div in driver.find_elements_by_xpath('//div[@class="f4 text-normal"]') ]



try:
    make_search()
    all_results = []
    # make pagination 
    flag = 1
    while flag:
        page_repos = grab_repos_name()
        # print("The Page Repos = ", page_repos)
        all_results.extend(page_repos)
        # as long as there is a next button present keep going 
        next_button = driver.find_element_by_xpath('//a[@class="next_page"]')
        if('disabled' not in next_button.get_attribute("class")):
            # print("\t\t\t Moving to next page . . . ")
            time.sleep(random.randint(1, 3))
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(random.randint(1, 3))
        else:
            print("Last page")
            flag = 0
    with open(directory + 'Repos-Links.txt', 'w') as f:
        for item in all_results:
            f.write("%s\n" % item)

    # driver.close()
    print("Script is completed.")
except Exception as e:
    # driver.close()
    print(traceback.print_exc())
    print("Exception 2")

























