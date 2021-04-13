import scrapy
import json
import re
from scrapy_gitcoin.items import BountiesItem


class BountiesSpider(scrapy.Spider):
    name = 'bounties'
    allowed_domains = ['gitcoin.co']
    start_urls = ['https://gitcoin.co/api/v0.1/bounties/slim/?network=mainnet&applicants=ALL&order_by=-web3_created&offset=0&limit=10']

    def parse(self, response):
        content = json.loads(response.body)
        count = len(content)

        for item in content:
            b_item = BountiesItem()
            b_item.item_id = item['pk']
            b_item.title = item['title']
            b_item.description = item['metadata']['issueDescription']
            b_item.status = item['status']
            b_item.categories = item['bounty_categories']

            b_item.keywords = item['keywords'].split(',')
            b_item.value_in_usdt = item['value_in_usdt']
            b_item.token_name = item['token_name']
            b_item.value_in_token = item['value_in_token']
            b_item.expires_date = item['expires_date']
            b_item.issue_type = item['metadata']['bountyType']

            b_item.project_type = item['project_type']
            b_item.time_commitment = item['metadata']['projectLength']
            b_item.experience_level = item['metadata']['experienceLevel']
            yield b_item
        
        res = re.search(r"https://gitcoin.co/api/v0.1/bounties/slim/\?network=mainnet&applicants=ALL&order_by=-web3_created&offset=(.*)&limit=(.*)", response.url)
        if res:
            offset = res.group(1)
            limit = res.group(2)
            new_offset = int(offset) + int(limit)
            new_url = "https://gitcoin.co/api/v0.1/bounties/slim/?network=mainnet&applicants=ALL&order_by=-web3_created&offset={}&limit={}".format(
                new_offset, limit
            )
            if count > 0:
                yield scrapy.Request(new_url, callback=self.parse)
