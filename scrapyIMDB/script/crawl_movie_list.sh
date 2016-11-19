#!/bin/bash

#usage: crawl_movie_list.sh {years}
#ex: sh crawl_movie_list.sh 2015,2014,2013,2012,2011

years=$1

cd  ..

scrapy crawl movie_list -a crawlYears=${years} --set FEED_URI=data/movie_list.csv --set FEED_FORMAT=csv
