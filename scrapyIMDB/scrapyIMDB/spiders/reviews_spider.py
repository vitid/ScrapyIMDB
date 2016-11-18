import scrapy

class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    pageNum = 0
    MAX_PAGE_NUM = -1
    MAX_CHAR_LENGTH = 1100
    MAX_NUM_COLLECT = 100
    numCollect = 0
    #titleId -> parsed by script's argument
    urlTemplate = "http://www.imdb.com/title/{title_id}/reviews?start={start_num}"

    def start_requests(self):
        self.titleId = getattr(self,'titleId',None)
        yield scrapy.Request(url=self.getCurrentUrl(), callback=self.parse)

    def getCurrentUrl(self):
        return self.urlTemplate.replace("{title_id}",self.titleId).replace("{start_num}",str(self.pageNum * 10))

    def parse(self, response):

        reviews = response.xpath("//layer/div[4]/div[3]/div[3]/div[3]/p").extract()
        # this indicates that no more review to crawl, terminate the program
        if(len(reviews) <= 1):
            return
        # Exclude the last one because it is a link to 'Add another review'
        for review in reviews[0:len(reviews)-1]:
            if(len(review) > self.MAX_CHAR_LENGTH):
                continue

            self.numCollect += 1
            yield{
                #strip <p>...</p> tag
                'review': review[3:-4]
            }
        self.pageNum += 1
        # stop if the crawling limit is reached
        if (self.MAX_PAGE_NUM!=-1 and self.pageNum > self.MAX_PAGE_NUM):
            return
        # stop if collecting enough reviews
        if (self.MAX_NUM_COLLECT != -1 and self.numCollect >= self.MAX_NUM_COLLECT):
            return
        # crawl the next page
        yield scrapy.Request(url=self.getCurrentUrl(), callback=self.parse)
