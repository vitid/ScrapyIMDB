#script to crawl reviews of all movies in data/movie_list.csv

import pandas as pd
import subprocess

CSV_FILE = "../data/movie_list.csv"

csvFile = pd.read_csv(CSV_FILE)

for index,titleId in enumerate(csvFile["titleId"]):
    print("processing index:{}...".format(index))
    subprocess.call(['./crawl_reviews.sh',titleId])
