from sqlobject.mysql import builder
from the_crawler.settings import DB_HOST, DB_NAME, DB_PASS, DB_USER

conn = builder()(user=DB_USER, password=DB_PASS, host=DB_HOST, db=DB_NAME)