import scrapy


class NFLSpider(scrapy.Spider):
    name = "nfl"
    start_urls = [
        'https://www.pro-football-reference.com/teams/sea/1998.htm,
        ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'Coach': response.xpath("//strong[contains(text(),'Coach:')]/following-sibling::a//text()").get(),
                'SRS': response.xpath("//strong[contains(text(),'SRS')]/following::text()").get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }