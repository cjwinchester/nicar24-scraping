import time
import csv

import requests
from bs4 import BeautifulSoup


url = 'https://www.justice.gov/crt/civil-rights-division-press-releases-speeches'

r = requests.get(url)

r.raise_for_status()

soup = BeautifulSoup(r.text, 'html.parser')

last_tag = soup.find('a', {'aria-label': 'Last page'})
last_page_number = int(last_tag['href'].split('=')[-1])

data = []

for page_number in range(last_page_number+1):
    params = {
        'page': page_number
    }

    r = requests.get(
        url,
        params=params
    )

    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'html.parser')

    items = soup.find_all(
        'article',
        {'class': 'news-content-listing'}
    )

    for item in items:
        item_type = ' '.join(
            item.find(
                'div',
                {'class': 'node-type'}
            ).text.split()
        )

        headline = ' '.join(
            item.find('h2').text.split()
        )

        link = item.find('a').get('href')
        if link:
            detail_url = f'https://www.justice.gov{link}'
        else:
            link = ''

        date = item.find('time').get('datetime').split('T')[0]

        data.append({
            'type': item_type,
            'headline': headline,
            'url': detail_url,
            'date': date
        })

    print(f'Scraped page {page_number}')

    time.sleep(0.5)


filename = 'doj-civil-rights-speeches-press-releases.csv'

with open(filename, 'w') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=list(data[0].keys()))
    writer.writeheader()
    writer.writerows(data)
    print(f'Wrote {filename}')


'''
Idea to extend this scraper: Download the detail pages themselves into a directory and scrape the contents, as well
'''
