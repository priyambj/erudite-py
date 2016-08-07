from __future__ import print_function
from time import sleep
from bs4 import BeautifulSoup
from collections import deque

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
    
    #print("loading page from " + url)
    wait = wait_until_session_stable(sess)
    #print("Wait " + str(wait) + " seconds")
    #sleep(wait)
    
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
def wait_until_session_stable(sess, time_res=1, max_wait=30, queue_length = 5):

    start_len = len(sess.body())
    #print("0: " + str(start_len))

    sess_length_queue = deque()
    for t in time_range(time_res, max_wait, time_res):
        
        sleep(time_res)
        sess_len = len(sess.body())
        sess_length_queue.append(sess_len)   

        #print( str(t) + ": " + str(sess_len))

        if( len(sess_length_queue) > queue_length ): 
            sess_length_queue.popleft()  
        
        #
        # If all members of the queue are equal
        #
        if( all(x==sess_length_queue[0] for x in sess_length_queue) and 
            len(sess_length_queue) == queue_length):
            return t
    
    return -1


"""
Continuously scroll to the bottom of the page for a full minute, 
let the page reload and load the data from there.
"""
def infinite_scroll_to_bottom(sess, total_scroll_time=60, total_wait_time=20):

    last_size = len(sess.body())
    
    for t in time_range(0, total_scroll_time, 1):
        script = "window.scrollBy(0,1000);"
        sess.exec_script(script)
        this_size = len(sess.body()) 
        
        if( this_size != last_size ):
            script = "window.scrollTo(0,0);"
            sess.exec_script(script)
            sleep(5)
            last_size = this_size
            
        sess.render(str(t) + ".png")
        sleep(1)

    sleep(total_wait_time)

    wait = wait_until_session_stable(sess,queue_length = total_wait_time)
    this_size = len(sess.body()) 
    sess.render(str(total_scroll_time) + ".png")
#        if( this_size == last_size ) :
#            break
#        i += 1
#       last_size = this_size
        
            
def time_range(start, end, step):
    while start <= end:
        yield start
        start += step

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
