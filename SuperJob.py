import scrapy
from scrapy.http import HtmlResponse
from jobpars.items import JobparsItem


class SuperjobSpider(scrapy.Spider):
    name = 'SuperJob'
    allowed_domains = ['superjob.ru']
    page = 2
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@class,"f-test-link-Dalshe")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
            self.page += 1
        links = response.xpath('//a[contains(@class,"_1IHWd _2b9za")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse_sj)

    def vacancy_parse_sj(self, response: HtmlResponse):
        name = response.xpath('//h1[contains(@class, "KySx7 Oert7")]/text()').get()
        link = response.url
        salary = response.xpath('//span[@class="_2eYAG -gENC _1TcZY dAWx1"]/text()').getall()
        yield JobparsItem(name=name, link=link, salary=salary)
