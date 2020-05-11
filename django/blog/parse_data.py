import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent

from .models import Category, Post

ua = UserAgent()


class ParseIguides:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': ua.chrome}

    def get_page(self, url_link):
        resp = self.session.get(url_link)
        return resp.content

    def get_links(self):
        txt_content = self.get_page('https://www.iguides.ru/')
        soup = BeautifulSoup(txt_content, 'lxml')

        links = soup.select('h2.name a')

        return ['https://www.iguides.ru' + link.get('href') for link in links]

    def get_detail_info(self):
        
        final_result = []
        for url_post in self.get_links():
            content = self.get_page(url_post)
            soup = BeautifulSoup(content, 'lxml')

            try:
                title = soup.find('h1', attrs={'itemprop': 'name'}).text.strip()
                category = soup.select_one('ul.newsTapes li.-active').text.strip()
                tags = [i.text for i in soup.find('div', class_='label').find_all('a', attrs={'itemprop': 'about'})]
                image = soup.find('div', class_='article-detail').find('img', attrs={'itemprop': 'image'})['src']

                if image.startswith('https://www.iguides.ru'):
                    image = image
                elif image.startswith('https://'):
                    image = image
                else:
                    image = 'https://www.iguides.ru' + image
                created = soup.find('time', attrs={'itemprop': 'datePublished'}).text.strip()
                content = soup.find('div', class_='article-detail').get_text()
                
                # print(title)
                # print(category)
                # print(tags)
                # print(image)
                # print(created)
                # print(content)
                # print('---------------------------------------------------')
                final_result.append({
                    'title': title,
                    'category': category,
                    'tags': tags,
                    'image': image,
                    'content': content
                    
                    })
                
                # time.sleep(1)
                # break

            except Exception as err:
                print(err, title)
                pass

            # break
        return final_result

# parse_iguides = ParseIguides()
# # parse_iguides.get_links()
# parse_iguides.get_detail_info()