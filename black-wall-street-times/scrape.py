import time
import csv

import requests
from bs4 import BeautifulSoup


url_base = 'https://theblackwallsttimes.com/category/news/'

r = requests.get(url_base)

r.raise_for_status()

soup = BeautifulSoup(r.text, 'html.parser')

pagination = soup.find_all('a', {'class': 'page-numbers'})

last_page = int(pagination[-2].text)

data = []

for page_number in range(1, last_page):

    url = f'{url_base}page/{page_number}'

    r = requests.get(url)

    r.raise_for_status()

    articles = soup.find_all('article', {'class': 'post'})

    for article in articles:
        img = article.find('img')

        if img:
            img = img.get('src')

        headline = ' '.join(
            article.find('h2').text.split()
        )

        url = article.find('a').get('href')

        byline = article.find('span', {'class': 'author'})
        author = byline.text
        author_link = byline.find('a').get('href')

        date = article.find('time').get('datetime').split('T')[0]

        data.append({
            'headline': headline,
            'date': date,
            'img': img,
            'url': url,
            'author': author,
            'author_link': author_link
        })

    print(f'Scraped page {page_number}')
    time.sleep(0.5)


filename = 'black-wall-street-times-articles.csv'

with open(filename, 'w') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=list(data[0].keys()))

    writer.writeheader()
    writer.writerows(data)

print(f'Wrote {filename}')
