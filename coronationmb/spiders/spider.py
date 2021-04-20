import scrapy

from scrapy.loader import ItemLoader

from ..items import CoronationmbItem
from itemloaders.processors import TakeFirst


class CoronationmbSpider(scrapy.Spider):
	name = 'coronationmb'
	start_urls = ['https://www.coronationmb.com/category/press-releases/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="elementor-post__text"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="page-numbers next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="elementor-element elementor-element-62bd2b0 elementor-widget elementor-widget-theme-post-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"]/text()').get()

		item = ItemLoader(item=CoronationmbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
