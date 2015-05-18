# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from win32com import *
from win32com.client import Dispatch
from AutoItLibrary import AutoItLibrary
import HTMLTestRunner
import sys, time 



account={"username":"dongjie",
         "password":"ZXzx123?"}

profileDict={"firefox":r"C:\Users\cfds\AppData\Roaming\Mozilla\Firefox\Profiles\3v7ol8zw.default",
            "ie":"",
            "chrome":""}

Driverpath={"chrome":r"C:\Users\cfds\AppData\Local\Google\Chrome\Application\chromedriver.exe"
            }

def get_screenshot(filename):
    '''
    Save screenshot when case failed
    usage:
    save_screenshot(r"C:\screenshot.png")
    '''
    print "Save screenshot..."
    #driver.Remote.get_screenshot_as_file(filename)
def open_configured_browser(base_url,brower_type="firefox"):
    '''
    Loading a configured browser, or it will launch with a pure environment
    '''
    #Load profile
    if brower_type.lower()=="firefox":
        profile = webdriver.FirefoxProfile(profileDict[brower_type.lower()])
        driver = webdriver.Firefox(profile)
    elif brower_type.lower()=='ie':
        driver = webdriver.Ie()
    elif brower_type.lower()=='chrome':
        #driver = webdriver.Chrome(executable_path=Driverpath[brower_type.lower()])
        option = webdriver.ChromeOptions()
        option.add_argument('test-type')
        driver = webdriver.Chrome(executable_path=Driverpath[brower_type.lower()], chrome_options=option)
    driver.implicitly_wait(30)
    driver.get(base_url)
    sleep(5)
    if brower_type.lower()=="chrome":
        #AutoItX = Dispatch("AutoItX3.Control")
        #AutoItX.send("{ENTER}")
        #AutoItLibrary.WinWaitActive(u"data:, - Google Chrome")
        #AutoItLibrary.send("{ENTER}") 
        pass
    return driver
    
def login_boss(driver,username=account["username"],password=account["password"]):
    '''
    Use the directed account to login BOSS
    '''
    driver.find_element_by_id("j_username").clear()
    driver.find_element_by_id("j_username").send_keys(username)
    driver.find_element_by_id("j_password").clear()
    driver.find_element_by_id("j_password").send_keys(password)
    #driver.find_element_by_id("code").clear()
    #driver.find_element_by_id("code").send_keys("6637")
    driver.find_element_by_id("loginForm").submit()
    sleep(5)
    return driver

