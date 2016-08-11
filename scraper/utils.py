from __future__ import print_function
from time import sleep
from bs4 import BeautifulSoup
import datetime
import sys
import re


def get_soup(url, js=False, wait=5, return_session=False, verbose=0):
    if js:
        session = get_js_session(url, verbose=verbose)
        content = session.body()
    else:
        page, session = get_rq_page(url, wait=wait, return_session=True, verbose=verbose)
        content = page.content

    soup = BeautifulSoup(content, "lxml")
    if return_session:
        return soup, session
    else:
        return soup


def get_js_session(url, viewport=(1024, 768), render_fn=None, verbose=0):
    import dryscrape

    if 'linux' in sys.platform:
        # start xvfb in case no X is running. Make sure xvfb
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()

    sess = dryscrape.Session()
    sess.set_viewport_size(width=viewport[0], height=viewport[1])
    sess.visit(url)

    # print("loading page from " + url)
    wait_until_session_stable(sess, verbose=verbose)
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


def wait_until_session_stable(sess, time_res=1, max_wait=30, queue_length=5, verbose=0):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=max_wait)
    v_print(verbose, 'chillout', end='')
    last_len = len(sess.body())
    c = queue_length
    while datetime.datetime.now() <= end and c > 0:
        sess_len = len(sess.body())
        if sess_len == last_len:
            c -= 1
            v_print(verbose, '.', end='')
        else:
            last_len = sess_len
            c = queue_length
            v_print(verbose, '+', end='')
        sleep(time_res)
    v_print(verbose)
    return c == 0


def get_rq_page(url, wait=5, return_session=True, verbose=0):
    import requests

    url = re.findall(u'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)[-1]

    session = requests.Session()
    session.mount("http://", requests.adapters.HTTPAdapter())
    session.mount("https://", requests.adapters.HTTPAdapter())
    page = session.get(url=url, allow_redirects=True, timeout=wait, verify=True)
    if return_session:
        return page, session
    else:
        return page


def click_buttons(sess, xpath, verbose=0):
    for button in sess.xpath(xpath):
        v_print(verbose, 'click button')
        try:
            button.click()
        except:
            v_print(verbose, '\tdone')
            break


def save_get_text(soup, blank_value=''):
    try:
        return soup.getText(separator=u' ').strip()
    except AttributeError:
        return blank_value


def v_print(v, *args, **kwargs):
    if v:
        print(*args, **kwargs)


def render_js_sess(sess, fn):
    if not isinstance(fn, str) or fn != '':
        fn = str(fn)
        if not fn.endswith('.png'): fn += '.png'
        sess.render(fn + ".png")


def extract_data(obj, fields, blank_value=''):
    d = list()
    obj_vars = vars(obj)
    for f in fields:
        try:
            val = obj_vars[f]
            if isinstance(val, (tuple, list, set)):
                val = list(filter(lambda x: x is not None and x != '', val))
                if len(val) > 0:
                    val = val[0]
                else:
                    val = ''
            elif not isinstance(val, basestring):
                val = str(val)
        except KeyError:
            val = blank_value
        d.append(val)
    return d
