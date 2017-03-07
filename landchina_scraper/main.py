# !/usr/bin/env python
# -*- coding: utf-8 -*-    # import system default encoding
from __future__ import print_function,unicode_literals    # import features of Python 3


# import my own modules
from LandChinaPageScraper import LandChinaPageScraper
from geventQueue import ScraperGeventQueue


def main():
    scrapers = ScraperGeventQueue(LandChinaPageScraper)
    scrapers.start()
    
    
main()