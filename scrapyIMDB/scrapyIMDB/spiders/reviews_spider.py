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
        self.MAX_CHAR_LENGTH = int(getattr(self,'maxCharLength','')) if len(getattr(self,'maxCharLength','')) > 0 else self.MAX_CHAR_LENGTH
        yield scrapy.Request(url=self.getCurrentUrl(), callback=self.parse)

    def getCurrentUrl(self):
        return self.urlTemplate.replace("{title_id}",self.titleId).replace("{start_num}",str(self.pageNum * 10))

    def parse(self, response):

        content = response.xpath("//div[@id='tn15content']")[0]

        headers = content.xpath("div[not(@id)]")
        reviews = content.xpath("p").extract()
        # this indicates that no more review to crawl, terminate the program
        if(len(reviews) <= 1):
            return

        for index in range(0,len(headers)):
            if headers[index].xpath("img/@alt").extract_first() == None:
                #no score is given for this review
                continue

            review = reviews[index]
            if (len(review) > self.MAX_CHAR_LENGTH):
                continue

            score = headers[index].xpath("img/@alt").extract_first().split("/")[0]
            self.numCollect += 1
            yield {
                # strip <p>...</p> tag
                'review': review[3:-4],
                'score': score
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
