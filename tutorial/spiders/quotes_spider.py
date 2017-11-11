import scrapy
from datetime import datetime
from tutorial.items import MacappItem
from slugify import slugify
import re
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://cmacapps.com',
    ]
    count = 1
    def parse(self, response):
        self.count += 1
        for article in response.xpath("//article[contains(@class, 'post')]"):
            try:
                item = MacappItem()
                icon = article.xpath("./figure/a/img/@srcset").extract_first()
                if icon:
                    icon = icon.split(', ')[-1].split(' ')[0]
                else:
                    icon = article.xpath("./figure/a/img/@src").extract_first()
                # if icon:
                #     item["icon"] = icon.split(', ')[-1].split(' ')[0]
                item["icon"] = icon
                date_upload = article.xpath("./div/div/div[1]/time/@datetime").extract_first()
                date_upload = datetime.strptime(date_upload, "%Y-%m-%d")
                item["date_upload"] = date_upload
                item["name"] = article.xpath("./div/div/h2/a/text()").extract_first()
                item["slug"] = slugify(item["name"])
                link = article.xpath("./div/div/h2/a/@href").extract_first()
                item["category"] = article.xpath("./div/div/p/span[2]/a/text()").extract()
                yield scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})
            except:
                pass
        # next_page = 'https://cmacapps.com/page/{}/'.format(self.count)
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):

        item = response.meta['item']
        if 'wpappbox' in response.text:
            screenshots = response.xpath("//div[contains(@class, 'wpappbox')]/div[@class='screenshots']/div/ul/li/img/@src").extract()
            if len(screenshots) > 0:
                screenshots = [x[2:] for x in screenshots]
                item["screenshots"] = screenshots
            item["developer"] = response.xpath("//div[contains(@class, 'developer')]/text()").extract_first()
            price = response.xpath("//div[contains(@class, 'price')]/span/text()").extract_first()
            if price:
                price = price[7:]
            item["price"] = price
            item["rating"] = response.xpath("//div[contains(@class, 'price')]/div/@title").extract_first()
            descriptions = response.xpath("//div[contains(@class, 'product-review')]/p/text()").extract()
            descriptions = '<br>'.join(descriptions)
            item["description"] = descriptions
            item["download_link"] = response.xpath("//p[contains(@class, 'p1')]/a/@href").extract()
            yield item
        else:
            screenshots = response.xpath("//div[contains(@class, 'entry-content')]/p/img/@srcset").extract_first()
            if screenshots:
                item["screenshots"] = screenshots.split(', ')[-1].split(' ')[0]
            description = response.xpath("//div[@id='description']").extract_first()
            if description:
                description = re.sub(r'https://cdn.cmacapps.com', 'http://127.0.0.1:8080/upload/q_100/https://cdn.cmacapps.com', description)
            item["description"] = description
            item["download_link"] = response.xpath("//p[contains(@class, 'p1')]/a/@href").extract()
            yield item

