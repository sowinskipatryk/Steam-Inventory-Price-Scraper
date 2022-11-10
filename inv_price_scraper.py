import os
import smtplib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

addr_from = ''
addr_to = ''
password = ''

names = ['Naklejka | Fnatic (Gold)', 'Naklejka | FaZe (złota)', 'Naklejka | Renegades (foliowana)',
         'Naklejka | Astralis (foliowana)', 'Naklejka | Natus Vincere (foliowana)', 'Naklejka | TYLOO (Foil)',
         'Naklejka | Virtus.pro (foliowana)', 'Naklejka | FaZe (foliowana)', 'Naklejka | Vitality (foliowana)',
         'Naklejka | Spirit (foliowana)', 'Naklejka | Fnatic (Foil)', 'Naklejka | Virtus.pro (hologramowa) | RMR 2020',
         'Naklejka | Spirit (hologramowa)', 'Naklejka | GODSENT (hologramowa) | RMR 2020',
         'Naklejka | TYLOO (hologramowa)', 'Naklejka | Natus Vincere', 'Naklejka | TYLOO', 'Naklejka | Astralis',
         'Naklejka | Vitality', 'Naklejka | Nemiga', 'Naklejka | FaZe', 'Naklejka | Liquid', 'Naklejka | G2',
         'Naklejka | Virtus.pro', 'Naklejka | Spirit', 'Naklejka | GODSENT', 'Naklejka | North', 'Naklejka | FURIA',
         'Naklejka | OG', 'Naklejka | Ninjas in Pyjamas', 'Naklejka | BIG', 'Naklejka | Renegades', 'Naklejka | Boom',
         'Naklejka | Heroic', 'Naklejka | Gen.G', 'Naklejka | ESPADA', 'Naklejka | 100 Thieves',
         'Naklejka | Evil Geniuses', 'Naklejka | Fnatic', 'Kandydaci RMR 2020', 'Pretendenci RMR 2020',
         'Legendy RMR 2020']

amounts = [1, 1, 3, 2, 2, 1, 2, 1, 3, 2, 15, 1, 1, 1, 1, 70, 75, 100, 140, 60, 130, 70, 85, 175, 115, 180, 199, 190,
          180, 245, 140, 255, 225, 195, 250, 260, 186, 215, 1000, 180, 180, 140]

links = ['https://csgostash.com/sticker/3895/Fnatic-Gold-2020-RMR',
         'https://csgostash.com/sticker/3829/FaZe-Gold-2020-RMR',
         'https://csgostash.com/sticker/3827/Renegades-Foil-2020-RMR',
         'https://csgostash.com/sticker/3885/Astralis-Foil-2020-RMR',
         'https://csgostash.com/sticker/3857/Natus-Vincere-Foil-2020-RMR',
         'https://csgostash.com/sticker/3828/TYLOO-Foil-2020-RMR',
         'https://csgostash.com/sticker/3823/Virtuspro-Foil-2020-RMR',
         'https://csgostash.com/sticker/3821/FaZe-Foil-2020-RMR',
         'https://csgostash.com/sticker/3853/Vitality-Foil-2020-RMR',
         'https://csgostash.com/sticker/3856/Spirit-Foil-2020-RMR',
         'https://csgostash.com/sticker/3887/Fnatic-Foil-2020-RMR',
         'https://csgostash.com/sticker/3815/Virtuspro-Holo-2020-RMR',
         'https://csgostash.com/sticker/3848/Spirit-Holo-2020-RMR',
         'https://csgostash.com/sticker/3882/GODSENT-Holo-2020-RMR',
         'https://csgostash.com/sticker/3820/TYLOO-Holo-2020-RMR',
         'https://csgostash.com/sticker/3841/Natus-Vincere-2020-RMR',
         'https://csgostash.com/sticker/3812/TYLOO-2020-RMR',
         'https://csgostash.com/sticker/3869/Astralis-2020-RMR',
         'https://csgostash.com/sticker/3837/Vitality-2020-RMR',
         'https://csgostash.com/sticker/3875/Nemiga-2020-RMR',
         'https://csgostash.com/sticker/3805/FaZe-2020-RMR',
         'https://csgostash.com/sticker/3876/Liquid-2020-RMR',
         'https://csgostash.com/sticker/3872/G2-2020-RMR',
         'https://csgostash.com/sticker/3807/Virtuspro-2020-RMR',
         'https://csgostash.com/sticker/3840/Spirit-2020-RMR',
         'https://csgostash.com/sticker/3874/GODSENT-2020-RMR',
         'https://csgostash.com/sticker/3806/North-2020-RMR',
         'https://csgostash.com/sticker/3844/FURIA-2020-RMR',
         'https://csgostash.com/sticker/3873/OG-2020-RMR',
         'https://csgostash.com/sticker/3839/Ninjas-in-Pyjamas-2020-RMR',
         'https://csgostash.com/sticker/3870/BIG-2020-RMR',
         'https://csgostash.com/sticker/3811/Renegades-2020-RMR',
         'https://csgostash.com/sticker/3810/Boom-2020-RMR',
         'https://csgostash.com/sticker/3838/Heroic-2020-RMR',
         'https://csgostash.com/sticker/3809/GenG-2020-RMR',
         'https://csgostash.com/sticker/3808/ESPADA-2020-RMR',
         'https://csgostash.com/sticker/3843/100-Thieves-2020-RMR',
         'https://csgostash.com/sticker/3842/Evil-Geniuses-2020-RMR',
         'https://csgostash.com/sticker/3871/Fnatic-2020-RMR',
         'https://csgostash.com/stickers/capsule/313/2020-RMR-Contenders',
         'https://csgostash.com/stickers/capsule/312/2020-RMR-Challengers',
         'https://csgostash.com/stickers/capsule/311/2020-RMR-Legends']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

s = requests.Session()

prices = []
for link in links:
    r = s.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('span', {'class': 'pull-right'}).text.replace('€',"")
    price = price.replace('-','0')
    price = float(price.replace(',','.'))
    prices.append(price)

values = []
for i in range(len(prices)):
    values.append(prices[i] * amounts[i])

total = round(sum(values),2)

time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

with open('last_prices.txt', 'r') as file:
    for line in file:
        last_line = line
    last_prices = last_line.replace('\n','').split(',')[1:]
    last_prices = list(map(lambda x: float(x), last_prices))

diff = []
for i in range(len(prices)):
    diff.append(((prices[i]-last_prices[i])/last_prices[i])*100)


with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(addr_from, password)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'The total value of my Steam Inventory - {total}'
    msg['From'] = addr_from
    msg['To'] = addr_to

    text = "".join(list(((f'{names[i]} | {amounts[i]} * {prices[i]:.2f}€ = {values[i]:.2f} | {diff[i]:.1f}% diff')
                         for i in range(len(names))))) + "\nRazem: {total:.2f}€"

    table_header = '<tr>' \
                   '<th>Nazwa</th>' \
                   '<th>Ilość</th>' \
                   '<th>Cena</th>' \
                   '<th>Suma</th>' \
                   '<th>Różnica</th>' \
                   '</tr>'

    table_body = "".join(list(((f'<tr>'
                                f'<td>{names[i]}</td>'
                                f'<td>{amounts[i]}</td>'
                                f'<td>{prices[i]:.2f}€</td>'
                                f'<td>{values[i]:.2f}€</td><td>{diff[i]:.1f}%</td>'
                                f'</tr>')
                         for i in range(len(names))))) + f"<tr>" \
                                                         f"<td>RAZEM</td>" \
                                                         f"<td>{sum(amounts)}</td>" \
                                                         f"<td>-------</td>" \
                                                         f"<td>{total:.2f}</td>" \
                                                         f"<td>{diff[-1]:.1f}%</td>" \
                                                         f"</tr>"

    table_style = "table, th, td {border: 1px solid black; padding: 2px;}"
    html = f"""\
    <html>
      <head>
        <style>{table_style}</style>
      </head>
      <body>
          <table>
               {table_header}{table_body}
          </table>
      </body>
    </html>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    smtp.sendmail(addr_from, addr_to, msg.as_string())

new_line = time + "," + ",".join(str(price) for price in prices) + f",{total:.2f}" + "\n"

with open('last_prices.txt', 'a') as file:
    file.write(new_line)