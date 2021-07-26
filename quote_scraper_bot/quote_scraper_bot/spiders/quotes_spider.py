import scrapy
from scrapy.http import FormRequest
# from scrapy.utils.response import open_in_browser 
# # used to confirm a page loaded successfully directly from the browser


from ..items import QuoteScraperBotItem

class QuotesSpider(scrapy.Spider):

    name = 'quotes'
    
    start_urls = [
        'http://quotes.toscrape.com/login'
        ]

    def parse(self, response):
        
        token = response.css('form input::attr(value)') .extract()
        return FormRequest.from_response(response, formdata={
            'token': token, 
            'username': 'spacesng@gmail.com',
            'password': 'rainfast'
        }, callback=self.scraper)
        
    
    def scraper(self, response):
        items = QuoteScraperBotItem()

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
            yield response.follow(next_page, callback=self.scraper)