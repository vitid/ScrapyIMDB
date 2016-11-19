#!/bin/bash

#usage: crawl_reviews.sh {titleId}
#ex: sh crawl_reviews.sh tt0418279

titleId=$1

cd ..

scrapy crawl reviews -o data/reviews_${titleId}.json -a titleId=${titleId}