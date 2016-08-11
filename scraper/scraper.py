from __future__ import print_function
from website.website_interface import WebsiteInterface
# from joblib import delayed, Parallel
import traceback
import pandas as pd
from collections import defaultdict
from operator import itemgetter
from erudite_schema import *
from utils import extract_data
from tqdm import tqdm


class Scraper:
    def __init__(self):
        self.website_scrapers = dict()
        self.fails = defaultdict(list)

    def register_website(self, ws):
        if not isinstance(ws, WebsiteInterface):
            print('No website interface')
        else:
            website_name = ws.name
            if website_name in self.website_scrapers:
                print('WARN: overwrite existing scraper.')
            self.website_scrapers[website_name] = ws

    def scrape(self, url):
        if isinstance(url, str):
            url = [url]
        data = list()
        for u in url:
            try:
                s_name, s = self.find_scraper(u)
            except KeyError:
                continue

            try:
                print(s_name, 'scraping', u, '...')
                d = s.scrape(u)
                if isinstance(d, dict):
                    d = [d]
                for i in d:
                    i.venue = s_name
                data.extend(d)
            except:
                # protection if any scraper fails...
                print(s_name, 'failed to handle "', u, '"')
                self.fails[s_name].append(u)
                print(traceback.format_exc())

        data_dict = defaultdict(list)
        columns_dict = defaultdict(None)

        print('extract data for database...')
        added_instructors = set()
        added_providers = set()
        for d in tqdm(data):
            if isinstance(d, LearningResource):
                table_name = 'learning_resource'
                data_dict[table_name].append(extract_data(d, d.db_fields))
                columns_dict[table_name] = d.db_fields
                for c in d.courses:
                    table_name = 'part_of'
                    data_dict[table_name].append([c, d.id])
                    columns_dict[table_name] = ['child_resource_id', 'parent_resource_id']

                prereq = d.prerequisite
                if prereq is not None:
                    table_name = 'prerequisite'
                    columns_dict[table_name] = ['resource_id', 'prerequisite_id', 'prerequisite_concept']
                    if isinstance(prereq, basestring) and prereq != '':
                        data_dict[table_name].append([d.id, '', prereq])
                    else:
                        for p in prereq:
                            data_dict[table_name].append([d.id, '', p])
                for i in d.instructors:
                    if i not in added_instructors:
                        added_instructors.add(i)
                        table_name = 'instructor'
                        columns_dict[table_name] = i.db_fields
                        data_dict[table_name].append(extract_data(i, i.db_fields))

                        for b in i.biography:
                            if b:
                                table_name = 'has_bio'
                                columns_dict[table_name] = b.db_fields
                                data_dict[table_name].append(extract_data(b, b.db_fields))
                        table_name = 'works_for'
                        columns_dict[table_name] = ['instructor_id', 'provider_id', 'department']
                        works_for = i.works_for
                        if works_for:
                            if isinstance(works_for, basestring):
                                data_dict[table_name].append([i.id, works_for, ''])
                            elif isinstance(works_for, Provider):
                                data_dict[table_name].append([i.id, works_for.id, ''])
                            else:
                                for w in i.works_for:
                                    data_dict[table_name].append([i.id, w, ''])
                    table_name = 'teaches'
                    columns_dict[table_name] = ['instructor_id', 'resource_id']
                    data_dict[table_name].append([i.id, d.id])
                provider = d.provider
                if provider:
                    table_name = 'provides'
                    columns_dict[table_name] = ['provider_id', 'resource_id']
                    data_dict[table_name].append([provider.id, d.id])
                    if provider not in added_providers:
                        added_providers.add(provider)
                        table_name = 'provider'
                        columns_dict[table_name] = provider.db_fields
                        data_dict[table_name].append(extract_data(provider, provider.db_fields))

            elif isinstance(d, Instructor):
                if i not in added_instructors:
                    added_instructors.add(i)
                    table_name = 'instructor'
                    columns_dict[table_name] = i.db_fields
                    data_dict[table_name].append(extract_data(i, i.db_fields))
            elif isinstance(d, Bio):
                pass
            else:
                print("can't handle the following instance retrieved from scraper:", d)

        if len(self.fails) > 0:
            print('statistics of scraper fails:')
            for n, f in sorted(self.fails.items(), key=itemgetter(1), reverse=True):
                print('\t', n, ':', len(f))
        df_dict = dict()
        print('create dataframes')
        for key, val in data_dict.items():
            print(key)
            col_names = columns_dict[key]
            df_dict[key] = pd.DataFrame(columns=col_names, data=val)
        return df_dict

    def find_scraper(self, url):
        for name, ws in self.website_scrapers.items():
            if ws.can_handle(url):
                return name, ws
        else:
            print('no registered scraper could handle"', url, '"')
            raise KeyError
