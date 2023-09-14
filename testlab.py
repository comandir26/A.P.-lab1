import os
import shutil
import time
import random
from bs4 import BeautifulSoup
import requests
import cv2

def send_requests(url, name):
    result = []
    for page in range(1, 10):
        html_page = requests.get(str(url) + name + "?page=" + str(page), headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(html_page.text, "html.parser")
        img_links = soup.find_all('img', class_ = 'serp-item__thumb justifier__thumb')
        result += img_links
        print(len(result))
        time.sleep(5)
    return result

def make_folders(names):
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    os.chdir('dataset')
    if not os.path.isdir(names[0]):
        os.mkdir(names[0])
    if not os.path.isdir(names[1]):
        os.mkdir(names[1])

def load_images(links, filename):
    os.chdir(filename)
    number = 0
    for link in links:
        try:
            link = link.get('src')
            img = requests.get('https:' + str(link))
            with open(str(number).zfill(4) + '.jpg', 'wb') as f:
                f.write(img.content)
        except:
            continue
        number+=1
    os.chdir('..')
    print(os.getcwd())

if os.path.isdir("dataset/polar_bear") and os.path.isdir("dataset/brown_bear"):
    shutil.rmtree("dataset/polar_bear") 
    shutil.rmtree("dataset/brown_bear")    

url = "https://yandex.ru/images/search?text="

make_folders(('polar_bear', 'brown_bear'))

time.sleep(7)
polarbear_links = send_requests(url, 'polarbear')
load_images(polarbear_links, 'polar_bear')

time.sleep(7)
brownbear_links = send_requests(url, 'brownbear')
load_images(brownbear_links, 'brown_bear')