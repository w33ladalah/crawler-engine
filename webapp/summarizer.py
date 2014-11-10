# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

__author__ = 'hendro'

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from string import punctuation
from tornado.web import RequestHandler
import re

class SummarizeContent(RequestHandler):
    LANGUAGE = "czech"

    def set_default_headers(self):
        self.set_header("Server", "LintasSummarizerAPIServer/0.1")
        self.set_header("Access-Control-Allow-Origin", "*")

    def post(self):
        try:
            content = self._clean_text(self.get_argument('content'))
            length = self.get_argument('length', '50')
            length_type = self.get_argument('length_type', 'percent')
            content_words = self._word_counter(content)

            if length_type == 'percent':
                sentence_length = length + "%"
            else:
                if int(length) <= content_words:
                    sentence_length = str(int((int(length) / content_words) * 100)) + "%"
                else:
                    sentence_length = '100%'

            parser = PlaintextParser.from_string(content, Tokenizer(self.LANGUAGE))
            stemmer = Stemmer(self.LANGUAGE)
            summarizer = Summarizer(stemmer)
            summarizer.stop_words = get_stop_words(self.LANGUAGE)
            summarized = summarizer(parser.document, sentence_length)

            summary = ""
            for sentence in summarized:
                summary += "%s\n\n" % self._sentence(sentence)

            response = {
                'summary': summary,
                'summary_word_count': self._word_counter(summary),
                'original_word_count': content_words
            }
        except ZeroDivisionError:
            response = {
                'summary': "",
                'summary_word_count': 0,
                'original_word_count': 0
            }

        self.write(response)

    def _sentence(self, sentence):
        return str(sentence).decode('utf-8')

    def _clean_text(self, text):
        regex_patterns = [
            '^([\w\.]+,\s[\w]+\s\-\s)',
            '^([\w]+,\s[\w\.]+\s\-\s)',
            '^([\w]+\s\-\s)'
        ]
        # regex = re.compile("\w\s[\-|\—|\,]\s([\w\s\S]+)")
        return text # .decode('latin9').encode('utf8')
        # regex.findall(text)[0]

    def _word_counter(self, text):
        r = re.compile(r'[{}]'.format(punctuation))
        new_str = r.sub(' ', text)
        return len(new_str.split())