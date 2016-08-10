from __future__ import print_function
from time import sleep
from bs4 import BeautifulSoup
import datetime

import sys


def get_soup(url, js=False, wait=5, return_session=False):
    if js:
        session = get_js_session(url)
        content = session.body()
    else:
        page, session = get_rq_page(url, wait=wait, return_session=True)
        content = page.content

    soup = BeautifulSoup(content, "lxml")
    if return_session:
        return soup, session
    else:
        return soup


def get_js_session(url, viewport=(1024, 768), render_fn=None):
    import dryscrape

    if 'linux' in sys.platform:
        # start xvfb in case no X is running. Make sure xvfb
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()

    sess = dryscrape.Session()
    sess.set_viewport_size(width=viewport[0], height=viewport[1])
    sess.visit(url)

    # print("loading page from " + url)
    wait_until_session_stable(sess)
    # print("Wait " + str(wait) + " seconds")
    # sleep(wait)

    if render_fn:
        if not render_fn.endswith('.png'):
            render_fn += '.png'
        sess.render(render_fn)
    return sess


"""
    GULLY: Wait function to hang around until the page returned stabilizes to a 
    set length for a set period of time. This means we don't have to guess 
    about the wait times for loading pages.  
"""


def wait_until_session_stable(sess, time_res=1, max_wait=30, queue_length=5):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=max_wait)
    print('chillout', end='')
    last_len = len(sess.body())
    c = queue_length
    while datetime.datetime.now() <= end and c > 0:
        sess_len = len(sess.body())
        if sess_len == last_len:
            c -= 1
            print('.', end='')
        else:
            last_len = sess_len
            c = queue_length
            print('+', end='')
        sleep(time_res)
    print()
    return c == 0


def get_rq_page(url, wait=5, return_session=True):
    import requests

    session = requests.Session()
    session.mount("http://", requests.adapters.HTTPAdapter())
    session.mount("https://", requests.adapters.HTTPAdapter())
    page = session.get(url=url, allow_redirects=True, timeout=wait, verify=True)
    if return_session:
        return page, session
    else:
        return page


def click_buttons(sess, xpath):
    for button in sess.xpath(xpath):
        # print('click button')
        try:
            button.click()
        except:
            # print('\tdone')
            break


def save_get_text(soup):
    if soup is None:
        return None
    else:
        try:
            return soup.getText(separator=u' ')
        except:
            return None