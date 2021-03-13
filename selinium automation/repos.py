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
from selenium.common.exceptions import TimeoutException
import glob
import configparser as cp 
import csv
import sys, re
import time
import traceback
import zipfile
import random



args = sys.argv
# print(args)
search_string = args[1]


options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver.exe')


# This block helps in gathering of the proxies from sslproxies.org page
driver.get("https://sslproxies.org/")
driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
# driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
select = Select(driver.find_element_by_xpath('//select[@name="proxylisttable_length"]'))
select.select_by_visible_text('80')# select by text
# select.select_by_value('1')# select by value 
ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
driver.quit()
proxies = []
for i in range(0, len(ips)):
    proxies.append(ips[i]+':'+ports[i])
print(proxies)
driver.close()


# ------------------------ sEnd of proxies gathering block ------------------------------


# user_agent_string = "My_User_Agent_String" # please chagne the string to user agent
# opts.add_argument("user-agent=%s" % ( user_agent_string ) ) # adding the user agent 



# https://stackoverflow.com/questions/54035436/headless-is-not-an-option-in-chrome-webdriver-for-selenium-python

# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-gpu')



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






def make_search(search_string):
    # http://github.com/search?q=big+data&type=
    print(f"GET: http://github.com/search?q={ search_string.replace(' ', '+') }&type=")
    driver.get(f"http://github.com/search?q={ search_string.replace(' ', '+') }&type=")
    print("The requested search url is loaded.")



def grab_repos_name():
    return [ div.text.replace("\n","") for div in driver.find_elements_by_xpath('//div[@class="f4 text-normal"]') ]





for i in range(0, len(proxies)):
    try:
        make_search(search_string)
        all_results = []
        # make pagination 
        flag = 1
        cnt = 1
        while flag:
            page_repos = grab_repos_name()
            # print("The Page Repos = ", page_repos)
            all_results.extend(page_repos)
            # as long as there is a next button present keep going 
            next_button = driver.find_element_by_xpath('//a[@class="next_page"]')
            
            if('disabled' not in next_button.get_attribute("class")):
                # print("\t\t\t Moving to next page . . . ")
                time.sleep(random.randint(1, 7))
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(random.randint(1, 3))
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(random.randint(1, 10))
                if(cnt == random.randint(2, 6)):
                    cnt = 1
                    print("Proxy selected: {}.".format(proxies[i]))
                    options = webdriver.ChromeOptions()
                    options.add_argument('--proxy-server={}'.format(proxies[i]))
                    driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
                    # driver.get("https://www.whatismyip.com/proxy-check/?iref=home") 
                    driver.get("https://www.whatismyip.com/proxy-check/") #This url changes with above url doesnot show cloudflare captchas 
                    if "Proxy Type" in WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.card-text"))):
                        break
            else:
                print("Last page")
                flag = 0
            cnt = cnt + 1
        with open(directory + 'Repos-Links.txt', 'w') as f:
            for item in all_results:
                f.write("%s\n" % item)
        # driver.close()
        print("Script is completed.")
    except Exception as e:
        # driver.close()
        print(traceback.print_exc())
        print("Exception 2")













