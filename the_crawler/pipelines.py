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
            summary = self._get_summary(self._sanitize_html(item['content']).strip())
            item['title'] = self._sanitize_html(item['title']).strip()
            item['content'] = self._sanitize_html(item['content']).strip()
            item['summary'] = summary['summary']
            item['content_word_count'] = summary['original_word_count']
            item['summary_word_count'] = summary['summary_word_count']

            if item['content'] == '':
                raise DropItem(item['url'])
            else:
                return item
        except KeyError:
            raise DropItem(item['url'])

    def _get_summary(self, content):
        r = requests.post('http://engine.lintas.me:1421/rest/summarize', data={'content':content})
        return json.loads(r.text)

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

class PopularSuggestion:    
    def __init__(self, path, delay, article_old):
        self.path = path[0]
        self.delay = delay[0]
        self.max_old_article = article_old[0]
            
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.getlist('LAST_POPULAR_UPDATE_PATH'),
            crawler.settings.getlist('SET_POPULAR_DELAY'),
            crawler.settings.getlist('MAX_OLD_ARTICLE')
        )
    
    def process_item(self, item, spider):        
        return item
    
    def close_spider(self, spider):
        spider.log('%s - THE SPIDER IS CLOSED!' % spider.channel, log.DEBUG)
        
        last_update = self._read_last_update(spider.channel)
        current_delay = int(time.strftime('%s')) - last_update
                
        if current_delay > (int(self.delay) * 60):
            where_clause = AND(
                   EngineCrawledContents.q.popular == 0,
                   EngineCrawledContents.q.channel == spider.channel,
                   EngineCrawledContents.q.createdat > datetime.datetime.fromtimestamp(last_update).strftime('%Y-%m-%d %H:%M:%S'),
                   EngineCrawledContents.q.createdat < time.strftime('%Y-%m-%d %H:%M:%S')
                )
            non_popular_contents = EngineCrawledContents.select(where_clause)
            if non_popular_contents.count() > 0:
                total_time_diff = 0
                for non_popular_content in non_popular_contents:
                    total_time_diff += self._pubdate_time_diff(convert_datetime_to_unix_timestamp(str(non_popular_content.publishdate).replace('-', '/')))

                content_popularity = AutoVivification()
                for non_popular_content in non_popular_contents:  
                    content_tweet_count = int(non_popular_content.tweets)
                    content_time_diff = self._pubdate_time_diff(convert_datetime_to_unix_timestamp(str(non_popular_content.publishdate).replace('-', '/')))
                    popularity = self._calculate_popularity_score(content_tweet_count, content_time_diff, total_time_diff)
                    content_popularity[non_popular_content.domain][non_popular_content.id] = popularity
                
                for domain in content_popularity:
                    ids_per_domain = content_popularity[domain]
                    sort_by_tweets = sorted(ids_per_domain.iteritems(), key=operator.itemgetter(1), reverse=True)
                    
                    best_content_id = sort_by_tweets[:5]
                    
                    for content_id in best_content_id:
                        best_content = EngineCrawledContents.get(content_id[0])
                        content_data = self._get_json_content(spider, best_content.contentpath)

                        if(content_data != False):
                            if(len(content_data['image_urls']) > 0):
                                spider.log('Content ID %s is set to popular suggestions' % content_id[0], log.DEBUG)

                                try:
                                    lintas_content_id = self._post_to_lintas(spider, content_data)

                                    if(self._existing_popular_content(best_content.hash) == False and
                                               is_old_article(best_content.publishdate, self.max_old_article) == False and
                                               lintas_content_id != False):
                                        EnginePopularContents(
                                            sourceid=content_id[0],
                                            postid=lintas_content_id,
                                            domain=best_content.domain,
                                            channel=best_content.channel,
                                            title=best_content.title,
                                            url=best_content.url,
                                            publishdate=best_content.publishdate,
                                            tweets=best_content.tweets,
                                            hash=best_content.hash,
                                            popularity=float(content_popularity[domain][content_id[0]]),
                                            contentpath=best_content.contentpath,
                                            createdat=datetime.datetime.now(),
                                            status=1
                                        )
                                except ValueError:
                                    spider.log("No JSON object could be decoded", log.ERROR)

                            best_content.popular = 1
                    
            self._write_last_update(spider.channel)     
        else:
            pass

    def _existing_popular_content(self, hashed_title):
        existing_content = EnginePopularContents.select(AND(EnginePopularContents.q.hash == hashed_title))
        if existing_content.count() > 0:
            log.msg("Popular content already exists! Hash: %s" % hashed_title)
            return False
        else:
            log.msg("Popular content doesn't exists. Hash: %s" % hashed_title)
            return False

    def _set_to_popular_lintas(self, last_update, spider):
        where_clause = AND(
               EnginePopularContents.q.postid <> '',
               EnginePopularContents.q.status == 1,
               EnginePopularContents.q.channel == spider.channel,
               EnginePopularContents.q.createdat > datetime.datetime.fromtimestamp(last_update).strftime('%Y-%m-%d %H:%M:%S'),
               EnginePopularContents.q.createdat < time.strftime('%Y-%m-%d %H:%M:%S')
            )
        popular_contents = EnginePopularContents.select(where_clause)

    def _is_post_to_lintas(self):
        with codecs.open('/opt/engine.lintas.me/console/db/engine.json', 'r+', encoding='utf-8') as f:
            return True if json.load(f)['post_to_lintas'] == "yes" else False

    def _post_to_lintas(self, spider, content_json):
        url = "http://devel.lintas.me/rest/newPost"
        title = content_json['title']
        content = content_json['content']
        image = content_json['image_urls'][0]
        source_url = content_json['url']
        tag = content_json['channel']
        source_channel = self._channel_to_id(content_json['channel'])
        thumbnail = self._set_thumbnail(image)
        try:
            summary = content_json['summary']
        except KeyError:
            summary = ""

        payload = {
            'is_backecd': 1,
            'origin_id': source_channel,
            'url': source_url,
            'post_title': title,
            'post_content': content,
            'post_img_url': image,
            'post_tag_no_auto': tag,
            'kind': 'article',
            'backecd_user': '51763a7d1b971a5c2000038f',
            'rand_user': self._random_user(),
            'local_thumbnail_url': thumbnail['result']['original'],
            'post_summarize': summary,
            'post_summarize_persen': 40
            # 'local_thumbnail_info': thumbnail['info']
        }

        # r = requests.post(url, data=payload)
        # response = json.loads(r.text)

        # return response['detail_post']['id'] if response['status'] == 'OK' else False
        return json.dumps(payload)

    def _get_json_content(self, spider, content_path):
        json_url = 'http://engine.lintas.me/%s' % content_path
        r = requests.get(json_url)
        if(r.status_code == 200):
            return json.loads(r.text)
        else:
            return False

    def _channel_to_id(self, channel_name):
        channel = {
            'news': '4d82a1d57205fb674a00003a',
            'otomotif': '4d82a1d47205fb674a00002e',
            'woman': '4d82a1d17205fb674a000005',
            'tech': '4d82a1d47205fb674a000032',
            'bola': '4d82a1d37205fb674a000023'
        }
        return channel[channel_name]

    def _random_user(self):
        r = requests.get('http://www.lintas.me/rest/getRandomUser')
        return json.loads(r.text)[0]['id']

    def _set_thumbnail(self, image_url):
        r = requests.get('http://di.lintas.me/upload?url=%s' % image_url)
        return json.loads(r.text)

    def _calculate_popularity_score(self, tweets, publish_date_diff, total_publish_date_diff):
        distribution = total_publish_date_diff / publish_date_diff
        new_distribution = 1 if distribution == 0 else distribution
        return float((new_distribution * tweets) / 100)

    def _pubdate_time_diff(self, pubdate):
        return int(time.time() - pubdate)

    def _read_last_update(self, channel):
        try:
            fr = open("%s/%s_last_popular_update" % (self.path, channel), "r")
            last_timestamp = fr.read()
            fr.close()
            
            return int(last_timestamp)
        except ValueError:
            return 0
        except IOError:
            return 0
        
    def _write_last_update(self, channel):
        fw = open("%s/%s_last_popular_update" % (self.path, channel), "wb")
        fw.write(time.strftime("%s"))
        fw.close()
