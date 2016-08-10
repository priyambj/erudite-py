from __future__ import print_function
from website.website_interface import WebsiteInterface
# from joblib import delayed, Parallel
import traceback
import numpy as np
import pandas as pd
from collections import defaultdict
from operator import itemgetter


class Scraper:
    def __init__(self, fields_of_interest=None):
        self.website_scrapers = dict()
        if fields_of_interest is None:
            self.fields_of_interest = []
        else:
            self.fields_of_interest = fields_of_interest

    def register_website(self, ws):
        if not isinstance(ws, WebsiteInterface):
            print('No website interface')
        else:
            website_name = ws.name
            if website_name in self.website_scrapers:
                print('WARN: overwrite existing scraper.')
            self.website_scrapers[website_name] = ws

    def scrape(self, url, wait=5):
        if isinstance(url, str):
            url = [url]
        data = list()
        fails = defaultdict(int)
        for u in url:
            try:
                s_name, s = self.find_scraper(u)
            except KeyError:
                continue

            try:
                print(s_name, 'scraping', u, '...')
                d = s.scrape(u, wait)
                if isinstance(d, dict):
                    d = [d]
                for i in d:
                    i['scraper'] = s_name
                data.extend(d)
            except:
                # protection if any scraper fails...
                print(s_name, 'failed to handle "', u, '"')
                fails[s_name] += 1
                print(traceback.format_exc())

        df_data = list()
        unused_fields = set()
        for course in data:
            course_data = list()
            for f in self.fields_of_interest:
                try:
                    course_data.append(course[f])
                except KeyError:
                    course_data.append(np.nan)
            unused_fields.update(set(course.keys()) - set(self.fields_of_interest))
            df_data.append(tuple(course_data))
        if unused_fields:
            print('ignored the following fields:', ', '.join(sorted(unused_fields)))
        if len(fails) > 0:
            print('statistics of scraper fails:')
            for n, f in sorted(fails.items(), key=itemgetter(1), reverse=True):
                print('\t', n, ':', f)
        return pd.DataFrame(columns=self.fields_of_interest, data=df_data)

    def find_scraper(self, url):
        for name, ws in self.website_scrapers.items():
            if ws.can_handle(url):
                return name, ws
        else:
            print('no registered scraper could handle"', url, '"')
            raise KeyError