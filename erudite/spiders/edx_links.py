from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from erudite.items import LearningResource

import re
import nltk
import json

class EdxHtmlFileCourseSpider(Spider):
    name = "edx_html_links"
    allowed_domains = ["edx.org"]
    start_urls = [
        #"https://www.edx.org/course?search_query=data+science"        
        "file:///Users/Gully/Documents/Projects/2_active/bigDataU/work/2016-07-07_horseman/Data%20Analysis%20&%20Statistics%20_%20edX.html",
        "file:///Users/Gully/Documents/Projects/2_active/bigDataU/work/2016-07-07_horseman/Computer%20Science%20_%20edX.html"
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
        course_links = sel.css('.course-link::attr(href)').extract()

        for course_link in course_links:
            
            item = LearningResource()
            item['typeOfResource'] = "MOOC Course"

            #item['name'] =  sel.xpath('//h1[@class="course-intro-heading"]')
            item['url'] =  course_link
            #item['identifier'] = course['guid']
            #item['url'] = course['url']
            #item['language'] = ", ".join(course['languages'])
            
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