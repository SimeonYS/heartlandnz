import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import HheartlandnzItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class HheartlandnzSpider(scrapy.Spider):
	name = 'heartlandnz'
	start_urls = ['https://www.heartland.co.nz/about-us/news']

	def parse(self, response):
		articles = response.xpath('//div[@class="card-body"]')
		for article in articles:
			date = article.xpath('.//p//small/text()').get().split(' by')[0]
			post_links = article.xpath('.//a/@href').get()
			yield response.follow(post_links, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h2[@class="news-item__title"]/text()').get()
		content = response.xpath('//article[@class="news-item__wrapper"]//text()[not(ancestor::h2)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=HheartlandnzItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
