from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from erudite.items import LearningResource

import re
import nltk
import json

class EdxCourseSpider(Spider):
    name = "edx_courses"
    allowed_domains = ["edx.org"]
    start_urls = [
        #"https://www.edx.org/course?search_query=data+science"        
        "https://www.edx.org/search/api/all"
    ]

    def parse(self, response):
        
        """
        @url http://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=data+science&collapse=
        @scrapes name
        """
        #
        # The top-level URL returns the entire edx catalog as a JSON file.
        # This information does not include much of the descriptions and other 
        # course metadata so we spider the URLs for more details
        # 
        sel = Selector(response)
        courses = json.loads(response.body)

        for course in courses:
            
            item = LearningResource()
            item['typeOfResource'] = "MOOC Course"

            #item['name'] =  sel.xpath('//h1[@class="course-intro-heading"]')
            item['name'] =  course['l']
            item['identifier'] = course['guid']
            item['url'] = course['url']
            item['language'] = ", ".join(course['languages'])
            
            yield item
        #for course in courses:
        #    url = course['url']
        #    yield Request(url, callback=self.parse_course_page)            
    
    #def parse_course_page(self, response):
    #    
    #    sel = Selector(response)
    #    
    #    item = LearningResource()
    #    item['typeOfResource'] = "MOOC Course"

    #    item['name'] =  sel.xpath('//h1[@class="course-intro-heading"]')
        #item['identifier'] = course['guid']
        #item['url'] = course['url']
        #item['language'] = ", ".join(course['languages'])
            
        #desc = course.xpath('div[@class="courseDescription"]/text()').extract_first()
        #match = re.search("^\s+(\S.*\S)\s+$", desc)
        #if match:
        #    item['description'] = match.group(1)
        #else:
        #    item['description'] = desc

        #sentences = nltk.sent_tokenize(item['description'])
        #for line in sentences:
        #    match_prerequisites = re.search(r"Prerequisites*:\s*(\S+.*\.)$", line) 
        #    if match_prerequisites:
        #        item['prerequisites'] = match_prerequisites.group(1)
                    
        #datePublished = course.xpath('//h3[@class="sectionContainerTerm"]/text()').extract_first()
        #item['datePublished'] = datePublished
                            
        #yield item