import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions 
import requests
import cv2

def send_requests(url, name):
    result = []
    page = 1
    '''
    while True:
        html_page = requests.get(url + name + "?page=" + str(page), headers={'User-Agent':'Mozilla/5.0'})
        soup = BeautifulSoup(html_page.text, "html.parser")
        img_links = soup.find_all("a", class_ = "serp-item__link")     
        if len(img_links) > 0:
            page+=1
        result += img_links
        print(len(result)) 
        time.sleep(5) 
        if len(result) > 0:
            break
    '''  
    html_page = webdriver.Edge()
    while True:
        try: 
            html_page.get(url + name)#+ "?p=" + str(page)  
            html_page.find_element(By.CLASS_NAME, "CheckboxCaptcha-Anchor").click()
        except exceptions.NoSuchElementException:
            print('No Captcha') 
        img_links = html_page.find_elements(By.CLASS_NAME, 'serp-item__link')
        if len(img_links) > 0:
            page+=1
        result += img_links
        print(len(result)) 
        time.sleep(5) 
        if len(result) > 0:
            break
        html_page.quit()
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
    for number, link in enumerate(links):
        #image_page = webdriver.Edge()
        href = link.get_attribute('href')
        #response = requests.get(href)
        response = None    
        while response is None:    
            try:
                response = requests.get(href, timeout=3)
                break
            except requests.exceptions.ConnectionError as e: 
                print(e)
                time.sleep(5)
                continue
        
        with open(str(number).zfill(4) + '.jpg', 'wb') as f:
            f.write(response.content)
            print('Success')
        time.sleep(2)

    os.chdir('..')
    print(os.getcwd())



url = "https://yandex.ru/images/search?text="
class1 = "polarbear"
class2 = "brownbear"

if os.path.isdir("dataset/" + class1) and os.path.isdir("dataset/" + class2):
   shutil.rmtree("dataset/" + class1) 
   shutil.rmtree("dataset/" + class2)    

make_folders((class1, class2))

polarbear_links = send_requests(url, class1)
load_images(polarbear_links, class1)

time.sleep(7)

brownbear_links = send_requests(url, class2)
load_images(brownbear_links, class2)