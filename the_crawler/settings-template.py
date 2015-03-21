import time

BOT_NAME = 'lintasengine'

SPIDER_MODULES = ['the_crawler.spiders']
NEWSPIDER_MODULE = 'the_crawler.spiders'
DEPTH_LIMIT = 1
DOWNLOAD_DELAY = 0.30  # 300ms
AJAXCRAWL_ENABLED = True
REDIRECT_ENABLED = True
DOWNLOAD_TIMEOUT = 30
# RETRY_ENABLED = False
CONCURRENT_REQUESTS = 1

DOWNLOADER_MIDDLEWARES = {
    'the_crawler.middleware.RandomUserAgent': 1,
    'the_crawler.middleware.ErrorMonkeyMiddleware': 2,
}

ITEM_PIPELINES = {
    'the_crawler.pipelines.CheckDuplicateAndOldArticle': 2,
    'the_crawler.pipelines.CleanHTML': 1,
    'the_crawler.pipelines.ImageDownloader': None,
    'the_crawler.pipelines.CheckTweets': 4,
    'the_crawler.pipelines.SaveResults': 5,
    'the_crawler.pipelines.SaveResultsJSON': 6,
}

DB_HOST = "YOUR_VALUE_HERE"
DB_NAME = "YOUR_VALUE_HERE"
DB_USER = "YOUR_VALUE_HERE"
DB_PASS = "YOUR_VALUE_HERE"

THIS_MONTH = time.strftime("%Y-%m")
ENGINE_PATH = ""
LAST_POPULAR_UPDATE_PATH = "/tmp"
SITE_CONFIG_PATH = ""
BASE_CONTENT_PATH = ""
CRAWLED_CONTENT_PATH = "%s/data" % BASE_CONTENT_PATH
SET_POPULAR_DELAY = 60
MAX_OLD_ARTICLE = 5
SET_POPULAR_ARTICLE = 1

IMAGES_STORE = "%s/image" % BASE_CONTENT_PATH
IMAGES_MIN_HEIGHT = 200
IMAGES_MIN_WIDTH = 250

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

MONTH_DICTIONARY = {
    '01': '01',
    'January': '01',
    'Januari': '01',
    'Jan': '01',

    '02': '02',
    'February': '02',
    'Pebruari': '02',
    'Februari': '02',
    'Peb': '02',
    'Feb': '02',

    '03': '03',
    'March': '03',
    'Maret': '03',
    'Mar': '03',

    '04': '04',
    'April': '04',
    'Apr': '04',

    '05': '05',
    'May': '05',
    'Mei': '05',

    '06': '06',
    'June': '06',
    'Juni': '06',
    'Jun': '06',

    '07': '07',
    'July': '07',
    'Juli': '07',
    'Juli': '07',

    '08': '08',
    'August': '08',
    'Agustus': '08',
    'Ags': '08',
    'Aug': '08',

    '09': '09',
    'September': '09',
    'Sep': '09',
    'Sept': '09',

    '10': '10',
    'October': '10',
    'Oktober': '10',
    'Okt': '10',
    'Oct': '10',

    '11': '11',
    'November': '11',
    'Nov': '11',

    '12': '12',
    'December': '12',
    'Desember': '12',
    'Des': '12',
    'Dec': '12',
}

try:
    from local_settings import *
except ImportError:
    pass
