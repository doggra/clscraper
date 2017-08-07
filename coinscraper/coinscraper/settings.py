# -*- coding: utf-8 -*-

BOT_NAME = 'coinscraper'

SPIDER_MODULES = ['coinscraper.spiders']
NEWSPIDER_MODULE = 'coinscraper.spiders'
ROBOTSTXT_OBEY = False


FIELDS_TO_EXPORT = [
    '_id',
    'currency_name',
    'symbol',
    'market_cap',
    'price',
    'circulating',
    'volume',
    'percent_1h',
    'percent_24h',
    'percent_7d',
]

FEED_URI = "coins.csv"
FEED_FORMAT = 'csv'
FEED_EXPORTERS = {
    'csv': 'coinscraper.exporters.CsvExporter'
}
