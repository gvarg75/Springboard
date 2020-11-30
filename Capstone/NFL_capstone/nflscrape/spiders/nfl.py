from nflscrape.items import NflscrapeItem
import scrapy
import numpy as np
import time


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
            yield response.follow(url=url, callback=self.parse_team, meta={'Team': Team})

    def parse_team(self, response):
        item = NflscrapeItem()
        Team_meta = response.request.meta
        rows = response.xpath("//table[@id='team_index']//tbody/tr")
        for row in rows[1:2]:
            yearurl = row.xpath(".//th[@data-stat='year_id']/a/@href").get()
            Team_meta['Year'] = row.xpath(
                ".//th[@data-stat='year_id']/a/text()").get()
            Team_meta['Wins'] = row.xpath(
                ".//td[@data-stat='wins']/text()").get()
            Team_meta['MoV'] = row.xpath(
                ".//td[@data-stat='mov']/text()").get()
            Team_meta['SoS'] = row.xpath(
                ".//td[@data-stat='sos_total']/text()").get()
            Team_meta['SRS'] = row.xpath(
                ".//td[@data-stat='srs_total']/text()").get()
            Team_meta['SRS_Off'] = row.xpath(
                ".//td[@data-stat='srs_offense']/text()").get()
            Team_meta['SRS_Def'] = row.xpath(
                ".//td[@data-stat='srs_defense']/text()").get()
            yield response.follow(url=yearurl, callback=self.parse_year, meta=Team_meta)

    def parse_year(self, response):
        year_meta = response.request.meta
        year_meta['Coach'] = response.xpath(
            "//strong[contains(text(),'Coach:')]/following-sibling::a//text()").get()
        year_meta['Off_Coor'] = response.xpath(
            "//strong[contains(text(),'Offensive Coordinator:')]/following-sibling::a//text()").get()
        year_meta['Def_Coor'] = response.xpath(
            "//strong[contains(text(),'Defensive Coordinator:')]/following-sibling::a//text()").get()
        year_meta['SRS'] = response.xpath(
            "substring-before(substring-after(//strong[contains(text(),'SRS')]/following::text(),':'),'(')").get()
        year_meta['SOS'] = response.xpath(
            "substring-before(substring-after(//strong[contains(text(),'SOS')]/following::text(),':'),'\n')").get()
        year_meta['Off_Scheme'] = response.xpath(
            "//strong[contains(text(),'Offensive Scheme:')]/following::text()").get()
        year_meta['Def_Align'] = response.xpath(
            "//strong[contains(text(),'Defensive Alignment:')]/following::text()").get()
        year_meta['Team_PF'] = response.xpath("//*[@id='team_stats']//tr[1]//td[1]//text()").get()
        year_meta['Team_Total_Yards'] = response.xpath("//*[@id='team_stats']//tr[1]//td[2]//text()").get()
        year_meta['Team_Plays_Offense'] = response.xpath("//*[@id='team_stats']//tr[1]//td[3]//text()").get()
        year_meta['Team_yds_per_play_offense'] = response.xpath("//*[@id='team_stats']//tr[4]//td[1]//text()").get()
        year_meta['Team_Turnovers'] = response.xpath("//*[@id='team_stats']//tr[1]//td[5]//text()").get()
        year_meta['Team_Fumbles'] = response.xpath("//*[@id='team_stats']//tr[1]//td[6]//text()").get()
        year_meta['Team_First_down'] = response.xpath("//*[@id='team_stats']//tr[1]//td[7]//text()").get()
        year_meta['Team_Pass_Comp'] = response.xpath("//*[@id='team_stats']//tr[1]//td[8]//text()").get()
        year_meta['Team_Pass_Att'] = response.xpath("//*[@id='team_stats']//tr[1]//td[9]//text()").get()
        year_meta['Team_Pass_Yds'] = response.xpath("//*[@id='team_stats']//tr[1]//td[10]//text()").get()
        year_meta['Team_Pass_Td'] = response.xpath("//*[@id='team_stats']//tr[1]//td[11]//text()").get()
        year_meta['Team_Pass_Int'] = response.xpath("//*[@id='team_stats']//tr[1]//td[12]//text()").get()
        year_meta['Team_Pass_Net_Yds_Att'] = response.xpath("//*[@id='team_stats']//tr[1]//td[13]//text()").get()
        year_meta['Team_Pass_First_Down'] = response.xpath("//*[@id='team_stats']//tr[1]//td[14]//text()").get()
        year_meta['Team_Rush_Att'] = response.xpath("//*[@id='team_stats']//tr[1]//td[15]//text()").get()
        year_meta['Team_Rush_Yds'] = response.xpath("//*[@id='team_stats']//tr[1]//td[16]//text()").get()
        year_meta['Team_Rush_Tds'] = response.xpath("//*[@id='team_stats']//tr[1]//td[17]//text()").get()
        year_meta['Team_Rush_Yds_Att'] = response.xpath("//*[@id='team_stats']//tr[1]//td[18]//text()").get()
        year_meta['Team_Rush_First_Down'] = response.xpath("//*[@id='team_stats']//tr[1]//td[19]//text()").get()
        
        year_meta['Opp_PF'] = response.xpath("//*[@id='team_stats']//tr[2]//td[1]//text()").get()
        year_meta['Opp_Total_Yards'] = response.xpath("//*[@id='team_stats']//tr[2]//td[2]//text()").get()
        year_meta['Opp_Plays_Offense'] = response.xpath("//*[@id='team_stats']//tr[2]//td[3]//text()").get()
        year_meta['Opp_yds_per_play_offense'] = response.xpath("//*[@id='team_stats']//tr[4]//td[1]//text()").get()
        year_meta['Opp_Turnovers'] = response.xpath("//*[@id='team_stats']//tr[2]//td[5]//text()").get()
        year_meta['Opp_Fumbles'] = response.xpath("//*[@id='team_stats']//tr[2]//td[6]//text()").get()
        year_meta['Opp_First_down'] = response.xpath("//*[@id='team_stats']//tr[2]//td[7]//text()").get()
        year_meta['Opp_Pass_Comp'] = response.xpath("//*[@id='team_stats']//tr[2]//td[8]//text()").get()
        year_meta['Opp_Pass_Att'] = response.xpath("//*[@id='team_stats']//tr[2]//td[9]//text()").get()
        year_meta['Opp_Pass_Yds'] = response.xpath("//*[@id='team_stats']//tr[2]//td[10]//text()").get()
        year_meta['Opp_Pass_Td'] = response.xpath("//*[@id='team_stats']//tr[2]//td[11]//text()").get()
        year_meta['Opp_Pass_Int'] = response.xpath("//*[@id='team_stats']//tr[2]//td[12]//text()").get()
        year_meta['Opp_Pass_Net_Yds_Att'] = response.xpath("//*[@id='team_stats']//tr[2]//td[13]//text()").get()
        year_meta['Opp_Pass_First_Down'] = response.xpath("//*[@id='team_stats']//tr[2]//td[14]//text()").get()
        year_meta['Opp_Rush_Att'] = response.xpath("//*[@id='team_stats']//tr[2]//td[15]//text()").get()
        year_meta['Opp_Rush_Yds'] = response.xpath("//*[@id='team_stats']//tr[2]//td[16]//text()").get()
        year_meta['Opp_Rush_Tds'] = response.xpath("//*[@id='team_stats']//tr[2]//td[17]//text()").get()
        year_meta['Opp_Rush_Yds_Att'] = response.xpath("//*[@id='team_stats']//tr[2]//td[18]//text()").get()
        year_meta['Opp_Rush_First_Down'] = response.xpath("//*[@id='team_stats']//tr[2]//td[19]//text()").get()

        Game_table = response.xpath("//table[@id='games']/tbody/tr")
        for game in Game_table:
            if game.xpath(".//td[@data-stat='opp']//text()").get() =='Bye Week':
                pass
            else:
                year_meta['Week']= game.xpath(".//th[@data-stat='week_num']//text()").get()
                year_meta['Week_Opp'] = game.xpath(".//td[@data-stat='opp']//text()").get()
                year_meta['Week_Points_Scored'] = game.xpath(".//td[@data-stat='pts_off']//text()").get()
                year_meta['Week_Points_Allowed'] = game.xpath(".//td[@data-stat='pts_def']//text()").get()
                year_meta['Week_First_Downs'] = game.xpath(".//td[@data-stat='first_down_off']//text()").get()
                year_meta['Week_Total_Off_Yards'] = game.xpath(".//td[@data-stat='opp']//text()").get()
                year_meta['Week_Total_Yards'] = game.xpath(".//td[@data-stat='yards_off']//text()").get()
                year_meta['Week_Pass_Yards'] = game.xpath(".//td[@data-stat='pass_yds_off']//text()").get()
                year_meta['Week_Rush_Yards'] = game.xpath(".//td[@data-stat='rush_yds_off']//text()").get()
                year_meta['Week_Off_Turnovers'] = game.xpath(".//td[@data-stat='to_off']//text()").get()
                year_meta['Week_Def_First_Downs'] = game.xpath(".//td[@data-stat='first_down_def']//text()").get()
                year_meta['Week_Def_Total_Yards'] = game.xpath(".//td[@data-stat='yards_def']//text()").get()
                year_meta['Week_Def_Pass_Yards'] = game.xpath(".//td[@data-stat='pass_yds_def']//text()").get()
                year_meta['Week_Def_Rush_Yards'] = game.xpath(".//td[@data-stat='rush_yds_def']//text()").get()
                year_meta['Week_Def_Turnovers'] = game.xpath(".//td[@data-stat='tp_def']//text()").get()

        Roster_url = response.xpath("//a[contains(text(), 'Starters & Roster')]/@href").get()

        yield response.follow(url=Roster_url, callback=self.parse_roster, meta=year_meta)

    def parse_roster(self, response):
        roster_meta = response.request.meta

        """item['Coach'] = response.xpath(
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