from scraper.field_definitions import Fields
from scraper.website.website_interface import WebsiteInterface
from scraper.utils import *
from time import sleep
import json
from tqdm import tqdm


class Coursera(WebsiteInterface):

    def __init__(self):
        self.name = 'CourseraScraper'

    def can_handle(self, url):
        if url == 'https://www.coursera.org/browse/data-science':
            return True
        else:
            return False

    def scrape(self, url):
        specializations = self.get_specializations(url)
        data = list()
        print('Coursera: Scrape course info of specialization...')
        for l in tqdm(specializations):
            data.extend(self.get_specializations_info(l))
        return data

    def get_specializations(self, url, wait=5):
        sess = get_js_session(url, wait=wait, viewport=(1024, 768))
        spec_pages = list()
        current_idx = 0
        while True:
            for exp_idx, expand_button in enumerate(sess.xpath("//button[contains(@class, 'primary see-all-button')]")):
                if current_idx == exp_idx:
                    # print('click')
                    expand_button.click()
                    sleep(2)
                    spec_pages.append(sess.body())
                    current_idx += 1
                    sess = get_js_session(url, wait=wait, viewport=(1024, 768))
                    break
            else:
                break

        spec_urls = set()
        for sp in spec_pages:
            sp = BeautifulSoup(sp, "lxml")
            js_obj = json.loads(sp.find('script', attrs={'type': 'application/ld+json'}).getText())
            for item in js_obj['itemListElement']:
                url = item['url']
                if url.startswith('https://www.coursera.org/specializations/'):
                    spec_urls.add(url)
        return spec_urls

    def get_specializations_info(self, url, wait=5):
        sess = get_js_session(url, wait=wait, viewport=(1024, 768))

        # expand all syllabus details
        self.click_buttons(sess, "//div[contains(@class, 'course-show-syllabus-text')]")

        sleep(1)
        soup = BeautifulSoup(sess.body(), "lxml")
        courses = soup.find_all('div', attrs={'class': 'rc-SingleCourse'})
        data = list()
        titles = set()
        for idx, c in enumerate(courses):
            title = c.find('div', attrs={'class': 'course-title'}).getText(separator=u' ')
            if title in titles:
                continue
            else:
                titles.add(title)
            # print(title)
            about = c.find('div', attrs={'class': 'course-about'}).getText(separator=u' ')
            try:
                syllabus = c.find('div', attrs={'class': 'rc-Syllabus'}).getText(separator=u' ')
            except:
                syllabus = ''
            c_dict = dict()
            c_dict[Fields.index] = idx
            c_dict[Fields.title] = title
            c_dict[Fields.description] = about
            c_dict[Fields.syllabus] = syllabus
            data.append(c_dict)
        sess.reset()
        return data

    def click_buttons(self, sess, xpath):
        for button in sess.xpath(xpath):
            # print('click button')
            try:
                button.click()
            except:
                # print('\tdone')
                break
