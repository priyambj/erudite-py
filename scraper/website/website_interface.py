from __future__ import print_function
import abc


class WebsiteInterface(object):
    def __init__(self):
        self.name = 'Abstract Interface'

    @abc.abstractmethod
    def can_handle(self, url):
        pass

    @abc.abstractmethod
    def scrape(self, url):
        pass