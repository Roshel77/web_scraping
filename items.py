import scrapy


class JobparsItem(scrapy.Item):
    # define the fields for your item here like:

    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    link = scrapy.Field()
    salary_max = scrapy.Field()
    salary_min = scrapy.Field()
    currency = scrapy.Field()
    pass
