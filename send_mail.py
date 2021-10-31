import os
import smtplib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

df = pd.read_excel(r'C:\Users\puchaty\PycharmProjects\webscraper_csgostash\sticker_prices.xlsx',sheet_name='Sheet1')[['Nazwa','Link','Ilość']]
df2 = pd.read_excel(r'C:\Users\puchaty\PycharmProjects\webscraper_csgostash\sticker_prices.xlsx',sheet_name='Sheet1')[['Suma','Data']]
df2.dropna(subset = ['Data'], inplace=True)

names = df['Nazwa'].tolist()
amount = df['Ilość'].tolist()
links = df['Link'].tolist()

#stickers = {names[i] : links[i] for i in range(len(names))}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

s = requests.Session()

prices = []

for link in links:
    url = link
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('span', {'class': 'pull-right'}).text.replace('€',"")
    prices.append(price.replace('-','0'))

df['Cena EUR'] = prices

values = []

for i in range(len(prices)):
    values.append(float(prices[i].replace(',','.')) * float(amount[i]))

df['Wartość'] = values

total = round(sum(values),2)

time = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")

dictionary = {'Suma' : [total],
              'Data' : [time],}

df3 = pd.DataFrame.from_dict(dictionary)

df4 = pd.concat([df2,df3],ignore_index=True)

writer = pd.ExcelWriter('sticker_prices.xlsx',engine='xlsxwriter')
workbook = writer.book
worksheet = workbook.add_worksheet('Sheet1')
writer.sheets['Sheet1'] = worksheet
df.to_excel(writer,sheet_name='Sheet1',index=False, startcol=0)
df4.to_excel(writer,sheet_name='Sheet1',index=False , startcol=6)
writer.save()

address = os.environ.get('MAIL_ADDRESS')
password = os.environ.get('MAIL_PASS')

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(address, password)

    subject = f'The total value of my Steam Inventory - {total}'
    body = "".join(list(((f'{names[i]} = {amount[i]} * {prices[i]}€\n') for i in range(len(names)))))
    body2 = f'\nRazem: {total}€'

    msg = f'Subject:{subject}\n\n{body}{body2}'

    smtp.sendmail(address, 'puchatyy@gmail.com', msg.encode('utf-8'))