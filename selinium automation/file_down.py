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
from subprocess import Popen, list2cmdline
import shutil




args = sys.argv
# print(args)
search_string = args[1].replace('`','')
print( "Download : {0} | File {1}" .format(search_string, 'https://github.com/'search_string+'/archive/master.zip') )

options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
options.add_argument("start-maximized")

# https://stackoverflow.com/questions/54035436/headless-is-not-an-option-in-chrome-webdriver-for-selenium-python

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

# Get list of user agents.
user_agents = user_agent_rotator.get_user_agents()
# print(user_agents)

# Get Random User Agent String.
user_agent = user_agent_rotator.get_random_user_agent()
# print(user_agent)

# https://stackoverflow.com/questions/53161173/how-to-rotate-various-user-agents-using-selenium-python-on-each-request?answertab=votes#tab-top
driver.execute_cdp_cmd(f'Network.setUserAgentOverride', {"userAgent": f'{user_agent_rotator.get_random_user_agent()}'})
print(driver.execute_script("return navigator.userAgent;")) # This would change the user string of the driver


driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver.exe')




try:
    pass
except Exception as e:
    # driver.close()
    print(traceback.print_exc())
    print("Exception 2")
