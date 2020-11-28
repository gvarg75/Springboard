from nflscrape.items import NflscrapeItem
import scrapy
import numpy as np


class NFLSpider(scrapy.Spider):
    teams = ['nwe', 'buf', 'nyj', 'mia', 'rav', 'pit', 'cle', 'cin', 'htx', 'oti', 'clt', 'jax', 'kan', 'den', 'rai',
             'sdg', 'phi', 'dal', 'nyg', 'was', 'gnb', 'min', 'chi', 'det', 'nor', 'atl', 'tam', 'car', 'sfo', 'sea', 'ram', 'crd']
    teams2 = ['nwe', 'buf']
    years = list(np.arange(1998, 2019))
    years2 = list(np.arange(1998, 2000))
    start_urls = ['https://www.pro-football-reference.com/teams/']
    name = "nfl"

    def parse(self, response):
        item = NflscrapeItem()
        rows = response.xpath(
            "//table[@id='teams_active']/tbody//tr/th[@class='left ']")
        for row in rows[1:2]:
            url = row.xpath("./a/@href").get()
            Team = row.xpath(
                ".//text()").get()
            item['Url'] = url
            yield response.follow(url=url, callback=self.parse_team, meta={'Team': Team})

    def parse_team(self, response):
        item = NflscrapeItem()
        Team_meta = response.request.meta
        rows = response.xpath(".//table[@id='team_index']//tbody/tr")
        for row in rows[1:2]:
            yearurl = row.xpath(".//th[@data-stat='year_id']/a/@href").get()
            Team_meta['Year'] = row.xpath(
                ".//th[@data-stat='year_id']/a/text()").get()
            Team_meta['Wins'] = row.xpath(
                ".//td[@data-stat='wins']/text()").get()
            Team_meta['MoV'] = row.xpath(
                ".//td[@data-stat='mov']/text()").get()
            Team_meta['SoS'] = row.xpath(
                "td[@data-stat='sos_total']/text()").get()
            Team_meta['SRS'] = row.xpath(
                "td[@data-stat='srs_total']/text()").get()
            Team_meta['SRS_Off'] = row.xpath(
                "td[@data-stat='srs_offense']/text()").get()
            Team_meta['SRS_Def'] = row.xpath(
                "td[@data-stat='srs_defense']/text()").get()
            # Team_meta = {'Year': Year, 'Wins': Wins, 'MoV': MoV, 'SoS': SoS,
            # 'SRS': SRS, 'SRS_Off': SRS_Off, 'SRS_Def': SRS_Def}
            # year_meta.update(Team_meta)
            # , meta=year_meta)
            yield response.follow(url=yearurl, callback=self.parse_year, meta=Team_meta)

    def parse_year(self, response):
        year_meta = response.request.meta
        print(year_meta)
        # rows = response.xpath(".//table[@id='team_stats']//tbody/tr")
        # for row in rows:
        #  Team_PF = row.xpath(
        #  ".//*[@id='team_stats']//tr[1]//td[1]//text()").get()


"""
item['Year'] = response.xpath(
            "//h1[@itemprop='name']//span[1]//text()").get()
        item['Coach'] = response.xpath(
            "//strong[contains(text(),'Coach:')]/following-sibling::a//text()").get()
        item['Off_Coor'] = response.xpath(
            "//strong[contains(text(),'Offensive Coordinator:')]/following-sibling::a//text()").get()
        item['Def_Coor'] = response.xpath(
            "//strong[contains(text(),'Defensive Coordinator:')]/following-sibling::a//text()").get()
        item['SRS'] = response.xpath(
            "substring-before(substring-after(//strong[contains(text(),'SRS')]/following::text(),':'),'(')").get()
        item['SOS'] = response.xpath(
            "substring-before(substring-after(//strong[contains(text(),'SOS')]/following::text(),':'),'\n')").get()
        item['Off_Scheme'] = response.xpath(
            "//strong[contains(text(),'Offensive Scheme:')]/following::text()").get()
        item['Def_Align'] = response.xpath(
            "//strong[contains(text(),'Defensive Alignment:')]/following::text()").get()
        item['Team_PF'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[1]//text()").get()
        item['Team_Y_P'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[4]//text()").get()
        item['Team_Pass_Cmp'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[8]//text()").get()
        item['Team_Pass_Att'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[9]//text()").get()
        item['Team_Pass_Yds'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[10]//text()").get()
        item['Team_Pass_TD'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[11]//text()").get()
        item['Team_Int'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[12]//text()").get()
        item['Team_Pass_NY_A'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[13]//text()").get()
        item['Team_Rush_Att'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[15]//text()").get()
        item['Team_Rush_Yds'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[16]//text()").get()
        item['Team_Rush_TD'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[17]//text()").get()
        item['Team_Rush_Y_A'] = response.xpath(
            "//*[@id='team_stats']//tr[1]//td[18]//text()").get()
        item['Opp_PF'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[1]//text()").get()
        item['Opp_Y_P'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[3]//text()").get()
        item['Opp_Pass_Cmp'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[8]//text()").get()
        item['Opp_Pass_Att'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[9]//text()").get()
        item['Opp_Pass_Yds'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[10]//text()").get()
        item['Opp_Pass_TD'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[11]//text()").get()
        item['Opp_Int'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[12]//text()").get()
        item['Opp_Pass_NY_A'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[13]//text()").get()
        item['Opp_Rush_Att'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[15]//text()").get()
        item['Opp_Rush_Yds'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[16]//text()").get()
        item['Opp_Rush_TD'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[17]//text()").get()
        item['Opp_Rush_Y_A'] = response.xpath(
            "//*[@id='team_stats']//tr[2]//td[18]//text()").get()"""
