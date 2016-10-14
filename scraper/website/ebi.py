from __future__ import print_function

from time import sleep
from tqdm import tqdm
import traceback

from scraper.erudite_schema import *
from scraper.erudite_schema import LearningResource
from scraper.utils import *
from scraper.website.website_interface import WebsiteInterface

class EBI (WebsiteInterface):
    def __init__(self):
        WebsiteInterface.__init__(self)
        self.name = 'EBI Training Academy'
        self.base_url = 'http://www.ebi.ac.uk'
        self.instructors = dict()
        self.providers = dict()

    def can_handle(self, url):
        if url.startswith('http://www.ebi.ac.uk/training/'):
            return True
        else:
            return False
    
    def scrape(self, url, verbose=0):
       
        if url == 'http://www.ebi.ac.uk/training/online/' :
            return self.scrape_overview(url)
        else:
            print(self.name, ": Don't know how to handle", url)
 

    
    def scrape_overview(self,url):
        sess = get_js_session(url)
        soup = BeautifulSoup(sess.body(),"lxml")
        pages_link = []
        course_links = set()
        union_course_links = set()
        data=set()
        page_link = self.get_pages_link(soup)
        union_course_links = self.harvest_course_links(soup)
        for p_l in page_link :
            soup = self.get_expanded_soup(p_l)
            course_links = self.harvest_course_links(soup)
            union_course_links = set(union_course_links).union(set(course_links))
        print('harvested', len(union_course_links), 'links!')
        for c_l in tqdm(union_course_links):
            try:
                course = self.get_course_info(c_l)
                data.add(course)
            except KeyboardInterrupt:
                break
            except:
                print('course failed:', c_l)
                print(traceback.format_exc())
    
        return data
    
    '''
    This function grabs all the links for the pages 
    '''  
    def get_pages_link(self,soup):
        pages_link = []
        for pages in soup.findAll('li',attrs={'class':'pager-item'}):
            link =self.base_url+str(pages.find('a')['href'])
            pages_link.append(link)
        return pages_link

    ''' 
    This function captures all the links of the courses
    '''
    def harvest_course_links(self,soup):
        links=set()
        for v_row in soup.findAll('div', attrs={'class': 'views-row'}):
            try:
                c_link = self.base_url+v_row.find('a')['href']
                links.add(c_link)
            except (AttributeError, TypeError):
                pass
        return links

    def get_course_info(self,url):
        soup = self.get_expanded_soup(url)
        course =  LearningResource()
        course.title = save_get_text(soup.find('div',attrs={'id':'local-title'}).find('h1').find('span'))
        course.id = url
        course.url = url
        try:   
            course.description = '\n'.join(filter(lambda x: x != '', [save_get_text(p) for p in
                                                soup.find('div',attrs={'class':'field-name-field-course-description'}).findAll('p')]))
            course.prerequisite_concept = '\n'.join(filter(lambda x: x != '', [save_get_text(r) for r in
                                                soup.find('div',attrs={'class':'field-name-field-course-pre-requisites'}).findAll('p')]))
                                                
        except AttributeError:
            pass
        about_course = soup.find('div',attrs={'class':'group-course-about'})
        instructor_link = self.base_url + about_course.find('div',attrs={'class':'field-name-author-list'}).find('a')['href']
        category = about_course.findAll('div',attrs={'class':'course-subject-term'})
        
        try :
            for c in range(len(category)):
                course_cat= category[c].find('a')['href']
                course.courses.append(course_cat)
        except AttributeError:
            pass
        
        
        course.difficulty = save_get_text(about_course.find('div',attrs={'class':'field-name-field-course-level'}))
    
        course.typical_learning_time = save_get_text(about_course.find('div',attrs={'class':'field-name-field-course-duration'}))  
        
        try:
            learn_objectives = soup.find('div',attrs={'class':'field-name-field-learning-objectives'})
            course.objectives = save_get_text(learn_objectives.find('ul',attrs={'class':'textformatter-list'}))
        except AttributeError:
            pass
        course.rating = save_get_text(soup.find('div',attrs={'class':'field-name-field-course-rating'}))
        
        course.syllabus = self.get_course_syllabus(soup)
        
        instructor = self.get_instructor_info(instructor_link, course)
        course.instructors = instructor
        return course

    def get_course_syllabus(self,soup):
        syllabus_panel = soup.find('aside',attrs={'class':'grid_6'}).find('ul',attrs={'class':'menu'})
        try:
            syllabus_content = '\n'.join(filter(lambda x: x != '', [save_get_text(p) for p in
                             syllabus_panel.findAll('li',attrs={'class':'expanded'})]))
        
        except AttributeError:
            pass
        return syllabus_content
    

    def get_instructor_info(self,url,course):
        soup = self.get_expanded_soup(url)
        instructor = Instructor()
        instructor.id = 'EBI' + str(id(instructor)%200)
        instructor.full_name = save_get_text(soup.find('div',attrs={'class':'pane-field-trainer-name'}))
        try:
            parts_name = instructor.full_name.split(" ")
            instructor.first_name = parts_name[0]
            instructor.last_name =  parts_name[len(parts_name)-1]
            if (len(parts_name)==3):
                instructor.middle_name = parts_name[1]
        except AttributeError:
            pass
        instructor.works_for = save_get_text(soup.find('div',attrs={'class':'field-name-field-company'}))
        instructor.job_title = save_get_text(soup.find('div',attrs={'class':'field-name-field-job-title'}))
        instructor.mail_id = save_get_text(soup.find('div',attrs={'class':'pane-field-trainer-mail'}))
        
        bio = self.get_bio(url,soup,instructor)
        instructor.biography.add(bio)
                
            
        if course not in instructor.teaches:
            instructor.teaches.add(course)
        
        return instructor
    
    def get_bio(self,url,soup,instructor):
        bio = Bio()
        bio.url = url
        bio.id = url
        bio.instructor_id = instructor.id
        bio_field = soup.find('div',attrs={'class':'field-name-field-bio'})
         
        try:
            bio.bio =  '\n'.join(filter(lambda x: x != '', [save_get_text(p) for p in
                                                    bio_field.findAll('p')]))
        except AttributeError:
            pass
        
        return bio
    
    def get_expanded_soup(self,url):
            sess = get_js_session(url)
            try:
                click_buttons(sess, "//span[contains(@class, 'see-more-label')]")
                click_buttons(sess, "//span[contains(@class, 'show-content-cta')]")
            except:
                    pass
            wait_until_session_stable(sess)
            soup = BeautifulSoup(sess.body(), "lxml")
            return soup

