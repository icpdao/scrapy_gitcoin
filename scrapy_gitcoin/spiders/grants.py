import scrapy
import json
import re

from scrapy_gitcoin.items import GrantsItem


class GrantsSpider(scrapy.Spider):
    name = 'grants'
    allowed_domains = ['gitcoin.co']
    start_urls = ['https://gitcoin.co/grants/cards_info?page=1&limit=6&sort_option=-created_on&network=mainnet']

    def parse(self, response):
        content = json.loads(response.body)
        grants = content['grants']
        has_next = content['has_next']

        for item in grants:
            b_item = GrantsItem()
            b_item.item_id = item['id']
            b_item.title = item['title']
            b_item.description = item['description']

            b_item.reference_url = item['reference_url']
            b_item.twitter = item['twitter_handle_1']
            b_item.github_project_url = item['github_project_url']

            region = item.get('region', {})
            if region:
                b_item.region = region.get('name')

            b_item.tenants = item['tenants']
            b_item.amount_received = item['amount_received']
            b_item.url = "https://gitcoin.co{}".format(item['details_url'])

            yield b_item
        
        if has_next:
            res = re.search(r"https://gitcoin.co/grants/cards_info\?page=(.*)&limit=6&sort_option=-created_on&network=mainnet", response.url)
            if res:
                page = res.group(1)
                new_page = int(page) + 1
                new_url = "https://gitcoin.co/grants/cards_info?page={}&limit=6&sort_option=-created_on&network=mainnet".format(
                    new_page
                )
                yield scrapy.Request(new_url, callback=self.parse)
