# -*- coding: utf-8 -*-

import scrapy

class CLScraperItem(scrapy.Item):
	_id = scrapy.Field()
	currency_name = scrapy.Field()
	symbol = scrapy.Field()
	market_cap = scrapy.Field()
	price = scrapy.Field()
	circulating = scrapy.Field()
	volume = scrapy.Field()
	percent_1h = scrapy.Field()
	percent_24h = scrapy.Field()
	percent_7d = scrapy.Field()