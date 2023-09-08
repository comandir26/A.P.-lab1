from bs4 import BeautifulSoup
import requests
import os #для создания папок
import cv2

def send_requests(url, name):
    ''''
    try:
        html_page = requests.get(str(url) + name, headers={"User-Agent":"Mozilla/5.0"}, timeout = 3) # 3 seconds
    except requests.exceptions.Timeout:
        print("Timed out")
    '''
    html_page = requests.get(str(url) + name, headers={"User-Agent":"Mozilla/5.0"}, timeout = 3)
    soup = BeautifulSoup(html_page.text, "html.parser")
    img_links = soup.find_all('img', class_ = 'serp-item__thumb justifier__thumb')
    return img_links

def make_folders(names):
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    os.chdir('dataset') #либо makedirs и рекурсивно создать папки
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

url = "https://yandex.ru/images/search?text="
make_folders(('polar_bear', 'brown_bear'))

polarbear_links = send_requests(url, 'polarbear')
load_images(polarbear_links, 'polar_bear')

brownbear_links = send_requests(url, 'brownbear')
load_images(brownbear_links, 'brown_bear')