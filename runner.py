from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobpars.spiders.SuperJob import SuperjobSpider
from jobpars import settings
# from jobpars.spiders.hhru import HhruSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    # process.crawl(HhruSpider)
    process.crawl(SuperjobSpider)

    process.start()