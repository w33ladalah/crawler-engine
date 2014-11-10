# -*- coding: utf-8 -*-
__author__ = 'hendro'

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from string import punctuation

import re

class ContentSummarizer():
    LANGUAGE = "czech"
    SUMMARY = ""
    WORD_COUNT = 0
    SUMMARY_COUNT = 0

    def __init__(self, content):
        sentence_length = '50%'
        parser = PlaintextParser.from_string(content, Tokenizer(self.LANGUAGE))
        stemmer = Stemmer(self.LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(self.LANGUAGE)
        summarized = summarizer(parser.document, sentence_length)

        for sentence in summarized:
            self.SUMMARY += "%s\n\n" % self._sentence(sentence)

        self.WORD_COUNT = self._word_counter(content)
        self.SUMMARY_COUNT = self._word_counter(self.SUMMARY)

    def get_summary(self):
        return self.SUMMARY

    def get_word_count(self):
        return self.WORD_COUNT

    def get_summary_word_count(self):
        return self.SUMMARY_COUNT

    def _sentence(self, sentence):
        return str(sentence).decode('utf-8')

    def _clean_text(self, text):
        # regex_patterns = [
        #     '^([\w\.]+,\s[\w]+\s\-\s)',
        #     '^([\w]+,\s[\w\.]+\s\-\s)',
        #     '^([\w]+\s\-\s)'
        # ]
        # regex = re.compile("\w\s[\-|\—|\,]\s([\w\s\S]+)")
        # regex.findall(text)[0]
        return text

    def _word_counter(self, text):
        r = re.compile(r'[{}]'.format(punctuation))
        new_str = r.sub(' ', text)
        return len(new_str.split())