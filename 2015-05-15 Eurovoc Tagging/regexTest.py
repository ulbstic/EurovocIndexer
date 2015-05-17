#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os, csv, re, nltk
from nltk.stem.snowball import SnowballStemmer # il est disponible en de nobmreuses langues

text = "The guideline does not cover the photostability of drugs administration after administrations (i.e. under conditions of use) and those applications not covered by the Parent Guideline."

regex = r"(administr\w{0,5})(\W)"




print(re.sub(regex, r"<:>\1</:>\2", text))

