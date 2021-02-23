import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from heritagech.items import Article


class HeritagechSpider(scrapy.Spider):
    name = 'heritagech'
    start_urls = ['https://www.heritage.ch/en/news']

    def parse(self, response):
        links = response.xpath('//div[@class="news-slide all-posts"]//div[@class="card"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//p[@class="title article-8 white-text"]//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="text-5"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="news-content col-12 col-lg-8"]//p/text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[:-1]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
