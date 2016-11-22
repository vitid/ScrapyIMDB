#!/bin/bash

#usage: crawl_reviews.sh {titleId} [{maxCharLength}]
#ex: sh crawl_reviews.sh tt0418279 1100

titleId=$1
maxCharLength=$2

cd ..

scrapy crawl reviews -o data/reviews_${titleId}.json -a titleId=${titleId} -a maxCharLength=${maxCharLength}