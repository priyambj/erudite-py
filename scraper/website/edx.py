from __future__ import print_function
from scraper.erudite_schema import *
from scraper.website.website_interface import WebsiteInterface
from scraper.utils import *
from time import sleep
import json
from tqdm import tqdm
import traceback

from scraper.erudite_schema import LearningResource
from statsmodels.regression.tests.test_quantile_regression import idx
from idlelib.idle_test.test_helpabout import About


class EDX(WebsiteInterface):

    def __init__(self):
        self.name = 'EDXScraper'
        self.base_url = 'https://www.edx.org'

    def can_handle(self, url):
        if url.startswith('https://www.edx.org/course/'):
            return True
        else:
            return False

    def scrape(self, url, wait=5):
        course_links = self.harvest_course_links(url)
        data = list()
        print('EDX: Scrape course info of specialization...')
        for l in tqdm(course_links):
            if not l.startswith('https://www.edx.org/xseries/'):
                try:
                    data.append(self.get_course_info(l))
                    break
                except:
                    print('failed:', l)
                    print(traceback.format_exc())
        return data

    """
    Scroll to the bottom of the page and grab all the course links. 
    """
    def harvest_course_links(self, url):
        sess = get_js_session(url)
        
        self.infinite_scroll_to_bottom(sess, timeout=120)
        soup = BeautifulSoup(sess.body(), "lxml")
        links = list()
        for card in soup.findAll('div', attrs={'class': 'course-card'}):
            c_link = card.find('a', attrs={'class': 'course-link'})['href']
            links.append(self.base_url + c_link)
        return links

    @staticmethod
    def get_course_info(url):
        sess = get_js_session(url)
        click_buttons(sess, "//span[contains(@class, 'see-more-label')]")
        click_buttons(sess, "//span[contains(@class, 'show-content-cta')]")
        wait_until_session_stable(sess)
        soup = BeautifulSoup(sess.body(), "lxml")

        course = LearningResource()
        course.url = url
        course.title = save_get_text(soup.find('h1', attrs={'class': 'course-intro-heading'}))
        course.subtitle = save_get_text(soup.find('p', attrs={'class': 'course-intro-lead-in'}))
        course.rating = save_get_text(soup.find('span', attrs={'class': 'ct-widget-stars__rating-stat'}))
        course.description = save_get_text(soup.find('div', attrs={'class': 'course-description'}).find('div'))
        course.objectives = save_get_text(soup.find('div', attrs={'class': 'course-info-list wysiwyg-content'}))
        course.syllabus = save_get_text(soup.find('div', attrs={'class': 'syllabus-content'}))
        course.prerequisite = save_get_text(soup.find('h2', attrs={'class': 'course-info-heading reg'}).parent)
        course.available = save_get_text(soup.find('div', attrs={'class': 'course-start'}).parent)
        # details

        course.language = save_get_text(soup.find('li', attrs={'data-field': 'language'}))
        course.length = save_get_text(soup.find('li', attrs={'data-field': 'length'}))
        course.typical_learning_time = save_get_text(soup.find('li', attrs={'data-field': 'effort'}))
        course.education_level = save_get_text(soup.find('li', attrs={'data-field': 'level'}))
        #course.education_level = save_get_text(soup.find('li', attrs={'data-field': 'school'}))
        course.price = save_get_text(soup.find('li', attrs={'data-field': 'price'}))

        course.print_info()
        return course

    def click_buttons(self, sess, xpath):
        for button in sess.xpath(xpath):
            # print('click button')
            try:
                button.click()
            except:
                # print('\tdone')
                break

    """
    Continuously scroll to the bottom of the page for a full minute,
    let the page reload and load the data from there.
    """
    @staticmethod
    def infinite_scroll_to_bottom(sess, timeout=120):
        last_size = len(sess.body())

        start = datetime.datetime.now()
        end = start + datetime.timedelta(seconds=timeout)

        sess.exec_script('function findPos(obj) { \
                                var curtop = 0; \
                                if (obj.offsetParent) { \
                                    do { \
                                        curtop += obj.offsetTop; \
                                    } while (obj = obj.offsetParent); \
                                return [curtop]; \
                                } \
                            }')

        scroll_script = 'var a = document.getElementsByClassName("course-card"); \
                         a = a[a.length - 1]; \
                         window.scroll(0, findPos(a)-300); \
                        '
        c = 0
        print('scrolling', end='')
        while datetime.datetime.now() <= end and c < 5:

            sess.exec_script(scroll_script)
            sleep(2)
            this_size = len(sess.body())

            if this_size <= last_size:
                c += 1
                print('.', end='')
            else:
                last_size = max(last_size, this_size)
                c = 0
                print('+', end='')
        print()
        #total_time = datetime.datetime.now() - start
        #print('took:', total_time)
        wait_until_session_stable(sess)
        # sess.render(str('edex') + ".png")
