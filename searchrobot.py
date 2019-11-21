#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import wikipedia as wiki
from nltk import tokenize
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

def error(string):
    print(string)
    sys.stdout.flush()
    input()
    exit(1)

class SearchRobot:

    def __init__(self):
        self.keywords_list = []
        self.sentences_number = 7

        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
                version="2018-11-16",
                iam_apikey="FQCBVugo5oTut94tU9JmzdIsvOetx1g3tMBWVRs8aYNN",
                url="https://gateway.watsonplatform.net/natural-language-understanding/api")

    def search(self, search_term):
        wiki.set_lang("pt")

        try:
            summary = wiki.summary(search_term, sentences=7)
            summary = re.sub(r"\([^)]*\)", "", summary)
        except wiki.exceptions.HTTPTimeoutError:
            error("Couldn't download Wikipedia due to HTTP Transfer errors.")
        except wiki.exceptions.PageError:
            error("Couldn't find term in Wikipedia. Try being more specific.")

        return tokenize.sent_tokenize(summary)

    def get_keywords(self, sentences):
        for sentence in sentences:
            try:
                response = self.natural_language_understanding.analyze(text=sentence,
                        features=Features(
                            keywords = KeywordsOptions(emotion = False, sentiment = False,
                                limit = 2))).get_result()
            except:
                print("Not enough text in summary. Press any key to close.")
                error()
                
            temp_list = []
            for keyword in response["keywords"]:
                temp_list.append(keyword["text"])

            self.keywords_list.append(temp_list)

        return self.keywords_list
