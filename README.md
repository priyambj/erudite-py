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

### Coursera

This scraper goes to `https://www.coursera.org/browse/data-science?languages=en`, clicks on each Button marked 'See All', loads each one of the course pages from the resultant links and then scrapes them for details.

### EDX

This is scraper goes to `https://www.edx.org/course/subject/computer-science`, attempts to scroll down to force the loading of all the appropriate pages to load the URLS of each page. We then intend to scrape each page for details. 

> Currently, this process does not work. The dryscrape engine executes the scrolling function intermittently within the webkit-server engine and does not force a reload of more pages more than once or twice. We need a new solution to this issue.  


