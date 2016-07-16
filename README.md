# erudite-scrapy

This is a Scrapy project to aggregate metadata about data science courses

This project is a part of the BigDataU `Erudite` and should be used in conjunction with the `erudite-horseman` project. 

Items
=====

The items scraped by this project are websites, and the item is defined in the
class::

    erudite.items.LearningResource

See the source code for more details.

Spiders
=======

This project contains several spiders for each resource to be crawled. 

* The ``stanford`` spider scrapes pages from the Stanford Catalog: [http://explorecourses.stanford.edu/]([http://explorecourses.stanford.edu/).
* The ``edx`` spider was intended to scrape pages from the EdX.com Catalog: [https://www.edx.org//]([https://www.edx.org//), but because that site uses extensive Javascript and asynchronous function calls to execute

Pipelines
=========

None active currently