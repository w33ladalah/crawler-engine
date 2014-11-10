# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

__author__ = 'hendro'

from library.regression import lm_independent_variable, lm_dependent_variable
from tornado.web import RequestHandler
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, TWITTER_COUNT_URL
import pandas as pd
import pandas.io.sql as psql
import requests
import MySQLdb
import time, datetime

class Prediction(RequestHandler):
    mysql_cn = None

    def set_default_headers(self):
        self.set_header("Server", "LintasPredictiveAnalyticServer/0.1")
        self.set_header("Access-Control-Allow-Origin", "*")

    def post(self):
        now = time.time()
        start =datetime.datetime.fromtimestamp(now - (30 * 24 * 3600)).strftime('%Y-%m-%d')
        finish = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d')

        post_count = int(self.get_argument('post_count', 0))
        tw_post = int(self.get_argument('tw_post', post_count))
        start_date = self.get_argument('start_date', start)
        finish_date = self.get_argument('finish_date', finish)

        prediction_tw = self._prediction_by_twitter(tw_post, start_date, finish_date)

        response = prediction_tw
        
        self.write(response)

    def _db_connect(self):
        self.mysql_cn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        return self.mysql_cn

    def _db_close(self):
        self.mysql_cn.close()

    def _prediction_by_twitter(self, post_count, start_date, finish_date):
        sql = "SELECT `date`, SUM(pageviews) total_pv, SUM(sessions) total_sessions, SUM(uniquePageviews) total_unq_pv " \
              "FROM lintaszone.z_report_ga_ref_hour WHERE userType LIKE 'Returning%' AND page = 'all' AND " \
              "socialNetwork = 'Twitter' AND `date` BETWEEN '{}' AND '{}' GROUP BY `date`;".format(start_date, finish_date)

        df_mysql = psql.read_sql(sql, con=self._db_connect())
        self._db_close()

        tweets_counter_url = TWITTER_COUNT_URL.format(start_date, finish_date)
        r = requests.get(tweets_counter_url)

        tw_counter = [c['data']['tweets'] for c in r.json()['data']]
        dt_counter = [c['date'] for c in r.json()['data']]
        df_twitter = pd.DataFrame({'date':dt_counter, 'tweets':tw_counter})
        df_merged = pd.merge(df_mysql, df_twitter, left_index=True, right_index=True, how='outer')

        predicted_sessions = int(lm_independent_variable(post_count, 'total_sessions', df_merged))
        predicted_unique_pv = int(lm_independent_variable(post_count, 'total_unq_pv', df_merged))
        predicted_pv = int(lm_dependent_variable(predicted_sessions, predicted_unique_pv, post_count, df_merged))

        results = {
            'sessions': predicted_sessions,
            'unique_pv': predicted_unique_pv,
            'pv': predicted_pv
        }

        return results