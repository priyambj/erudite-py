from scraper.field_definitions import Fields
from scraper.scraper import Scraper
from scraper.website.coursera import Coursera
from scraper.website.edx import EDX
from scraper.utils import *
import datetime

scraper = Scraper(fields_of_interest=[Fields.title, Fields.description, Fields.syllabus])
scraper.register_website(Coursera())
scraper.register_website(EDX())

urls = ['none',
        'https://www.edx.org/course/subject/computer-science']
#        'https://www.coursera.org/browse/data-science']

df = scraper.scrape(urls)

df.to_pickle('EDX' + format(datetime.datetime.now()) + '.pkl')
df.to_csv('EDX' + format(datetime.datetime.now()) + '.tsv', sep='\t', encoding='utf-8')