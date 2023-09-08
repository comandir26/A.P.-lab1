from bs4 import BeautifulSoup
import requests
import os #для создания папок
import cv2


URL = "https://yandex.ru/images/search?text=polarbear"
html_page = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}, timeout = 3)
soup = BeautifulSoup(html_page.text, "html.parser")#or html_page.content?
img_links = soup.find_all('img', class_ = 'serp-item__thumb justifier__thumb')
number = 0

if not os.path.isdir('dataset'):
    os.mkdir('dataset')

os.chdir('dataset') # либо makedirs и рекурсивно создать папки

if not os.path.isdir('polar_bear'):
    os.mkdir('polar_bear')

if not os.path.isdir('brown_bear'):
    os.mkdir('brown_bear')
'''
for img_link in img_links:
    try:
        link = img_link.get('src')
        img = requests.get('https:' + str(link))
        with open(str(number) + '.jpg', 'wb') as f:
            f.write(img.content)
    except:
        continue
    number+=1
'''