from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from erudite.items import LearningResource

import re
import nltk

class StanfordProgramSpider(Spider):
    name = "stanford_programs"
    allowed_domains = ["stanford.edu"]
    start_urls = [
        "https://statistics.stanford.edu/academics/ms-statistics-data-science",
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url https://statistics.stanford.edu/academics/ms-statistics-data-science/
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//div[@class="field-item even"]//ul/li')
        items = []

        for site in sites:
            item = LearningResource()

            item.prerequisiteKeys.extend(site.xpath('//li/text()').extract())
            item['pre'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)

        return items

class StanfordCourseSpider(Spider):
    name = "stanford_courses"
    allowed_domains = ["stanford.edu"]
    start_urls = [
        "http://explorecourses.stanford.edu/search?view=catalog&academicYear=&page=0&q=STATS&filter-departmentcode-STATS=on&filter-coursestatus-Active=on&filter-term-Summer=on",
        "http://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=CS&collapse=",
        "http://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=CME&collapse=",
        "http://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=BIOE&collapse=",
        "http://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=OIT&collapse=",
        "http://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=BioMedin&collapse=",        
    ]

    def parse(self, response):
        
        """
        @url http://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=data+science&collapse=
        @scrapes name
        """
        sel = Selector(response)
        courses = sel.xpath('//div[@class="searchResult"]/div[@class="courseInfo"]')

        for course in courses:
            item = LearningResource()
            item['typeOfResource'] = "University Course"

            item['name'] = course.xpath('h2/span[@class="courseTitle"]/text()').extract_first()
            item['identifier'] = course.xpath('h2/span[@class="courseNumber"]/text()').extract_first()
            item['url'] = response.url
            
            desc = course.xpath('div[@class="courseDescription"]/text()').extract_first()
            match = re.search("^\s+(\S.*\S)\s+$", desc)
            if match:
                item['description'] = match.group(1)
            else:
                item['description'] = desc

            sentences = nltk.sent_tokenize(item['description'])
            for line in sentences:
                match_prerequisites = re.search(r"Prerequisites*:\s*(\S+.*\.)$", line) 
                if match_prerequisites:
                    item['prerequisites'] = match_prerequisites.group(1)
                    
            datePublished = course.xpath('//h3[@class="sectionContainerTerm"]/text()').extract_first()
            item['datePublished'] = datePublished
                            
            yield item
            
        links = sel.xpath('//div[@id="pagination"]/a/@href')
        for link in links:
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse)
            