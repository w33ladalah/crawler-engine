from urlparse import urlparse

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request, Response
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

from the_crawler.items import ContentAttributes
from the_crawler.libraries.helpers import convert_datetime_to_unix_timestamp
from the_crawler.settings import SITE_CONFIG_PATH, MONTH_DICTIONARY

import re

class TheCrawler(Spider):

    name = 'TheCrawlerEngineV1'

    def __init__(self, **kw):
        super(TheCrawler, self).__init__(**kw)
        
        self.channel = kw.get('channel')
        self.domain = kw.get('domain')
        
        full_config_path = '%s%s' % (SITE_CONFIG_PATH, self.channel)
        
        self.config_path = "%s/%s.txt" % (full_config_path, self.domain)
        self.config_items = self._parse_config(self.config_path)
        
        try:
            self.url = self.config_items['start_url']
        except KeyError:
            self.url = 'http://%s/' % self.domain
            
        try:
            self.link_extractor = LxmlLinkExtractor(restrict_xpaths=self.config_items['crawl_areas'], unique=True)
        except KeyError:
            self.link_extractor = LxmlLinkExtractor(unique=True)
                        
        self.real_domain = urlparse(self.url).hostname.lstrip('www.')
        self.allowed_domains = [urlparse(self.url).hostname.lstrip('www.')]
        
        self.cookies_seen = set()
        
    def start_requests(self):
        return [Request(self.url, callback=self.parse)]

    def parse(self, response):
        page = self._get_item(response)
        r = [page]
        r.extend(self._extract_requests(response))
        return r

    def _get_item(self, response):        
        item = ContentAttributes(
            url=response.url,
            size=str(len(response.body)),
            referer=response.request.headers.get('Referer')
        )

        self._set_content_data(item, response)
        self._set_new_cookies(item, response)
        
        return item

    def _extract_requests(self, response):
        r = []
        if isinstance(response, Response):
            links = self.link_extractor.extract_links(response)
            r.extend(Request(x.url, callback=self.parse) for x in links)
        return r

    def _set_content_data(self, page, response):
        if isinstance(response, Response):
            title = Selector(response).xpath(self.config_items['title']).extract()
            content = Selector(response).xpath(self.config_items['body']).extract()
            
            try:
                published_date = Selector(response).xpath(self.config_items['publish_date']).extract()
            except KeyError:
                published_date = None
            
            try:
                images = Selector(response).xpath(self.config_items['image']).extract()
            except KeyError:
                images = Selector(response).xpath('%s//img/@src' % self.config_items['body']).extract()

            image_urls = []
            for img_url in images:
                image_url_hostname = urlparse(img_url).hostname   
                image_url_scheme = urlparse(img_url).scheme
                
                if image_url_hostname is None:
                    img_url = "http://%s%s" % (self.real_domain, img_url)
                    
                if image_url_scheme is None:
                    img_url = "http://%s" % img_url
                    
                image_urls.append(img_url)
                        
            if title:
                page['title'] = title[0]
                
            if content:
                page['content'] = content[0]

            pubdate = 0
            if published_date is not None:
                if published_date:
                    day_pattern = self.config_items['publish_date_day_pattern']
                    month_pattern = self.config_items['publish_date_month_pattern']
                    year_pattern = self.config_items['publish_date_year_pattern']
                    time_pattern = self.config_items['publish_date_time_pattern']
                    
                    pubdate = self._translate_publish_date_to_timestamp(published_date[0], day_pattern, month_pattern, year_pattern, time_pattern)
            
            page['publish_date'] = str(pubdate)
            page['image_urls'] = image_urls 
            page['channel'] = self.channel
            page['domain'] = self.real_domain
        
    def _set_new_cookies(self, page, response):
        cookies = []
        for cookie in [x.split(';', 1)[0] for x in response.headers.getlist('Set-Cookie')]:
            if cookie not in self.cookies_seen:
                self.cookies_seen.add(cookie)
                cookies.append(cookie)
        if cookies:
            page['newcookies'] = cookies
            
    def _parse_config(self, filename):
        config = {}
        f = open(filename, 'r')

        for line in f.readlines():
            config_per_line = line.split(': ')
            if len(config_per_line) > 1:
                if config_per_line[0] != 'test_url':
                    config[config_per_line[0]] = config_per_line[1].rstrip()

                if config_per_line[0] == 'publish_date_time_pattern':
                    config[config_per_line[0]] = ':'.join(config_per_line[1:]).rstrip()
        f.close()
        
        return config
    
    def _translate_publish_date_to_timestamp(self, pubdate, day_pattern, month_pattern, year_pattern, time_pattern):
        try:
            re_day = re.compile(day_pattern)
            re_month = re.compile(month_pattern)
            re_year = re.compile(year_pattern)
            re_time = re.compile(time_pattern)

            try:
                day = re_day.findall(pubdate)[0]
            except IndexError:
                day = "00"

            try:
                month = re_month.findall(pubdate)[0].lower()
            except IndexError:
                month = "00"

            try:
                year = re_year.findall(pubdate)[0]
            except IndexError:
                year = "0000"

            try:
                parsed_time = re_time.findall(pubdate)[0]
            except IndexError:
                parsed_time = "00:00"
            try:
                pubdate_timestamp = convert_datetime_to_unix_timestamp("%s/%s/%s %s" % (year, MONTH_DICTIONARY["%s%s" % (month[0].upper(), month[1:])], day, parsed_time))
            except KeyError:
                pubdate_timestamp = 0
            
            return pubdate_timestamp
        except AttributeError:
            return 0
