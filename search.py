from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import urllib.request
import requests
import time
import re
import json
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import common.logging as log


driver = Chrome()
wait = WebDriverWait(driver, 1)
driver.maximize_window()

def searchRelatedKeywordGoogle(query):
    driver.get('https://www.google.com')
    if insert('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input', query):
        return ''

    if click('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]'):
        return ''
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    keywords = reads('//*[@id="brs"]/g-section-with-header/div[2]/div/p')
    return keywords

def searchRelatedKeywordNaver(query):
    driver.get('https://www.naver.com')
    if insert('//*[@id="query"]', query):
        return ''

    if click('//*[@id="search_btn"]'):
        return ''

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    keywords = reads('//*[@id="nx_related_keywords"]/dl/dd[1]/ul/li')

    return keywords

def searchRelatedKeywordDaum(query):
    driver.get('https://www.daum.net')
    if insert('//*[@id="q"]', query):
        return ''

    if click('//*[@id="daumSearch"]/fieldset/div/div/button[2]'):
        return ''
    
    click('//*[@id="netizen_more_btn_bottom"]')
    keywords = reads('//*[@id="netizen_lists_bottom"]/span[@class="wsn"]')
    return keywords

def click(xpath): 
    try:
        wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
        driver.find_element_by_xpath(xpath).click()
    except:
        log.debug('Cannot Click:' + xpath)

def insert(xpath, value):
    try:
        wait.until(ec.visibility_of_all_elements_located((By.XPATH, xpath)))
        driver.find_element_by_xpath(xpath).send_keys(value)
    except:
        log.debug('Cannot Insert:' + xpath)

def read(xpath):
    try:
        wait.until(ec.visibility_of_all_elements_located((By.XPATH, xpath)))
        text = driver.find_element_by_xpath(xpath).text
        return text.split()
    except:
        log.debug('Cannot Read:' + xpath)
        return []

def reads(xpath):
    try:
        wait.until(ec.visibility_of_all_elements_located((By.XPATH, xpath)))
        elements = driver.find_elements_by_xpath(xpath)
        texts = []
        for element in elements:
            texts.append(element.text)
        return texts
    except:
        log.debug('Cannot Read:' + xpath)
        return []
