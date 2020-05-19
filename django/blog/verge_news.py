import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import datetime
from selenium import webdriver

ua = UserAgent()

class VergeParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': ua.chrome}

    def get_page(self, url):
        r = self.session.get(url)
        return r.content

    def get_links(self):
        content = self.get_page('https://www.theverge.com/')
        soup = BeautifulSoup(content, 'lxml')
        links = soup.find_all('div', class_='c-entry-box--compact__body')
        all_links = []
        for link in links:
            # if link.a['href'] == 'https://www.voxmedia.com/careers':
            if link.a['href'].startswith('https://www.voxmedia.com'):
                continue
            lnk = link.a['href']
            all_links.append(lnk)
        # print(all_links)
        return all_links[:3]

    def get_detail_info(self):
        final_result = []
        links = self.get_links()
        for link in links:
            if link.startswith('https://www.vox.com/'):
                continue

            try:
                soup = BeautifulSoup(self.get_page(link), 'lxml')
                title = soup.find('h1', class_='c-page-title').text
                # tags = []

                tags = [tag.a.span.text for tag in soup.find_all('li', class_='c-entry-group-labels__item') if tag]
                # print(tags)
                category = tags[0]
                # print(category)
                image = soup.find('picture', class_='c-picture').find('img')['src']
                # print(image)

                content = soup.find('div', class_='c-entry-content')
                # print(title)
                # print('===============================================================')
                cntnt = []
                for c in content.find_all(['p', 'figure']):
                    text_content = c.text
                    cntnt.append(text_content)
                    try:
                        image_content = c.find('span', class_='e-image__image')['data-original']
                        cntnt.append(image_content)
                        # print(image_content)
                    except Exception as err:
                        # print(err)
                        pass

                content = '\n\n'.join([i.strip() for i in cntnt])
                ############################   SELENIUM  #############################################################################
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                browser = webdriver.Chrome(options=options, executable_path="C:/Program Files/Python38/chromedriver.exe")
                # browser = webdriver.Chrome(executable_path="C:/Program Files/Python38/chromedriver.exe")

                browser.get('https://translate.google.com.ua/?hl=ru#view=home&op=translate&sl=en&tl=ru')
                time.sleep(2)
                browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_css_selector("textarea.tlid-source-text-input"), f"{title}")
                time.sleep(2)
                translated_title = browser.find_element_by_xpath("//span[@class='tlid-translation translation']").text
                # print(translated_title)
                # print('-------------------------------------------------------------------')
                time.sleep(2)
                browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_css_selector("textarea.tlid-source-text-input"), f"{content}")
                time.sleep(2)
                translated_text = browser.find_element_by_xpath("//span[@class='tlid-translation translation']").text
                ###########################   END SELENIUM  #############################################################################
                time.sleep(2)
                # print(translated_text)
                # print('-------------------------------------------------------------------')
                final_result.append({
                    'title': translated_title,
                    'category': category,
                    'tags': tags,
                    'image': image,
                    'content': translated_text
                    })
                browser.quit()
                
            except Exception as err:
                # print(err)
                pass
        return final_result
            ############################   SELENIUM  #############################################################################
            # options = webdriver.ChromeOptions()
            # # options.add_argument('headless')
            # # browser = webdriver.Chrome(options=options, executable_path="C:/Program Files/Python38/chromedriver.exe")
            # browser = webdriver.Chrome(executable_path="C:/Program Files/Python38/chromedriver.exe")

            # browser.get('https://translate.google.com.ua/?hl=ru#view=home&op=translate&sl=en&tl=ru')
            # time.sleep(2)
            # browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_css_selector("textarea.tlid-source-text-input"), f"{title}\n{content}")
            # time.sleep(3)
            # translated_text = browser.find_element_by_xpath("//span[@class='tlid-translation translation']").text
            ############################   END SELENIUM  #############################################################################
            # time.sleep(3)
            # print(translated_text)
            # browser.quit()
            

# new_win = VergeParser()
# new_win.get_links()
# new_win.get_detail_info()