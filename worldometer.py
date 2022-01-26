
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue
import datetime as dt

import schedule
import time
import os
import sys

class Worldometer4Spider(scrapy.Spider):
    name = 'worldometer'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/population/']

    def parse(self, response):
        continents = response.xpath('//li/a/strong[contains(text(), "Countries")]')

        for continent in continents:
            continent_name = continent.xpath('.//text()').get()
            page_link = continent.xpath('..//@href').get()
            #absolute_url = response.urljoin(page_link)

            yield response.follow(url=page_link, callback=self.parse_continent, meta={'continent': continent_name})

    def parse_continent(self, response):
        rows_1 = response.xpath("(//table[contains(@class, 'table')])[1]/tbody/tr")
        continent = response.request.meta['continent']

        for row in rows_1:
            countries = row.xpath('.//td/a/text()').get()
            link = row.xpath('.//td/a//@href').get()
            migrants  = row.xpath('.//td[8]/text()').get()
            fertility_rate = row.xpath('.//td[9]/text()').get()
            med_age = row.xpath('.//td[10]/text()').get()


            yield response.follow(url=link, callback=self.parse_row, meta={'country':countries, 'continent': continent, 'migrants': migrants, 'fertility_rate': fertility_rate, 'med_age': med_age})

    def parse_row(self, response):
        rows = response.xpath("(//table[contains(@class, 'table')])[1]/tbody/tr")
        country = response.request.meta['country']
        continent = response.request.meta['continent']
        migrants = response.request.meta['migrants']
        fertility_rate = response.request.meta['fertility_rate']
        med_age = response.request.meta['med_age']

        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath(".//td[2]/strong/text()").get()  # prendo il 2°tag td che contiene la popolazione

            yield {
                'continent': continent,
                'country': country,
                'year': year,
                'population': population,
                'migrants': migrants,
                'fertility rate': fertility_rate,
                'med_age': med_age,

            }


process = CrawlerProcess(settings={
  "FEEDS": {"t_demographics_hist.xlsx": {"format": "xlsx", "overwrite": True}},
  "FEED_EXPORTERS": {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
  'ROBOTSTXT_OBEY': 'False',
  'AUTOTHROTTLE_ENABLED': 'True',
  'AUTOTHROTTLE_START_DELAY': '5'
})

process.crawl(Worldometer4Spider)
process.start()


time.sleep(300)






