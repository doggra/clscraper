# -*- coding: utf-8 -*-

import pygsheets
import scrapy
from scrapy import signals
from ..items import CoinscraperItem

class CoinScraper(scrapy.Spider):

	name = 'coinscraper'
	allowed_domains = ['coinmarketcap.com']
	start_urls = ['https://coinmarketcap.com/all/views/all/']


	def parse(self, response):

		coins_table_rows = response.css('table#currencies-all tbody tr')

		for row in coins_table_rows:
			_id = row.css('td::text').extract_first().strip()
			currency_name = row.css('td.currency-name a::text').extract_first().strip()
			symbol = row.css('td::text').extract()[4].strip()
			market_cap = row.css('td.market-cap::text').extract_first().strip()
			price = row.css('td a.price::text').extract_first().strip()
			try:
				circulating = row.css('td')[5].css('a::text').extract_first().strip()
			except:
				circulating = row.css('td')[5].css('span::text').extract_first().strip()
			volume = row.css('td a.volume::text').extract_first().strip()
			percent_1h = row.css('td')[7].css('::text').extract_first().strip()
			percent_24h = row.css('td')[8].css('::text').extract_first().strip()
			percent_7d = row.css('td')[9].css('::text').extract_first().strip()

			item = CoinscraperItem()
			item['_id'] = _id
			item['currency_name'] = currency_name
			item['symbol'] = symbol
			item['market_cap'] = market_cap
			item['price'] = price
			item['circulating'] = circulating
			item['volume'] = volume
			item['percent_1h'] = percent_1h
			item['percent_24h'] = percent_24h
			item['percent_7d'] = percent_7d

			yield item