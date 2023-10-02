import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions 
import requests
from bs4 import BeautifulSoup
import cv2

def send_requests(url, name, html_page):
    result = []
    page = 1
    while True:
        full_url = url + name #+ "?p=" + str(page)
        try: 
            html_page.get(full_url)  
            html_page.find_element(By.CLASS_NAME, "CheckboxCaptcha-Anchor").click()
        except exceptions.NoSuchElementException:
            print('No Captcha') 
        img_links = html_page.find_elements(By.CLASS_NAME, 'serp-item__link')
        if len(img_links) > 0:
            page+=1
        result += img_links
        print(len(result)) 
        time.sleep(2) 
        if len(result) > 0:
            #html_page.quit()
            break   
    return result

def make_folders(names):
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    os.chdir('dataset')
    if not os.path.isdir(names[0]):
        os.mkdir(names[0])
    if not os.path.isdir(names[1]):
        os.mkdir(names[1])

def load_images(links, filename):
    os.chdir(filename)
    img_page = webdriver.Edge()
    for number, link in enumerate(links): 
        time.sleep(3)
        href = link.get_attribute('href')
        img_page.get(href)
        time.sleep(2)
        try:
            #img_origin = img_page.find_element(By.CLASS_NAME, "MMImage-Origin")
            img_origin = img_page.find_element(By.CLASS_NAME, "MMImage-Origin")
        except exceptions.NoSuchElementException:
            print("No such element")
            continue
        img_link = img_origin.get_attribute('src')
        response = requests.get(img_link, timeout=3)
        time.sleep(2)
        with open(str(number).zfill(4) + '.jpg', 'wb') as f:
            f.write(response.content)
            print('Success')
        
    os.chdir('..')
    img_page.close()
    print(os.getcwd())



url = "https://yandex.ru/images/search?text="
class1 = "polarbear"
class2 = "brownbear"

'''
if os.path.isdir("dataset/" + class1) and os.path.isdir("dataset/" + class2):
   shutil.rmtree("dataset/" + class1) 
   shutil.rmtree("dataset/" + class2)
'''   

make_folders((class1, class2))

html_page = webdriver.Edge()

polarbear_links = send_requests(url, class1, html_page)
load_images(polarbear_links, class1)

time.sleep(5)

brownbear_links = send_requests(url, class2, html_page)
load_images(brownbear_links, class2)

#html_page.close()