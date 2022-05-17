import scrapy
from scrapy.http import HtmlResponse
from jobpars.items import JobparsItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    page = 2
    start_urls = [
        'https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
            self.page += 1
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse_hh)

    def vacancy_parse_hh(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']/span/text()").getall()
        link = response.url

        yield JobparsItem(name=name, salary=salary, link=link)