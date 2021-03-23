import scrapy

class QuotesSpiderCSS(scrapy.Spider):
    name = "quotes-css"
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall()
            }
        
        for a in response.css('ul.pager a'):
            yield response.follow(a, callback=self.parse)