import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import datetime
from selenium import webdriver

ua = UserAgent()

class NeoWinParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': ua.chrome}

    def get_page(self, url):
        r = self.session.get(url)
        return r.content

    def get_links(self):
        content = self.get_page('https://www.neowin.net/')
        soup = BeautifulSoup(content, 'lxml')
        links = soup.find('div', class_='news-list').find_all('h3', class_='news-item-title')
        links_list = []
        for link in links:
            lnk = 'https://www.neowin.net' + link.a['href']
            links_list.append(lnk)
        # print(links_list[:3])
        return links_list#[:5]

    def get_detail_info(self):
        links = self.get_links()
        final_result = []
        for link in links:
            soup = BeautifulSoup(self.get_page(link), 'lxml')
            title = soup.find('h1', class_='article-title').a.text.strip()
            published = soup.find('time', class_='date published').text.strip()

            image_block = soup.find('div', class_='article-content')
            image = None
            try:
                image = image_block.find('figure', class_='image--expandable').a['href']
            except:
                pass
                
            try:
                image = image_block.find('p').find('img')['src']
            except:
                pass
                
            try:
                category = soup.find('ul', class_='nav-secondary-menu').find('li', class_='active-menu').a.text
            except:
                category = 'Other'

            tags = soup.find('div', class_='article-tags').find('ul').find_all('li')
            all_tags = []
            for tag in tags:
                all_tags.append(tag.a.text)

            content = soup.find('div', class_='article-content')

            print(title)
            print(image)
            print(category)
            print(all_tags)
            print(published)
            print('-----------------------------------------------------------------')
            # time.sleep(1)
            # break

            content_body = []
            for i in content.find_all('p'):
                content_body.append(i.text)
                try:
                    content_body.append(i.img['src'])
                except:
                    pass
            content = '\n\n'.join(content_body)

            ###########################        SELENIUM        ################################################
            # options = webdriver.ChromeOptions()
            # options.add_argument('headless')
            # browser = webdriver.Chrome(options=options, executable_path="C:/Program Files/Python38/chromedriver.exe")
            # # browser = webdriver.Chrome(executable_path="C:/Program Files/Python38/chromedriver.exe")

            # browser.get('https://translate.google.com.ua/?hl=ru#view=home&op=translate&sl=en&tl=ru')
            # time.sleep(2)
            # browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_css_selector("textarea.tlid-source-text-input"), f"{title}")
            # # browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_css_selector("textarea.tlid-source-text-input"), f"{title}")
            # time.sleep(1)
            # translated_title = browser.find_element_by_xpath("//span[@class='tlid-translation translation']").text

            # # time.sleep(3)
            # # print('TITLE ----> ', translated_title)
            # browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_css_selector("textarea.tlid-source-text-input"), f"{content}")
            # # browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_css_selector("textarea.tlid-source-text-input"), f"{title}")
            # time.sleep(2)
            # translated_content = browser.find_element_by_xpath("//span[@class='tlid-translation translation']").text
            # # print('CONTENT ----> ', translated_content)
            # # print('----------------------------------------------------------------------------------------------')
            # final_result.append({
            #     'title': translated_title,
            #     'category': category,
            #     'tags': all_tags,
            #     'image': image,
            #     'content': translated_content

            # })
            # browser.quit()
            ###########################     END SELENIUM       ################################################
            # final_result.append({
            #         'title': translated_title,
            #         'category': category,
            #         'tags': all_tags,
            #         'image': image,
            #         'content': translated_content
            #
            #         })
            # break
        return final_result



new_win = NeoWinParser()
new_win.get_detail_info()