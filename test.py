import concurrent.futures
import random
import time
import csv
import requests
import re
from collections import namedtuple
from os import path
from bs4 import BeautifulSoup
from my_logging import get_my_logger

logger = get_my_logger(__name__)

class Get_info(object):
    def __init__(self, url=None, soup=None, timeout=180):
        self.url = url
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')

    def height(self):
         for i in self.soup.select('#coordinate_info > p.model_info > a'):
             get_hight = i.string[:3]
             return get_hight

    def sex(self):
        for i in self.soup.select('#coordinate_info > p.model_info > a'):
            start = re.search(r'MEN|WOMEN', i.string).span()[0]
            end = re.search(r'MEN|WOMEN', i.string).span()[1]
            get_sex = i.string[start:end]
            return get_sex

    def title(self):
        for i in self.soup.select('#coordinate_info > h1'):
            get_title = i.string
        return get_title

    def text(self):
        # import pdb; pdb.set_trace()
        if self.soup.select('#coordinate_info > p.content_txt') == []:
            get_text = ''
        else:
            for i in self.soup.select('#coordinate_info > p.content_txt'):
                get_text = re.sub('<br/>|<p class="content_txt">|</p>','',str(i))

        return get_text

    

    def view(self):
        for i in self.soup.select('#coordinate_img > p.view_num.icon_font'):
            get_view = i.string
        return get_view

    def fav(self):
        for i in self.soup.select('#function_btn > div.container.clearfix > div.btn_save.detailBtn.fn_btn > p > a > span'):
            get_fav = i.string
        return get_fav

    def update_date(self):
        for i in self.soup.select('#coordinate_info > div > p'):
            get_date = i.string
        return get_date

    def ware_item(self):
        get_ware_items = []
        for i in self.soup.select('#item > ul'):
            for x in i.find_all('p',class_='txt'):
                result = x.find('a')
                if result == None:
                    pass
                else:
                    get_ware_items.append(result.string)
        return get_ware_items

    def ware_tag(self):
        get_ware_tags = []
        for i in self.soup.select('#tag > ul'):
            for x in i.find_all('li'):
                get_ware_tags.append(x.find('a').string)
            return get_ware_tags

    def image(self):
        img_html = self.soup.find('img',src=re.compile('^http://cdn.wimg.jp/coordinate'))
        get_image = img_html['src']
        return get_image


def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def scraping(url, timeout=180):
    #リクエストの幅をランダムに選択する
    sleep_time = random.choice(RANDOM_SLEEP_TIMES)

    logger.info('[download start] sleep: {time} '.format(time=sleep_time))
    time.sleep(sleep_time)

    logger.info('scraping start')
    logger.info('url name: {}'.format(url))
    get_information = Get_info(url)

    #scraping
    result_height = get_information.height()
    result_sex = get_information.sex()
    result_title = get_information.title()
    # import pdb; pdb.set_trace()
    result_text = get_information.text()
    result_view = get_information.view()
    result_fav = get_information.fav()
    result_update_date = get_information.update_date()
    result_ware_item = get_information.ware_item()
    result_ware_tag = get_information.ware_tag()
    result_image = get_information.image()
    logger.info('scraping end')

    results =[result_height, result_sex, result_title,
              result_text, result_view, result_fav,
              result_update_date, result_ware_item, result_ware_tag, result_image]
    logger.info('scraping results{}'.format(results))

    return(result_height, result_sex, result_title,
           result_text, result_view, result_fav,
           result_update_date, result_ware_item, result_ware_tag,result_image)

if __name__ == '__main__':

    RANDOM_SLEEP_TIMES = [x * 0.1 for x in range(10,40,5)]  # 0.5秒

    FASHION_INFO = ['http://wear.jp/sinniti/11317790/']

    # with open('urls.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     header = next(reader)
    #     for row in reader:
    #         FASHION_INFO.append(row)

    result_scrapings = []
    for url_list in FASHION_INFO:
        result_scrapings.append(scraping(url_list))

    with open('result_scraping.csv', 'w') as f:
        fieldnames = ['height', 'sex', 'title',
                      'text', 'view', 'fav',
                      'update_date', 'ware_item','ware_tag','result_image']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for results in result_scrapings:
            writer.writerow({'height':results[0], 'sex':results[1], 'title':results[2],
                          'text':results[3], 'view':results[4], 'fav':results[5],
                          'update_date':results[6], 'ware_item':results[7],'ware_tag':results[8],'result_image':results[9]})
