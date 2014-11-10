# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ContentAttributes(Item):
    domain = Field()
    title = Field()    
    author = Field()
    date = Field()
    content = Field()
    summary = Field()
    publish_date = Field()
    publish_date_time_diff = Field()
    tags = Field()
    channel = Field() 
    images = Field()
    image_urls = Field()
    image_paths = Field()
    url = Field()
    tweets = Field()
    popularity = Field()
    file_path = Field()
    referer = Field()
    size = Field()
    hash = Field()
    newcookies = Field()
    content_word_count = Field()
    summary_word_count = Field()