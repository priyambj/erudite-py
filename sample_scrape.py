from scraper.field_definitions import Fields
from scraper.scraper import Scraper
from scraper.website import *


scraper = Scraper(fields_of_interest=[Fields.title, Fields.description, Fields.syllabus])
scraper.register_website(Coursera())

urls = ['none',
        'https://www.coursera.org/browse/data-science']

df = scraper.scrape(urls)
print(df.head(2))
