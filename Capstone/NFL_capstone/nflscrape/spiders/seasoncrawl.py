import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nflscrape.items import SeasoncrawlItem


class SeasoncrawlSpider(CrawlSpider):
    name = 'seasoncrawl'
    allowed_domains = ['www.pro-football-reference.com']
    start_urls = ['https:////www.pro-football-reference.com/teams/']
    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//table[@id='teams_active']//th[@class='left ']/a"), callback='parse_team', follow=True),
    )

    def parse_team(self, response):
        item = SeasoncrawlItem()
        rows = response.xpath("//table[@id='team_index']//tbody/tr")
        for row in rows[1:2]:
            item['Team'] = response.xpath(
                ".//td[@data-stat='team']/a/text()").get()
            item['Year'] = response.xpath(
                ".//th[@data-stat='year_id']/a/text()").get()
            item['Wins'] = response.xpath(
                ".//td[@data-stat='wins']/text()").get()
            item['MoV'] = response.xpath(
                ".//td[@data-stat='mov']/text()").get()
            item['SoS'] = response.xpath(
                "td[@data-stat='sos_total']/text()").get()
            item['SRS'] = response.xpath(
                "td[@data-stat='srs_total']/text()").get()
            item['SRS_Off'] = response.xpath(
                "td[@data-stat='srs_offense']/text()").get()
            item['SRS_Def'] = response.xpath(
                "td[@data-stat='srs_defense']/text()").get()
            link = row.xpath(".//@href").get()
            yield item
            yield response.follow(url=link, callback=self.parse_year)

    def parse_year(self, response):
        item = SeasoncrawlItem()
        teamrows = response.xpath(".//table[@id='team_stats']//tbody/tr")
        for row in teamrows:
            item['Points'] = row.xpath(
                ".//td[@data-stat='points']/text()").get()
            yield item
