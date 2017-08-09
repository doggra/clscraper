# -*- coding: utf-8 -*-

import time
import datetime
import pygsheets
import scrapy
from scrapy import signals
from ..items import CLScraperItem


class CLScraper(scrapy.Spider):

	name = 'clscraper'
	allowed_domains = ['coinmarketcap.com']
	start_urls = ['https://coinmarketcap.com/all/views/all/']
	coins = []

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(CLScraper, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		spider.logger.info("Uploading results")
		gc = pygsheets.authorize()
		sh = gc.open("CL Data")

		all_wks = sh.worksheets()

		# If max worksheets limit is reached, copy all worksheets to another spreadsheet.
		if len(all_wks) >= 200:
			sh2 = gc.create("CL Data 2")

			for wk in all_wks[1:]:
				wk.copy_to(sh2.id)
				sh.del_worksheet(wk)

		placeholder = sh.sheet1

		wks_name = datetime.datetime.now().strftime("%d/%m/%y")
		wks = sh.add_worksheet(wks_name, rows=1500, cols=10, src_worksheet=placeholder)

		values = []

		for coin in self.coins:
			coin_vals = [coin['_id'], 
						 coin['currency_name'],
						 coin['symbol'],
						 coin['market_cap'],
						 coin['price'],
						 coin['circulating'],
						 coin['volume'],
						 coin['percent_1h'],
						 coin['percent_24h'],
						 coin['percent_7d']]

			values.append(coin_vals)

		wks.update_cells('A2', values)

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

			item = CLScraperItem()
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

			self.coins.append(item)