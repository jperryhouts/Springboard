import scrapy

CLASS_SELECTOR="//div[contains(concat(' ', normalize-space(@class), ' '), ' {} ')]"
TEXT_SELECTOR="descendant-or-self::{}[@class and contains(concat(' ', normalize-space(@class), ' '), ' {} ')]/text()"
TAGS_SELECTOR="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' tags ')]" \
            + "/descendant-or-self::*/a[@class and contains(concat(' ', normalize-space(@class), ' '), ' tag ')]/text()"
PAGE_SELECTOR="descendant-or-self::ul[@class and contains(concat(' ', normalize-space(@class), ' '), ' pager ')]" \
            + "/descendant-or-self::*/a"

class QuotesSpiderXPATH(scrapy.Spider):
    name = "quotes-xpath"
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        for quote in response.xpath(CLASS_SELECTOR.format('quote')):
            yield {
                'text': quote.xpath(TEXT_SELECTOR.format('span','text')).get(),
                'author': quote.xpath(TEXT_SELECTOR.format('small','author')).get(),
                'tags': quote.xpath(TAGS_SELECTOR).getall()
            }
        
        for a in response.xpath(PAGE_SELECTOR):
            yield response.follow(a, callback=self.parse)
