from hgext.zeroconf import publish
from mercurial.revset import public
from scrapy import log

import hashlib, time, datetime

'''
Created on Aug 7, 2014

@author: hendro
'''

def generate_hash(string):
    md5hash = hashlib.md5()
    md5hash.update(string)
    
    return md5hash.hexdigest()

def convert_datetime_to_unix_timestamp(date_string, format="%Y/%m/%d %H:%M"):
    try:
        return int(time.mktime(datetime.datetime.strptime(date_string[:16], format).timetuple()))
    except ValueError:
        return 0

def convert_unix_timestamp_to_datetime(unix_timestamp):
    return datetime.datetime.fromtimestamp(float(unix_timestamp))

def is_old_article(publish_date, max_old_article=5):
        max_expire = max_old_article
        now = int(time.time())
        pubdate_diff = int((now - int(publish_date)) / 24 / 60 / 60)

        # log.msg("Now : %s" % str(now))
        # log.msg("Publish Date : %s" % str(publish_date))
        # log.msg("Max Expire: %s" % str(max_expire))
        # log.msg("Publish Diff: %s" % (pubdate_diff))
        # log.msg(str(convert_unix_timestamp_to_datetime(publish_date)))

        if(pubdate_diff > max_expire):
            log.msg("Is old article")
            return True
        return False