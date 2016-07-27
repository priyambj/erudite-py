from __future__ import print_function
from time import sleep
from bs4 import BeautifulSoup
import sys


def get_soup(url, js=False, wait=5, return_session=False):
    if js:
        session = get_js_session(url, wait=wait)
        content = session.body()
    else:
        page, session = get_rq_page(url, wait=wait, return_session=True)
        content = page.content

    soup = BeautifulSoup(content, "lxml")
    if return_session:
        return soup, session
    else:
        return soup


def get_js_session(url, wait=5, viewport=(1024, 768), render_fn=None):

    import dryscrape

    if 'linux' in sys.platform:
        # start xvfb in case no X is running. Make sure xvfb
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()

    sess = dryscrape.Session()
    sess.set_viewport_size(width=viewport[0], height=viewport[1])
    sess.visit(url)
    sleep(wait)
    if render_fn:
        if not render_fn.endswith('.png'):
            render_fn += '.png'
        sess.render(render_fn)
    return sess


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
