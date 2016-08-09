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

Docker
---
We also provide a docker image including all needed libraries to run the framework. The docker image can be run using 
```
docker run -i -t -p 8888:8888 floriangeigl/erudite
```
The framework within the docker image can be found at /home/erudite/erudite/. Please consider using ```git pull``` within this directory to update to the latest version available. The included ipython notebooks should then be available at localhost:8888.

### Updating to the latest docker image
After the inital run you can always update to the latest docker image using:
```
docker pull floriangeigl/erudite
```
Please be aware that your data within the docker image might get lost during the update. Hence we recommend to commit and push your changes to the erudite github repository before doing the udpate.
