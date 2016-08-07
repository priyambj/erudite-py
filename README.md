# erudite-py

This is a python project containing scripts for web-scraping, data analysis and visualization in the **BigDataU Educational Resource Indexing** (`ERudIte`) project.

The majority of code for this system was built by [Florian Geigl](https://github.com/orgs/BMKEG/people/floriangeigl) 

Web Scraping
---
The system is run within a python script using the following method. First we write a scraper and register each scraper into the system (e.g., Coursera, EDX) and then run this on the system:

```
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
        'https://www.coursera.org/browse/data-science']

df = scraper.scrape(urls)

df.to_csv('EDX' + format(datetime.datetime.now()) + '.tsv', sep='\t', encoding='utf-8')
```



