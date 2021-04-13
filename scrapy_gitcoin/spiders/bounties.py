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
            b_item.description = item.get('metadata', {}).get('issueDescription')
            b_item.status = item.get('status')
            b_item.categories = item.get('bounty_categories')

            b_item.keywords = item.get('keywords', '').split(',')
            b_item.value_in_usdt = item.get('value_in_usdt')
            b_item.token_name = item.get('token_name')
            b_item.value_in_token = item.get('value_in_token')
            b_item.expires_date = item.get('expires_date')
            b_item.issue_type = item.get('metadata', {}).get('bountyType')

            b_item.project_type = item.get('project_type')
            b_item.time_commitment = item.get('metadata', {}).get('projectLength')
            b_item.experience_level = item.get('metadata', {}).get('experienceLevel')
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
