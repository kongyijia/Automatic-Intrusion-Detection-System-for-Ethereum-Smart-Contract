# use www.stateofthedapp.com to get categories
# use etherscan api to get transactions
# focus on main net
# only collect the following categories:
# exchanges, finance, gambling, games, nft and social
import json

import scrapy

from production.items import ProductionItem
from utils.generate_url import make_etherscan_tx_url
from utils.generate_url import make_stateofdapps_url

categories = ['exchanges', 'finance', 'gambling', 'games', 'nft', 'social']


class ProductionSpider(scrapy.Spider):
    name = "production"

    def start_requests(self):
        for category in categories:
            current = 1
            url = make_stateofdapps_url(category, current)
            yield scrapy.Request(url=url, callback=self.parse, meta={'category': category, 'current': current})

    def parse(self, response):
        for row in response.css('div.table-body').css('div.table-row'):
            goto = row.css('h4.name a::attr(href)').get()
            yield response.follow(goto, callback=self.details, meta={'category': response.meta['category']})
        last = int(response.css('div.next-prev-wrapper button')[-1].css('span.button-inner::text').get())
        if response.meta['current'] < last:
            category = response.meta['category']
            current = response.meta['current'] + 1
            url = make_stateofdapps_url(category, current)
            yield scrapy.Request(url=url, callback=self.parse, meta={'category': category, 'current': current})

    def details(self, response):
        script = response.xpath("/html/body/script[1]/text()").extract()
        mainnet = str(script).split("contractsMainnet")[1].split(']')[0] \
            .replace('[', '').replace('\"', '').replace(':', '') \
            .split(',')
        if len(mainnet) > 0:
            for address in mainnet:
                if len(address) == 42:
                    tx_url = make_etherscan_tx_url(address, 'txlist')
                    tx_url_internal = make_etherscan_tx_url(address, 'txlistinternal')
                    request = scrapy.Request(url=tx_url, callback=self.get_txlist)
                    request.meta['address'] = address
                    request.meta['category'] = response.meta['category']
                    request.meta['url_internal'] = tx_url_internal
                    yield request

    def get_txlist(self, response):
        item = ProductionItem()
        item['address'] = response.meta['address']
        result = json.loads(response.text)['result']
        if result == "Max rate limit reached":
            try_again = scrapy.Request(url=response.url, callback=self.get_txlist,
                                       meta={'address': response.meta['address'],
                                             'url_internal': response.meta['url_internal'],
                                             'category': response.meta['category']})
            return try_again
        item['txlist'] = result
        item['category'] = response.meta['category']
        request = scrapy.Request(url=response.meta['url_internal'], callback=self.get_txlist_internal)
        request.meta['item'] = item
        return request

    def get_txlist_internal(self, response):
        item = response.meta['item']
        result = json.loads(response.text)['result']
        if result == "Max rate limit reached":
            request = scrapy.Request(url=response.url, callback=self.get_txlist_internal)
            request.meta['item'] = item
            return request
        item['txlistinternal'] = result
        return item
