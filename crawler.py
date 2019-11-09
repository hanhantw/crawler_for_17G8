# -*- coding: utf-8 -*-
"""記帳Crawler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XbJ5OW3r1VxXIPHANLkiStHu5JipR7x2
"""

import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import load_workbook

colums = ['日期', '品項', '類別', '金額']

today = datetime.date.today()
# print(month)
# start_date = str(today.replace(day=1))
# end_date = str(today)
start_date = '2019-05-01'
end_date = '2019-05-30'
uid = ''
url = f"https://www.checkchick.me/liff_analyzeExpenditure.php?userid={uid}&start={start_date}&end={end_date}&mix=0"
resp = requests.get(url) # html

all_items = []
if resp.status_code == requests.codes.ok:
  soup = BeautifulSoup(resp.text, "lxml")
  categ_tag = soup.find_all("div", class_="accordion")
  item_tag = soup.find_all("div", class_="panel")
  for i in range(0, len(categ_tag)):
    categ = categ_tag[i].find("span", class_="accordionSpan").text.strip().split('$')[0]
    for item in item_tag[i].find_all("li"):
      date_item_price = [line.strip() for line in item.text.strip().splitlines() if line.strip() != '']
      date_item_price.insert(-1, categ)
      all_items.append(date_item_price)
  df = pd.DataFrame(all_items, columns = colums)
  with pd.ExcelWriter('2019-05.xlsx') as writer:
    df.to_excel(writer, sheet_name = '2019年05月', index = None, header=True)