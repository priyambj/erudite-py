from __future__ import print_function
from scraper.scraper import Scraper
from scraper.website.coursera import Coursera
from scraper.website.edx import EDX
from scraper.website.bigdatauniversity import BigDataUniversity
from scraper.website.ebi import EBI
from scraper.website.videolectures import VideoLectures
from csv import QUOTE_ALL

scraper = Scraper()
scraper.register_website(Coursera())
scraper.register_website(EDX())
scraper.register_website(BigDataUniversity())
scraper.register_website(EBI())
scraper.register_website(VideoLectures())


urls = ['none',
        'https://www.edx.org/course/subject/data-analysis-statistics',
       'http://videolectures.net/']
#        'https://www.coursera.org/browse/data-science']

df_dict = scraper.scrape(urls)
for key, val in df_dict.items():
    # print(val.head(2))
    val.to_csv(key + '.csv', encoding='utf-8', index=False, quoting=QUOTE_ALL)
    val.to_pickle(key + '.df')

# please ignore the KeyError on exit - it is a bug in one of the used libraries. I've already submitted a pull request
# to fix this bug.


#df.to_pickle('EDX' + format(datetime.datetime.now()) + '.pkl')
#df.to_csv('EDX' + format(datetime.datetime.now()) + '.csv', sep='\t', encoding='utf-8')
