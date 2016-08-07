from scraper.field_definitions import Fields
from scraper.website.website_interface import WebsiteInterface
from scraper.utils import *
from time import sleep
import json
from tqdm import tqdm

from scraper.erudite_schema import LearningResource
from statsmodels.regression.tests.test_quantile_regression import idx
from idlelib.idle_test.test_helpabout import About
from sympy.tensor.indexed import Idx

class Coursera(WebsiteInterface):

    def __init__(self):
        self.name = 'CourseraScraper'

    def can_handle(self, url):
        if url == 'https://www.coursera.org/browse/data-science':
            return True
        else:
            return False

    def scrape(self, url, wait=5):
        print('    Coursera: Scrape specializations from: ' + url)
        specializations = self.get_specializations(url, wait)
        data = list()
        for l in tqdm(specializations):
            print('\n    Coursera: Scrape ' + l)
            data.extend(self.get_specializations_info(l, wait))
            print('    Coursera: ' + str(len(data)) + ' courses loaded')
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
                    
                    #sleep(wait)
                    print('    Coursera: Scrape ' + url + ", clicking button " + str(current_idx))
           
                    wait_until_session_stable(sess)
                    
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

        wait = wait_until_session_stable(sess)
        #sleep(wait)

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
            
            """lr = LearningResource()
            lr.id = idx
            lr.title = titles
            lr.description = About
            lr.syllabus = syllabus"""
          
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
