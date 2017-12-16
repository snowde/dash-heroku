# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import re
from lxml import html
import time
import csv

url = 'https://www.glassdoor.com/Reviews/BJ-s-Restaurants-Reviews-E6490.htm'
filename = url.split('/')[-1].split('.')[0] + '.csv'

chromedriver = "C:/chromedriver"
chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chromedriver, chrome_options=chromeOptions)

driver.get(url)

driver.find_element_by_xpath('//span[@class="ratingsDetailsLink link"]').click()
element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "Accordion")))

X = True
while X:
    try:
        overall_rating = driver.find_element_by_xpath('//div[@data-label-key="modRatingDetailsLabelOverall"]').text.split()[-1]
        culture_rating = driver.find_element_by_xpath('//div[@data-label-key="modRatingDetailsLabelCultureValues"]').text.split()[-1]
        work_life_balance = driver.find_element_by_xpath('//div[@data-label-key="modRatingDetailsLabelWLB"]').text.split()[-1]
        senior_management = driver.find_element_by_xpath('//div[@data-label-key="modRatingDetailsLabelMgmt"]').text.split()[-1]
        comp_and_benefits = driver.find_element_by_xpath('//div[@data-label-key="modRatingDetailsLabelComp"]').text.split()[-1]
        career_opportunities = driver.find_element_by_xpath('//div[@data-label-key="modRatingDetailsLabelCareerOpps"]').text.split()[-1]
        recommend_to_a_friend = driver.find_element_by_xpath('//div[@id="Recommend"]').text
        ceo_approval = driver.find_element_by_xpath('//div[@id="CeoRating"]').text
        positive_business_outlook = driver.find_element_by_xpath('//div[@id="BizOutlook"]').text
    except IndexError:
        continue

    data = {'Overall': overall_rating, 'Culture': culture_rating, 'Work Life': work_life_balance,
            'Senior Management': senior_management, 'Comp and Benefits': comp_and_benefits,
            'Career Opportunities': career_opportunities, 'Recommend to Friend': recommend_to_a_friend,
            'CEO approval': ceo_approval, 'Positive Business Outlook': positive_business_outlook}


    with open(filename, 'a+', encoding='utf-8', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=data.keys())
        if not os.fstat(output.fileno()).st_size > 0:
            writer.writeheader()
        writer.writerow(data)
    print('Done')
    X = False