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
from zipfile import ZipFile


args = sys.argv
print(args)
repo = args[1].replace('`','')
search_string = args[2].replace('`','')
print( "Download : {0} | File {1}" .format(search_string, 'https://github.com/'+repo+'/archive/master.zip') )
directory_zip = '.\\Repos-Files\\{0}\\{1}'.format(search_string, repo.replace('/','.'))
path_zip = os.getcwd() + directory_zip[1:] + '\\'
print(f"Path :  {path_zip} ")
options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-notifications")
options.add_argument('--no-sandbox')
options.add_argument('--verbose')
options.add_experimental_option("prefs", {
        "download.default_directory": f"{path_zip}",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agents = user_agent_rotator.get_user_agents() # Get list of user agents.
user_agent = user_agent_rotator.get_random_user_agent() # Get Random User Agent String. 


driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver.exe')


# https://stackoverflow.com/questions/53161173/how-to-rotate-various-user-agents-using-selenium-python-on-each-request?answertab=votes#tab-top
driver.execute_cdp_cmd(f'Network.setUserAgentOverride', {"userAgent": f'{user_agent_rotator.get_random_user_agent()}'})
print(driver.execute_script("return navigator.userAgent;")) # This would change the user string of the driver



try:
    driver.get('https://github.com/'+repo+'/archive/master.zip')
    time_to_wait = 10
    time_counter = 0
    while not os.path.exists(path_zip+repo.split('/')[1]+"-master.zip"):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:break
    with ZipFile(path_zip+repo.split('/')[1]+"-master.zip", 'r') as zipObj:
        zipObj.extractall(path_zip)
    print(f"done file : {path_zip}")
    driver.close()
    os.remove(path_zip+repo.split('/')[1]+"-master.zip") # path_zip+repo.split('/')[1]+"-master.zip" shouold be deleted
except Exception as e:
    driver.close()
    print(traceback.print_exc())
    print("Exception 2")
