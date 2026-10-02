# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

import scrapy


@dataclass
class AgentsscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = 
    pass

class AgentItem(scrapy.Item):

    first_name = scrapy.Field()
    last_name = scrapy.Field()
    email_address = scrapy.Field()
