import requests
from selenium import webdriver
from PIL import Image
from io import BytesIO
from time import sleep
from bs4 import BeautifulSoup
import sys
import os

if len(sys.argv) == 1:
  print("Usage : python InstaDownloader.py 'url'\nEx)python InstaDownloader.py https://www.instagram.com/p/BrQNqCBgzpy/")
  exit()

def find(_soup):
  path = ""
  items = []
  for total_div in range(20):
    for first in range(total_div + 1):
      path = "#react-root > section > main" + (" > div" * first) + " > article" + (" > div" * (total_div - first)) + " > img"
      items.extend(_soup.select(path))

      for second in range(total_div - first + 1):
        path = "#react-root > section > main" + (" > div" * first) + " > article" + (" > div" * second) + " > ul > li" + (" > div" * (total_div - first - second)) + " > img"
        items.extend(_soup.select(path))

  return items

url = sys.argv[1]

driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe')

driver.get(url)
driver.implicitly_wait(3)
sleep(1)

url_check = set()

j = 0
while True:
  driver.implicitly_wait(3)
  sleep(1)
  items = find(BeautifulSoup(driver.page_source, "html.parser"))
  print(len(items))
  url_part = driver.current_url.replace("/", "").replace("https:www.instagram.com", "")
  for item in items:
    try:

      url = item['src']
      print(url)
      if url in url_check: continue
      url_check.add(url)

      while True:
        response = requests.get(url)
        if str(response) != "<Response [200]>": continue
        if os.path.isfile("%s_%d.jpg"%(url_part, j)):
          print("File already exists, so it stops here.")
          driver.quit()
          exit()
        Image.open(BytesIO(response.content)).save("%s_%d.jpg"%(url_part, j))
        print("%d_%d.jpg downloaded"%(0, j))
        break

      j += 1
    except KeyError as e:
      print(str(e))

  next_image_button = driver.find_elements_by_class_name("coreSpriteRightChevron")
  if len(next_image_button) == 0: break
  next_image_button[0].click()

driver.quit()
