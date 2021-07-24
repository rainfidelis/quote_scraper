import scrapy
from ..items import QuotesScraperBotItem

class QuotesSpider(scrapy.Spider):

    name = 'quotes'
    
    start_urls = [
        'http://quotes.toscrape.com/'
        ]

    def parse(self, response):
        items = QuotesScraperBotItem()

        all_quotes = response.css('div.quote')
        
        for div in all_quotes:
            quote = div.css('.text::text').extract()
            authors = div.css('.author::text').extract()
            tags = div.css('.tags a::text').extract()

            items['quote'] = quote
            items['author'] = authors
            items['tags'] = tags

            yield items

        next_page = response.css('.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)