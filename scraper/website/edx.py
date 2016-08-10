from __future__ import print_function
from scraper.erudite_schema import *
from scraper.website.website_interface import WebsiteInterface
from scraper.utils import *
from time import sleep
import json
from tqdm import tqdm
import traceback
from collections import defaultdict

from scraper.erudite_schema import LearningResource
from statsmodels.regression.tests.test_quantile_regression import idx
from idlelib.idle_test.test_helpabout import About


class EDX(WebsiteInterface):

    def __init__(self):
        self.name = 'EDXScraper'
        self.base_url = 'https://www.edx.org'
        self.instructors = dict()

    def can_handle(self, url):
        if url.startswith('https://www.edx.org/course/'):
            return True
        else:
            return False

    def scrape(self, url, wait=5):
        course_links = self.harvest_course_links(url)
        data = set()
        print('EDX: Scrape course info of xseries...')
        for l in tqdm(list(filter(lambda x: x.startswith('https://www.edx.org/xseries/', course_links)))):
            try:
                xs = self.get_series_info(l)

                # get courses of series to crawl them in the next step
                for cl in xs.courses:
                    course_links.add(cl)
                data.add(xs)
            except KeyboardInterrupt:
                break
            except:
                print('xseries failed:', l)
                print(traceback.format_exc())

        print('EDX: Scrape course info of courses...')
        for l in tqdm(list(filter(lambda x: not x.startswith('https://www.edx.org/xseries/', course_links)))):
            try:
                c = self.get_course_info(l)
                data.add(c)
            except KeyboardInterrupt:
                break
            except:
                print('course failed:', l)
                print(traceback.format_exc())
        return data

    """
    Scroll to the bottom of the page and grab all the course links. 
    """
    def harvest_course_links(self, url):
        sess = get_js_session(url)
        
        self.infinite_scroll_to_bottom(sess, timeout=120)
        soup = BeautifulSoup(sess.body(), "lxml")
        links = set()
        for card in soup.findAll('div', attrs={'class': 'course-card'}):
            c_link = card.find('a', attrs={'class': 'course-link'})['href']
            links.add(self.base_url + c_link)
        print('harvested', len(links), 'links!')
        return links

    def get_course_info(self, url, verbose=0):
        sess = get_js_session(url)
        click_buttons(sess, "//span[contains(@class, 'see-more-label')]")
        click_buttons(sess, "//span[contains(@class, 'show-content-cta')]")
        wait_until_session_stable(sess)
        soup = BeautifulSoup(sess.body(), "lxml")

        course = LearningResource()
        course.id = url
        course.url = url
        course.title = save_get_text(soup.find('h1', attrs={'class': 'course-intro-heading'}))
        course.subtitle = save_get_text(soup.find('p', attrs={'class': 'course-intro-lead-in'}))
        course.rating = save_get_text(soup.find('span', attrs={'class': 'ct-widget-stars__rating-stat'}))
        course.description = save_get_text(soup.find('div', attrs={'class': 'course-description'}).find('div'))
        course.objectives = save_get_text(soup.find('div', attrs={'class': 'course-info-list wysiwyg-content'}))
        course.syllabus = save_get_text(soup.find('div', attrs={'class': 'syllabus-content'}))
        course.prerequisite = save_get_text(soup.find('h2', attrs={'class': 'course-info-heading reg'}).parent).split(
            'Prerequisites', 1)[-1].strip().strip(':').strip()
        course.available = self.field_cleanup(save_get_text(soup.find('div', attrs={'class': 'course-start'}).parent), 'Enroll Now', pos=0)
        # details

        course.language = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'language'})), 'Languages')
        course.length = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'length'})), 'Length')
        course.typical_learning_time = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'effort'})), 'Effort')
        course.education_level = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'level'})), 'Level')
        course.venue = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'school'})), 'Institution')
        course.price = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'price'})), 'Price')
        instructors = self.get_instructors(soup, course, verbose=verbose)
        course.is_teacher.update(instructors)
        if verbose:
            course.print_info()
        return course

    def get_series_info(self, url, verbose=0):
        sess = get_js_session(url)
        click_buttons(sess, "//span[contains(@class, 'see-more-label')]")
        click_buttons(sess, "//span[contains(@class, 'show-content-cta')]")
        wait_until_session_stable(sess)
        soup = BeautifulSoup(sess.body(), "lxml")

        course = LearningResource()
        course.id = url
        course.url = url
        course.title = save_get_text(soup.find('div', attrs={'class': 'org-label'}).find_next('h1'))
        course.subtitle = save_get_text(soup.find('p', attrs={'class': 'banner-description'}))
        overview_div = soup.find('div', attrs={'class': 'overview'})
        course.description = '\n'.join([save_get_text(p) for p in
                                        overview_div.find('div', attrs={
                                            'class': 'see-more-content'}).findAll('p')])

        course.objectives = '\n'.join([save_get_text(li) for li in overview_div.find_next_sibling('div').findAll('li')])

        # course.rating = save_get_text(soup.find('span', attrs={'class': 'ct-widget-stars__rating-stat'}))


        # course.syllabus = save_get_text(soup.find('div', attrs={'class': 'syllabus-content'}))
        course.prerequisite = save_get_text(soup.find('h2', attrs={'class': 'course-info-heading reg'}).parent).split(
            'Prerequisites', 1)[-1].strip().strip(':').strip()
        # course.available = self.field_cleanup(save_get_text(soup.find('div', attrs={'class': 'course-start'}).parent), 'Enroll Now', pos=0)

        # details
        course.language = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'language'})), 'Languages')
        course.length = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'length'})), 'Length')
        course.typical_learning_time = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'effort'})), 'Effort')
        course.education_level = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'level'})), 'Level')
        course.venue = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'school'})), 'Institution')
        course.price = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'price'})), 'Price')
        # instructors = self.get_instructors(soup, course, verbose=verbose)
        # course.is_teacher.update(instructors)
        for card in soup.find('section', attrs={'class': 'courses'}).findAll('div', attrs={'class': 'discovery-card'}):
            card_url = self.base_url + card.find('a')['href']
            course.courses.append(card_url)
        if verbose:
            course.print_info()
        return course

    @staticmethod
    def field_cleanup(text, split_name, pos=-1):
        return text.strip().split(split_name)[pos].strip(':').strip()

    def get_instructors(self, soup, course, verbose=0):
        instructors = set()
        for i in soup.findAll('li', attrs={'class': 'list-instructor__item'}):
            instructor = Instructor()
            name = i.find('p', attrs={'class': 'instructor-name'})
            try:
                bio_url = self.base_url + name.parent['href']
            except AttributeError:
                bio_url = ''
            name = save_get_text(name).strip()
            instructor.full_name = name
            name = name.replace('Dr.', '').strip()
            split_name = name.split()
            if len(split_name) == 3:
                instructor.first_name = split_name[0]
                instructor.middle_name = split_name[1]
                instructor.last_name = split_name[-1]
            elif len(split_name) == 2:
                instructor.first_name = split_name[0]
                instructor.last_name = split_name[1]
            else:
                instructor.last_name = name
            instructor.id = instructor.full_name

            updates = False
            if instructor in self.instructors:
                instructor = self.instructors[instructor]
            else:
                updates = True

            if instructor.job_title == '' or instructor.works_for == '':
                position = i.find('p', attrs={'class': 'instructor-position'})
                try:
                    org = save_get_text(position.find('span', attrs={'class': 'instructor-org'})).strip()
                except AttributeError:
                    org = ''
                position = save_get_text(position).replace(org, '').strip()
                instructor.job_title = position
                instructor.works_for = org
                updates = True

            if course not in instructor.teaches:
                instructor.teaches.add(course)
                updates = True

            if bio_url != '':
                bio = Bio()
                bio.url = bio_url
                if bio not in instructor.has_bio:
                    bio.bio_owner = instructor
                    #TODO: crawl bio
                    instructor.has_bio.add(bio)
                    if verbose:
                        print('-' * 80)
                        print('new bio for instructor')
                        print(bio.print_info())
                        print('-' * 80)
                    updates = True

            if updates:
                self.instructors[instructor] = instructor
                if verbose:
                    print('-' * 80)
                    print('new instructor')
                    instructor.print_info()
                    print('-' * 80)
            instructors.add(instructor)
        return instructors


    """
    Continuously scroll to the bottom of the page for a full minute,
    let the page reload and load the data from there.
    """
    @staticmethod
    def infinite_scroll_to_bottom(sess, timeout=120, verbose=0, render=''):
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
                         if (a.length >= 4) { \
                             a = a[a.length - 4]; \
                             window.scroll(0, findPos(a)); \
                         } else {  \
                             a = a[a.length - 1]; \
                             window.scroll(0, findPos(a)-300); \
                         } \
                        '
        c = 0
        v_print(verbose, 'scrolling', end='')
        while datetime.datetime.now() <= end and c < 10:

            sess.exec_script(scroll_script)
            sleep(1)
            this_size = len(sess.body())

            if this_size <= last_size:
                c += 1
                v_print(verbose, '.', end='')
            else:
                last_size = max(last_size, this_size)
                c = 0
                v_print(verbose, '+', end='')
        total_time = datetime.datetime.now() - start
        v_print(verbose, total_time)
        wait_until_session_stable(sess, verbose=verbose)
        render_js_sess(sess, render)
