import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import HheartlandnzItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BlogSpider(scrapy.Spider):
    name = 'blog'
    start_urls = ['https://www.heartland.co.nz/business-loans/blog']

    def parse(self, response):
        post_links = response.xpath(
            '//a[@class="btn btn-seniors-green-outline btn-seniors-green-outline--thick mt-auto btn-heartland-sf-news-item"]/@href').getall()
        yield from response.follow_all(post_links, self.parse_post)

    def parse_post(self, response):
        date = "Not stated in article"
        title = response.xpath('//h2[@class="news-item__title"]/text()').get()
        content = response.xpath('//div[@class="news-item__wrapper mt-0"]//text()').getall()
        content = [p.strip() for p in content if p.strip()]
        content = re.sub(pattern, "", ' '.join(content))

        item = ItemLoader(item=HheartlandnzItem(), response=response)
        item.default_output_processor = TakeFirst()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('date', date)

        yield item.load_item()
