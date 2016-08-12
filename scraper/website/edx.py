from __future__ import print_function
from scraper.erudite_schema import *
from scraper.website.website_interface import WebsiteInterface
from scraper.utils import *
from time import sleep
from tqdm import tqdm
import traceback
from scraper.erudite_schema import LearningResource


class EDX(WebsiteInterface):

    def __init__(self):
        WebsiteInterface.__init__(self)
        self.name = 'edX'
        self.base_url = 'https://www.edx.org'
        self.instructors = dict()
        self.providers = dict()

    def can_handle(self, url):
        if url.startswith('https://www.edx.org'):
            return True
        else:
            return False

    def scrape(self, url, verbose=0):
        url = url.strip('/')
        if url == 'https://www.edx.org/course' or url == 'https://www.edx.org' or url.startswith('https://www.edx.org/course/subject/'):
            return self.scrape_overview(url)
        elif url.startswith('https://www.edx.org/bio/'):
            return [self.scrape_bio(url)]
        elif url.startswith('https://www.edx.org/course/'):
            return [self.get_course_info(url, verbose=verbose)]
        elif url.startswith('https://www.edx.org/xseries/'):
            return [self.get_series_info(url, verbose=verbose)]
        else:
            print(self.name, ": Don't know how to handle", url)

    def scrape_overview(self, url):
        course_links = self.harvest_course_links(url)
        data = set()
        print('EDX: Scrape info of xseries...')
        for l in tqdm(list(filter(lambda x: 'www.edx.org/xseries/' in x, course_links))):
            try:
                xs = self.get_series_info(l)

                # get courses of series to crawl them in the next step
                for cl in xs.courses:
                    if cl not in course_links:
                        print('add course from xseries:', cl, '\n')
                    course_links.add(cl)
                data.add(xs)
            except KeyboardInterrupt:
                break
            except:
                print('xseries failed:', l)
                print(traceback.format_exc())
            # break

        print('EDX: Scrape info of courses...')
        for l in tqdm(list(filter(lambda x: 'www.edx.org/course/' in x, course_links))):
            try:
                c = self.get_course_info(l)
                data.add(c)
            except KeyboardInterrupt:
                break
            except:
                print('course failed:', l)
                print(traceback.format_exc())
            # break
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
            try:
                c_link = card.find('a', attrs={'class': 'course-link'})['href']
                links.add(self.base_url + c_link)
            except (AttributeError, TypeError):
                pass
        print('harvested', len(links), 'links!')
        return links

    def get_course_info(self, url, verbose=0):
        soup = self.get_expanded_soup(url)

        course = LearningResource()
        course.id = url
        course.url = url
        course.slug = url.rsplit('/', 1)[-1]
        course.title = save_get_text(soup.find('h1', attrs={'class': 'course-intro-heading'}))
        course.subtitle = save_get_text(soup.find('p', attrs={'class': 'course-intro-lead-in'}))
        course.rating = save_get_text(soup.find('span', attrs={'class': 'ct-widget-stars__rating-stat'}))
        try:
            course.description = save_get_text(soup.find('div', attrs={'class': 'course-description'}).find('div'))
        except AttributeError:
            pass
        course.objectives = save_get_text(soup.find('div', attrs={'class': 'course-info-list wysiwyg-content'}))
        course.syllabus = save_get_text(soup.find('div', attrs={'class': 'syllabus-content'}))
        try:
            course.prerequisite = save_get_text(soup.find('h2', attrs={'class': 'course-info-heading reg'}).parent).split(
                'Prerequisites', 1)[-1].strip().strip(':').strip()
            if course.prerequisite.lower().strip().strip('.') == 'none':
                course.prerequisite = ''
        except AttributeError:
            pass
        try:
            course.available = self.field_cleanup(save_get_text(soup.find('div', attrs={'class': 'course-start'}).parent), 'Enroll Now', pos=0)
        except AttributeError:
            pass
        # details
        self.add_details_panel(course, soup)

        instructors = self.get_instructors(soup, course, verbose=verbose)
        course.instructors.update(instructors)
        if verbose:
            course.print_info()
        return course

    def add_details_panel(self, course, soup):
        course.language = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'language'})),
                                             ['Languages', 'Language'])
        course.length = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'length'})), 'Length')
        course.typical_learning_time = self.field_cleanup(
            save_get_text(soup.find('li', attrs={'data-field': 'effort'})), 'Effort')
        course.difficulty = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'level'})), 'Level')
        provider = Provider()
        provider.id = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'school'})), 'Institution')
        try:
            provider = self.providers[provider]
        except KeyError:
            try:
                provider_url = self.base_url + soup.find('li', attrs={'data-field': 'school'}).find('a')['href']
                provider = self.get_provider(provider_url, provider)
                self.providers[provider] = provider
            except (AttributeError, TypeError):
                pass

        course.provider = provider
        course.price = self.field_cleanup(save_get_text(soup.find('li', attrs={'data-field': 'price'})), 'Price')

    def get_provider(self, url, provider=None):
        soup = self.get_expanded_soup(url)
        if provider is None:
            provider = Provider()
        page_title = soup.find('h1', attrs={'id': 'page-title'})
        try:
            subtitle = save_get_text(page_title.find('span', attrs={'class': 'subtitle'}))
            page_title = save_get_text(page_title).replace(subtitle, '').strip()
        except AttributeError:
            page_title = save_get_text(page_title)
        provider.id = page_title
        provider.name = page_title
        provider.description = save_get_text(soup.find('div', attrs={'id': 'block-system-main', 'class': 'block'}))
        provider.url = url
        return provider

    @staticmethod
    def get_expanded_soup(url):
        sess = get_js_session(url)
        click_buttons(sess, "//span[contains(@class, 'see-more-label')]")
        click_buttons(sess, "//span[contains(@class, 'show-content-cta')]")
        wait_until_session_stable(sess)
        soup = BeautifulSoup(sess.body(), "lxml")
        return soup

    def get_series_info(self, url, verbose=0):
        soup = self.get_expanded_soup(url)

        course = LearningResource()
        course.id = url
        course.url = url
        course.slug = url.rsplit('/', 1)[-1]
        course.title = save_get_text(soup.find('div', attrs={'class': 'org-label'}).find_next('h1'))
        course.subtitle = save_get_text(soup.find('p', attrs={'class': 'banner-description'}))
        overview_div = soup.find('div', attrs={'class': 'overview'})
        try:
            course.description = '\n'.join(filter(lambda x: x != '', [save_get_text(p) for p in
                                                                      overview_div.find('div', attrs={
                                                                          'class': 'see-more-content'}).findAll('p')]))
        except AttributeError:
            pass
        try:
            course.objectives = '\n'.join(filter(lambda x: x != '', [save_get_text(li) for li in
                                                                     overview_div.find_next_sibling('div').findAll(
                                                                         'li')]))
        except AttributeError:
            pass

        # details
        self.add_details_panel(course, soup)

        try:
            for card in soup.find('section', attrs={'id': 'courses'}).findAll('div', attrs={'class': 'discovery-card'}):
                try:
                    card_url = self.base_url + card.find('a')['href']
                    course.courses.append(card_url)
                except (AttributeError, TypeError):
                    pass
        except AttributeError:
            pass
        if verbose:
            course.print_info()
        return course

    @staticmethod
    def field_cleanup(text, split_name, pos=-1):
        if isinstance(split_name, str):
            split_name = [split_name]
        for s in split_name:
            text = text.strip().split(s)[pos].strip(':').strip().strip('\n')
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        return text

    def get_instructors(self, soup, course, verbose=0):
        instructors = set()
        for i in soup.findAll('li', attrs={'class': 'list-instructor__item'}):
            instructor = Instructor()
            try:
                name = i.find('p', attrs={'class': 'instructor-name'})
            except AttributeError:
                continue
            try:
                bio_url = self.base_url + name.parent['href']
            except (AttributeError, TypeError):
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

            if course not in instructor.teaches:
                instructor.teaches.add(course)
                updates = True

            if bio_url != '':
                bio = Bio()
                bio.url = bio_url
                bio.id = bio.url
                if bio not in instructor.biography:
                    bio.instructor_id = instructor.id
                    bio.bio, bio_soup = self.get_bio(bio_url, return_soup=True)
                    if bio:
                        instructor.biography.add(bio)
                        # print('add bio to instructor', instructor.id, bio_url)
                        if verbose:
                            print('-' * 80)
                            print('new bio for instructor')
                            print(bio.print_info())
                            print('-' * 80)
                        updates = True

                    try:
                        bio_jobtitle = save_get_text(bio_soup.find('ul', attrs={'class': 'org-roles'}).find('li'))
                        instructor.job_title = max([bio_jobtitle, instructor.job_title], key=len)
                        updates = True
                    except AttributeError:
                        pass
                    try:
                        bio_worksfor = bio_soup.find('li', attrs={'class': 'org-name'})
                        try:
                            worksfor_link = bio_worksfor.find('a')['href']
                            if worksfor_link != '':
                                provider = self.get_provider(worksfor_link)
                                try:
                                    provider = self.providers[provider]
                                except KeyError:
                                    self.providers[provider] = provider
                                instructor.works_for.add(provider)
                                updates = True
                        except (AttributeError, TypeError):
                            worksfor_link = ''
                        if worksfor_link == '':
                            instructor.works_for.add(save_get_text(bio_worksfor))
                            updates = True
                    except AttributeError:
                        pass

            if instructor.job_title == '' or len(instructor.works_for) == 0:
                position = i.find('p', attrs={'class': 'instructor-position'})
                try:
                    org = save_get_text(position.find('span', attrs={'class': 'instructor-org'})).strip()
                except AttributeError:
                    org = ''
                position = save_get_text(position).replace(org, '').strip()
                if instructor.job_title == '':
                    instructor.job_title = position
                    updates = True
                if org != '' and len(instructor.works_for) == 0:
                    instructor.works_for.add(org)
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

    @staticmethod
    def get_bio(url, verbose=0, return_soup=False):
        soup = get_soup(url, js=True, verbose=verbose)
        bio = ''
        try:
            bio_part = soup.find('p', attrs={'class': 'resume-copy'})
            while True:
                bio += ('\n' + save_get_text(bio_part))
                bio_part = bio_part.find_next_sibling('p')
        except AttributeError:
            pass
        bio = bio.strip('\n')
        if return_soup:
            return bio, soup
        else:
            return bio

    def scrape_bio(self, url, verbose=0):
        b = Bio()
        b.url = url
        b.id = url
        b.bio = self.get_bio(url, verbose=verbose)
        return b

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
