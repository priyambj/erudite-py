from __future__ import print_function
from scraper.scraper import Scraper
from scraper.website.coursera import Coursera
from scraper.website.edx import EDX

scraper = Scraper()
scraper.register_website(Coursera())
scraper.register_website(EDX())

urls = ['none',
        'https://www.edx.org/course/subject/data-analysis-statistics']
#        'https://www.coursera.org/browse/data-science']

df_dict = scraper.scrape(urls)
for key, val in df_dict.items():
    # print(val.head(2))
    val.to_csv(key + '.csv', encoding='utf-8')


#df.to_pickle('EDX' + format(datetime.datetime.now()) + '.pkl')
#df.to_csv('EDX' + format(datetime.datetime.now()) + '.csv', sep='\t', encoding='utf-8')