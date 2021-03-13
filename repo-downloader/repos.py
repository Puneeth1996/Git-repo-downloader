from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import os  
import glob
import configparser as cp 
import csv
import sys, re
import time
import traceback
import zipfile
import random
import json


def make_search(search_string):
    # http://github.com/search?q=big+data&type=
    print(f"GET: http://github.com/search?q={ search_string.replace(' ', '+') }&type=")
    driver.get(f"http://github.com/search?q={ search_string.replace(' ', '+') }&type=")

def grab_repos_name(driver):
    return [ div.text.replace("\n","") for div in driver.find_elements_by_xpath('//div[@class="f4 text-normal"]') ]



args = sys.argv
if(len(args) >= 1):
    search_string = args[1]
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    options.add_argument("start-maximized")
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver.exe')
    directory = '.\\Repos-Links\\{0}\\'.format( search_string.replace('\\', '|') )
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        make_search(search_string)
        flag = 1
        cnt = 1
        while flag:
            all_results = []
            page_repos = grab_repos_name(driver)
            all_results.extend(page_repos)
            try:
                next_button = driver.find_element_by_xpath('//a[@class="next_page"]')
                if('disabled' not in next_button.get_attribute("class")):
                    time.sleep(random.randint(1, 7))
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(random.randint(1, 3))
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(random.randint(1, 10))
                    if(cnt == random.randint(2, 6)):
                        cnt = 1
                        driver.execute_cdp_cmd(f'Network.setUserAgentOverride', {"userAgent": f'{user_agent_rotator.get_random_user_agent()}'})
                        print(driver.execute_script("return navigator.userAgent;")) # This would change the user string of the driver
            except:
                print("Last page")
                flag = 0
            cnt = cnt + 1
            with open(directory + 'Repos-Links.txt', 'a') as f:
                for item in all_results:
                    f.write("%s\n" % item)
        driver.close()
        with open(directory + 'Repos-Links.txt') as result:
            uniqlines = set(result.readlines())
            with open(directory + 'Repos-Links.txt', 'w') as rmdup:
                rmdup.writelines(set(uniqlines))
        print(f"The links are gathered for : {search_string} | URL : http://github.com/search?q={ search_string.replace(' ', '+') }&type=")
        info = {
            "Search Term" : str(search_string),
            "Search URL" : f"http://github.com/search?q={ search_string.replace(' ', '+') }&type=", 
            "Repo List"  : os.getcwd() + directory[1:] + 'Repos-Links.txt'
        }
        # print(json.dumps(info, indent=4, sort_keys=True))
        path = "result.json"
        with open(path, 'w') as json_file:
            json.dump(info, json_file)
    except Exception as e:
        driver.close()
        print(traceback.print_exc())
        print("Exception 2")



else:
    print("Please Enter the Required Arguments `Search Term`.")

