from __future__ import print_function, division

import sys
import bs4 as bs
import time
import pandas as pd
import dryscrape
import time
import json

from scraper import erudite_schema as es

from tqdm import tqdm

if 'linux' in sys.platform:
    # start xvfb in case no X is running. Make sure xvfb 
    # is installed, otherwise this won't work!
    dryscrape.start_xvfb()
    
def get_page_session(url, wait=2):
    sess = dryscrape.Session()
    sess.set_viewport_size(width=1024, height=20000)
    sess.visit(url)
    time.sleep(30)

    name = url.rsplit('/', 1)[-1]  
    sess.render( 'data/coursera/specializations/' + name + '.png')
    
    return sess

def click_buttons(sess, xpath):
    for button in sess.xpath(xpath):
        #print('click button')
        try:
            button.click()
        except:
            #print('\tdone')
            break    

def get_specialization_df(url):
    sess = get_page_session(url)
    
    #expand all syllabus details
    click_buttons(sess, "//div[contains(@class, 'course-show-syllabus-text')]")
    
    time.sleep(5)

    name = url.rsplit('/', 1)[-1]  
    sess.render( 'data/coursera/specializations/' + name + '_button.png')
    
    soup = bs.BeautifulSoup(sess.body(), "lxml")
    courses = soup.find_all('div', attrs={'class': 'rc-SingleCourse'})
    data = list()
    titles = set()
    for idx, c in enumerate(courses):
        title = c.find('div', attrs={'class': 'course-title'}).getText(separator=u' ')
        if title in titles:
            continue
        else:
            titles.add(title)
        print(title)
        about = c.find('div', attrs={'class': 'course-about'}).getText(separator=u' ')
        try:
            syllabus = c.find('div', attrs={'class': 'rc-Syllabus'}).getText(separator=u' ')
        except:
            syllabus = ''
        data.append((idx, title, about, syllabus))
    sess.reset()
    return pd.DataFrame(columns=['course_num', 'title', 'about', 'syllabus'], data=data)

def get_specialization_links(url):
    sess = get_page_session(url)
    spec_pages = list()
    current_idx = 0;
    while True:
        for exp_idx, expand_button in enumerate(sess.xpath("//button[contains(@class, 'primary see-all-button')]")):
            if current_idx == exp_idx:
                print('click' + str(current_idx))
                expand_button.left_click()
                time.sleep(20)
                spec_pages.append(sess.body())
                current_idx += 1
                name = url.rsplit('/', 1)[-1]  
                sess.render( 'data/coursera/specializations/' + name + '_' + str(current_idx) + '.png')
                sess = get_page_session(url)
                break
        else:
            break
        
            
    spec_urls = set()
    for sp in spec_pages:
        sp = bs.BeautifulSoup(sp, "lxml")
        js_obj = json.loads(sp.find('script', attrs={'type': 'application/ld+json'}).getText())
        for item in  js_obj['itemListElement']:
            url = item['url']
            if url.startswith('https://www.coursera.org/specializations/'):
                spec_urls.add(url)
                print(url)
    return spec_urls

spec_links = get_specialization_links('https://www.coursera.org/browse/data-science')
print("\n".join(spec_links))

courses = set()
for l in tqdm(spec_links):
    sys.stdout.flush()
    name = l.rsplit('/', 1)[-1]    
    print('process', name)
    print('-' * 80)
    df = get_specialization_df(l)
    #print(df.head(2))
    df.to_pickle('data/coursera/specializations/' + name + '.df')
    df.to_csv('data/coursera/specializations/' + name + '.csv', encoding='utf-8', index=False)
    courses.update(set(df['title']))
    print('=' * 80)
    
print('num specializations:', len(spec_links))
print('overall courses:', len(courses))