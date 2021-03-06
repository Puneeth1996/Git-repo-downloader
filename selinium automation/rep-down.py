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
search_string = args[1]


download_directory = '.\\Repos-Files\\{0}\\'.format( search_string.replace('\\', '|') )
if not os.path.exists(download_directory):
    os.makedirs(download_directory)



directory = '.\\Repos-Links\\{0}\\'.format( search_string.replace('\\', '|') )
with open(directory + 'Repos-Links.txt') as result:
    uniqlines = set(result.readlines())
    with open(directory + 'Repos-Links.txt', 'w') as rmdup:
        rmdup.writelines(set(uniqlines))





with open(directory + 'Repos-Links.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

# print(content)






def cpu_count():
    ''' Returns the number of CPUs in the system
    '''
    num = 1
    if sys.platform == 'win32':
        try:
            num = int(os.environ['NUMBER_OF_PROCESSORS'])
        except (ValueError, KeyError):
            pass
    elif sys.platform == 'darwin':
        try:
            num = int(os.popen('sysctl -n hw.ncpu').read())
        except ValueError:
            pass
    else:
        try:
            num = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, OSError, AttributeError):
            pass

    return num

def exec_commands(cmds):
    ''' Exec commands in parallel in multiple process 
    (as much as we have CPU)
    '''
    if not cmds: return # empty list

    def done(p):
        return p.poll() is not None
    def success(p):
        return p.returncode == 0
    def fail():
        sys.exit(1)

    max_task = cpu_count()
    processes = []
    while True:
        while cmds and len(processes) < max_task:
            task = cmds.pop()
            print(list2cmdline(task))
            processes.append(Popen(task))

        for p in processes:
            if done(p):
                if success(p):
                    processes.remove(p)
                else:
                    fail()

        if not processes and not cmds:
            break
        else:
            time.sleep(0.05)



commands = []
for rep in content:
	commands.append(['python','file_down.py','"%s"' %rep, '"%s"' %search_string ])
exec_commands(commands)



