from __future__ import print_function

from time import sleep
from tqdm import tqdm
import traceback
import sys
sys.setrecursionlimit(10000)

from scraper.erudite_schema import *
from scraper.erudite_schema import LearningResource
from scraper.utils import *
from scraper.website.website_interface import WebsiteInterface
import urllib2


class VideoLectures (WebsiteInterface):
    def __init__(self):
        WebsiteInterface.__init__(self)
        self.name = 'Video Lectures Data Science '
        self.base_url = 'http://videolectures.net'
        self.instructors = dict()
        self.providers = dict()

    def can_handle(self, url):
        if url.startswith('http://videolectures.net/'):
            return True
        else:
            return False
    
    def scrape(self, url, verbose=0):
       
        if url == 'http://videolectures.net/' :
            return self.scrape_overview(url)
        else:
            print(self.name, ": Don't know how to handle", url)
    
    def scrape_overview(self,url):
        comp_links = set()
        data = set()
        sess = get_js_session(url)
        soup1 = BeautifulSoup(sess.body(),"lxml")
        browse_course_link = self.base_url+ soup1.find('li',attrs={'id':'tm_browse'}).find('a')['href']
    
        course_page = self.get_expanded_soup(browse_course_link)
        for i in tqdm(range(1,282)):
            url = "http://videolectures.net/site/ajax/drilldown/?p="+str(i)+"&cid=633&w=5" 
            links = self.get_course_links(url)
            comp_links = set(links).union(set(comp_links))
        print('harvested', len(comp_links), 'comp_links!')
        for c_l in tqdm(comp_links):
            course = self.get_course_info(c_l)
            data.add(course)
            
            
        return data
    

    def get_course_links(self,url):
        links = set()
        soup = self.get_soup(url)
        for card in soup.findAll('div',attrs={'class':'lec_thumb'}):
            try:
                c_link=self.base_url+card.find('a')['href']
                links.add(c_link)
            except AttributeError:
                pass
        
        return links
     
    def get_course_info(self,url):
        course = LearningResource()
        try:
            soup = self.get_expanded_soup(url)
            course.id = url
            course.url = url
            course.title = save_get_text(soup.find('div',attrs={'id':'drilldown_list'}).find('h2'))
            
            lec_data = soup.find('div',attrs ={'class':'lec_data'})
            instructor_link = self.base_url + lec_data.find('a')['href']
            instructor = self.get_instructor_info(instructor_link,course)
            instructor.works_for.add(lec_data.find('a').next_sibling)
            
            course.instructors.add(instructor)
            
            course.created = lec_data.find('br').find_next_sibling().next_sibling
            course.available = lec_data.find('br').find_next_sibling().find_next_sibling().next_sibling
            course.views = lec_data.find('br').find_next_sibling().find_next_sibling().find_next_sibling().next_sibling
            
            category_path = soup.find('legend').find_next_sibling()
            cat_links = category_path.findAll('a')
            for c_l in cat_links:
                category = save_get_text(c_l)
                if category not in course.part_of:
                    course.part_of.append(category)
        
            course.description =  '\n'.join(filter(lambda x: x != '', [save_get_text(p) for p in
                                                        soup.find('div',attrs={'class':'wiki'}).findAll('p')]))
            course.url = self.base_url + soup.find('div',attrs={'id':'vl_seealso'}).find('a')['href']
        except AttributeError:
            pass
        
        rate=0
        stars = soup.find('span',attrs={'class':'rating'}).findAll('span',attrs={'class':'star on'})
        for s in stars:
            rate+=1
        course.rating = str(rate)
        course.syllabus = self.get_syllabus(url,course)
        return course
    
    def get_syllabus(self,url,course):
        try:
            soup = self.get_expanded_soup(url)
            syll_table = soup.find('table',attrs={'id','sync_list'})
            course.syllabus =  '\n'.join(filter(lambda x: x != '', [save_get_text(p) for p in
                                                        syll_table.findAll('a')]))
        except AttributeError:
            pass
    

    def get_instructor_info(self,url,course):
        instructor = Instructor()
        try :
            soup = self.get_expanded_soup(url)
            instructor.id = "VDL" +str(id(instructor))
         
            instructor.full_name = soup.find('span',attrs={'class':'auth_name '}).find('a').text
            instructor.url = soup.find('span',attrs={'class':'auth_name'}).find('a')['href']
            parts_name = instructor.full_name.split(" ")
            instructor.first_name = parts_name[0]
            instructor.last_name =  parts_name[len(parts_name)-1]
            if (len(parts_name)==3):
                instructor.middle_name = parts_name[1]
        except AttributeError:
            pass
        if instructor.full_name == " ":
           instructor.full_name = save_get_text(soup.find('span',attrs={'class':'auth_name '}))
        bio = self.get_bio(url,soup,instructor)
        instructor.biography.add(bio)
                
            
        if course not in instructor.teaches:
            instructor.teaches.add(course)
        
        return instructor
    
    def get_bio(self,url,soup,instructor):
        bio = Bio()
        try:
            bio.url = url
            bio.id = instructor.url
            bio.instructor_id = instructor.id
            bio_field = soup.find('span',attrs={'id':'auth_desc_edit'})
            
            bio.bio = " "
            bio.bio = '\n'.join(filter(lambda x: x != '', [save_get_text(p) for p in
                                                        bio_field.findAll('p')]))
        except AttributeError:
            pass
        return bio

    

    def get_soup(self,url):
        response = urllib2.urlopen(url).read()
        return BeautifulSoup(response,"html.parser")
        
        
    def get_expanded_soup(self,url):
            sess = get_js_session(url)
            wait_until_session_stable(sess)
            soup = BeautifulSoup(sess.body(), "lxml")
            return soup

        
 