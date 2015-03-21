# -*- coding: utf-8 -*-

"""
Crawler Pipelines
"""

__author__ = 'hendro'

from the_crawler.libraries.Models import EngineCrawledContents, EnginePopularContents
from the_crawler.libraries.AutoVivification import AutoVivification
from the_crawler.libraries.helpers import generate_hash, convert_datetime_to_unix_timestamp, convert_unix_timestamp_to_datetime, is_old_article
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
from BeautifulSoup import BeautifulSoup
from sqlobject.sqlbuilder import AND

import scrapy, re, json, requests, urlparse, os, datetime, time, operator, codecs

class CheckDuplicateAndOldArticle(object):
    def __init__(self, content_path, article_old):
        self.content_path = content_path[0]
        self.max_old_article = article_old[0]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('CRAWLED_CONTENT_PATH'), crawler.settings.getlist('MAX_OLD_ARTICLE'))

    def process_item(self, item, spider):
        try:
            item['hash'] = generate_hash(item['title'])
            existing_content = EngineCrawledContents.select(AND(EngineCrawledContents.q.hash == item['hash']))

            if is_old_article(item['publish_date']) == True:
                raise DropItem("Old article! Drop it!")

            if existing_content.count() > 0:
                raise DropItem("Found duplicate item! Drop it!")

            return item
        except KeyError:
            raise DropItem("Error processing content from %s" % item['url'])

class CleanHTML(object):
    def process_item(self, item, spider):
        try:
            item['title'] = self._sanitize_html(item['title']).strip()
            item['content'] = self._sanitize_html(item['content']).strip()

            if item['content'] == '':
                raise DropItem(item['url'])
            else:
                return item
        except KeyError:
            raise DropItem(item['url'])

    def _sanitize_html(self, html):
        pattern = re.compile(r"<!\s*--(.*?)(--\s*\>)", re.DOTALL | re.MULTILINE | re.IGNORECASE)
        soup = BeautifulSoup(html)

        for tag in soup.findAll(True):
            tag.hidden = True

        content = soup.renderContents()

        return pattern.sub('', content)

class ImageDownloader(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

class CheckTweets:
    def process_item(self, item, spider):
        item['tweets'] = self._check_tweets_count(item['url'])

        return item

    def _check_tweets_count(self, url):
        try:
            cleaned_url = self._clean_url(url)

            log.msg('Check tweets count of URL: %s.' % cleaned_url, log.INFO)

            tweets_check_url = 'http://urls.api.twitter.com/1/urls/count.json?url=%s' % cleaned_url
            r = requests.get(tweets_check_url)
            tweet_count = r.json()

            return tweet_count['count']
        except requests.exceptions.ConnectionError:
            return 0

    def _clean_url(self, url, keep_params=('ID=',)):
        parsed = urlparse.urlsplit(url)
        filtered_query = '&'.join(qry_item for qry_item in parsed.query.split('&') if qry_item.startswith(keep_params))

        return urlparse.urlunsplit(parsed[:3] + (filtered_query,) + parsed[4:])

class SaveResults(object):
    def __init__(self, this_month):
        self.this_month = this_month[0]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('THIS_MONTH'))

    def process_item(self, item, spider):
        file_path = u'contents/%s/data/%s.json' % (self.this_month, item['hash'])

        spider.log(str(datetime.datetime.now()), log.INFO)
        spider.log(str(convert_unix_timestamp_to_datetime(time.time())), log.INFO)

        EngineCrawledContents(
            domain=item['domain'],
            channel=item['channel'],
            title=item['title'],
            url=item['url'],
            tweets=item['tweets'],
            publishdate=convert_unix_timestamp_to_datetime(float(item['publish_date'])),
            contentpath=file_path,
            hash=item['hash'],
            createdat=datetime.datetime.now()
        )

        return item

class SaveResultsJSON(object):
    def __init__(self, cfg_path):
        self.cfg_path = cfg_path[0]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('CRAWLED_CONTENT_PATH'))

    def process_item(self, item, spider):
        if not os.path.exists(self.cfg_path):
            os.makedirs(self.cfg_path)
        file_content = open('%s/%s.json' % (self.cfg_path, item['hash']), 'wb')
        line = json.dumps(dict(item))
        file_content.write(line)

        return item

