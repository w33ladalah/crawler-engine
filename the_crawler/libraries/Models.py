from sqlobject import SQLObject
from the_crawler.libraries.connection import conn

__connection__ = conn

class EngineCrawledContents(SQLObject):
    class sqlmeta:
        fromDatabase = True
        table = 'engine_crawled_contents'
        
    
class EnginePopularContents(SQLObject):
    class sqlmeta:
        fromDatabase = True
        table = 'engine_popular_contents'