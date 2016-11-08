#!/bin/bash

#usage: runCrawler.sh {titleId}
#ex: sh runCrawler.sh tt0418279

titleId=$1

cd ..

scrapy crawl reviews -o data/reviews_${titleId}.json -a titleId=${titleId}