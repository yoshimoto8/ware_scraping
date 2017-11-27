import requests
import time
import csv
from bs4 import BeautifulSoup

def gets(response,i):
    i += 1
    print('{} 回目のスクリピングを実行します。'.format(str(i)))

    start_url = 'http://wear.jp'
    time.sleep(3)
    html = requests.get(response)
    soup = BeautifulSoup(html.text, 'lxml')

    #get url
    for li in soup.find_all("li", class_="like_mark"):
        url = start_url + li.a.get("href")
        get_urls.append(url)

    #next_page
    next_h = soup.select('#pager > p.next > a')
    for next_url in next_h:
        response = start_url + next_url.get('href')
        gets(response, i)

if __name__ == '__main__':
    get_urls = []
    start_url = 'http://wear.jp/men-coordinate/'
    i = 0
    get = gets(start_url, i)

    with open('urls.csv', 'w') as f:
        fieldnames = ['url']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for url in get_urls:
            writer.writerow({'url': url})
