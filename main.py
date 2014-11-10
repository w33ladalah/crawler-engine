import sys, getopt

from twisted.internet import reactor

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

from os import listdir
from os.path import isfile, join, splitext

from the_crawler.spiders.lintasengine import LintasEngine
from the_crawler.settings import SITE_CONFIG_PATH

def setup_crawler(channel, domain):
    spider = LintasEngine(channel=channel, domain=domain)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure() 
    crawler.crawl(spider)
    crawler.start()
    
def main(argv):
    if len(sys.argv) == 1:
        raise getopt.GetoptError
    
    try:
        opts, args = getopt.getopt(argv, "c:")
        config_path = SITE_CONFIG_PATH
        for opt, arg in opts:
            cfg_path = config_path + arg
            channel = arg
            domains = [ splitext(f)[0] for f in listdir(cfg_path) if isfile(join(cfg_path, f)) ]
            for domain in domains:
                setup_crawler(channel, domain)      
                
        log.start()
        reactor.run()  # the script will block here until the spider_closed signal was sent   
    except getopt.GetoptError:
        print 'main.py -c <channel>'
        sys.exit(2)
    
if __name__ == "__main__":
    main(sys.argv[1:])
