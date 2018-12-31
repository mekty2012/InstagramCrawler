from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from time import sleep
import requests
import os
import sys

if len(sys.argv) == 1:
  print("usage : python InstaCrawler.py \"account_name\"\nEx) python InstaCrawler.py aimin_official")
  exit()

account_name = sys.argv[1]

# body > n div > article > m div > img
# body > n div > article > m div > ul > li > k div > img

foldername = sys.path[0] + "\\" + account_name + "\\"

if not os.path.exists(os.path.dirname(foldername)):
  os.makedirs(os.path.dirname(foldername))


def find(soup_a):
  path = ""
  items = []
  for total_div in range(20):
    for first in range(total_div + 1):
      path = "body" + (" > div" * first) + " > article" + (" > div" * (total_div - first)) + " > img"
      items.extend(soup_a.select(path))

      for second in range(total_div - first + 1):
        path = "body" + (" > div" * first) + " > article" + (" > div" * second) + " > ul > li" + (" > div" * (total_div - first - second)) + " > img"
        items.extend(soup_a.select(path))
    #total_div += 1
  return items

if __name__ == '__main__':
  driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe')

  driver.get("https://www.instagram.com/" + account_name + "/")
  driver.implicitly_wait(3)

  references = driver.find_elements_by_tag_name('a')
  for reference in references:
    if reference.get_attribute('href').startswith('https://www.instagram.com/p/'):
      reference.click()
      break
  # need to update using...?
  i = 0
  while True:
    url_check = set()
    j = 0
    while True:
      driver.implicitly_wait(3)
      sleep(1)
      items = find(BeautifulSoup(driver.page_source, "html.parser"))
      print(len(items))
      for item in items:
        try:

          url = item['src']
          print(url)
          if url in url_check: continue
          url_check.add(url)

          while True:
            response = requests.get(url)
            if str(response) != "<Response [200]>": continue
            Image.open(BytesIO(response.content)).save(foldername + "%d_%d.jpg"%(i, j))
            print("%d_%d.jpg downloaded"%(i, j))
            break

          j += 1
        except KeyError as e:
          print(str(e))

      next_image_button = driver.find_elements_by_class_name("coreSpriteRightChevron")
      if len(next_image_button) == 0: break
      next_image_button[0].click()

    i += 1

    next_page_button = driver.find_elements_by_class_name("coreSpriteRightPaginationArrow")
    if len(next_page_button) == 0: break
    next_page_button[0].click()
