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
        Team_meta = {}
        for row in rows:
            url = row.xpath("./a/@href").get()
            Team_meta['Team'] = row.xpath(
                ".//text()").get()
            item['Team'] = Team_meta['Team']
            yield response.follow(url=url, callback=self.parse_team, meta=Team_meta, dont_filter=True)

    def parse_team(self, response):
        item = NflscrapeItem()
        full_Team_meta = response.request.meta
        rem_list = ['depth', 'download_timeout',
                    'download_slot', 'download_latency']
        Team_meta = dict(
            [(key, val) for key, val in full_Team_meta.items() if key not in rem_list])
        rows = response.xpath("//table[@id='team_index']//tbody/tr")
        for row in rows[1:19]:
            yearurl = row.xpath(
                ".//th[@data-stat='year_id']/a/@href").get()
            Team_meta['Year'] = row.xpath(
                ".//th[@data-stat='year_id']/a/text()").get()
            Team_meta['Wins'] = row.xpath(
                ".//td[@data-stat='wins']/text()").get()
            Team_meta['Losses'] = row.xpath(
                ".//td[@data-stat='losses']/text()").get()
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
        item = NflscrapeItem()
        full_year_meta = response.request.meta
        rem_list = ['depth', 'download_timeout',
                    'download_slot', 'download_latency']
        year_meta = dict(
            [(key, val) for key, val in full_year_meta.items() if key not in rem_list])
        Game_table = response.xpath("//table[@id='games']/tbody/tr")
        for game in Game_table:
            if game.xpath(".//td[@data-stat='opp']//text()").get() == 'Bye Week' or game.xpath(".//td[@data-stat='game_date']//text()").get() == 'Playoffs':
                pass
            else:
                year_meta['Week'] = game.xpath(
                    ".//th[@data-stat='week_num']//text()").get()
                year_meta['Week_Opp'] = game.xpath(
                    ".//td[@data-stat='opp']//text()").get()
                year_meta['Week_Points_Scored'] = game.xpath(
                    ".//td[@data-stat='pts_off']//text()").get()
                year_meta['Week_Points_Allowed'] = game.xpath(
                    ".//td[@data-stat='pts_def']//text()").get()
                year_meta['Week_First_Downs'] = game.xpath(
                    ".//td[@data-stat='first_down_off']//text()").get()
                year_meta['Week_Total_Off_Yards'] = game.xpath(
                    ".//td[@data-stat='yards_off']//text()").get()
                year_meta['Week_Pass_Yards'] = game.xpath(
                    ".//td[@data-stat='pass_yds_off']//text()").get()
                year_meta['Week_Rush_Yards'] = game.xpath(
                    ".//td[@data-stat='rush_yds_off']//text()").get()
                if game.xpath(".//td[@data-stat='to_off']//text()").get() == "":
                    year_meta["Week_Off_Turnovers"] = 0
                else:
                    year_meta['Week_Off_Turnovers'] = game.xpath(
                        ".//td[@data-stat='to_off']//text()").get()
                year_meta['Week_Def_First_Downs'] = game.xpath(
                    ".//td[@data-stat='first_down_def']//text()").get()
                year_meta['Week_Def_Total_Yards'] = game.xpath(
                    ".//td[@data-stat='yards_def']//text()").get()
                year_meta['Week_Def_Pass_Yards'] = game.xpath(
                    ".//td[@data-stat='pass_yds_def']//text()").get()
                year_meta['Week_Def_Rush_Yards'] = game.xpath(
                    ".//td[@data-stat='rush_yds_def']//text()").get()
                if game.xpath(".//td[@data-stat='to_off']//text()").get() == "":
                    year_meta["Week_Def_Turnovers"] = 0
                else:
                    year_meta['Week_Def_Turnovers'] = game.xpath(
                        ".//td[@data-stat='to_def']//text()").get()
                year_meta['Coach'] = response.xpath(
                    "//strong[contains(text(),'Coach:')]/following-sibling::a//text()").get()
                year_meta['Off_Coor'] = response.xpath(
                    "//strong[contains(text(),'Offensive Coordinator:')]/following-sibling::a//text()").get()
                year_meta['Def_Coor'] = response.xpath(
                    "//strong[contains(text(),'Defensive Coordinator:')]/following-sibling::a//text()").get()
                year_meta['Off_Scheme'] = response.xpath(
                    "//strong[contains(text(),'Offensive Scheme:')]/following::text()").get()
                year_meta['Def_Align'] = response.xpath(
                    "//strong[contains(text(),'Defensive Alignment:')]/following::text()").get()
                year_meta['Team_PF'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[1]//text()").get()
                year_meta['Team_Total_Yards'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[2]//text()").get()
                year_meta['Team_Plays_Offense'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[3]//text()").get()
                year_meta['Team_yds_per_play_offense'] = response.xpath(
                    "//*[@id='team_stats']//tr[4]//td[1]//text()").get()
                year_meta['Team_Turnovers'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[5]//text()").get()
                year_meta['Team_Fumbles'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[6]//text()").get()
                year_meta['Team_First_down'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[7]//text()").get()
                year_meta['Team_Pass_Comp'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[8]//text()").get()
                year_meta['Team_Pass_Att'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[9]//text()").get()
                year_meta['Team_Pass_Yds'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[10]//text()").get()
                year_meta['Team_Pass_Td'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[11]//text()").get()
                year_meta['Team_Pass_Int'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[12]//text()").get()
                year_meta['Team_Pass_Net_Yds_Att'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[13]//text()").get()
                year_meta['Team_Pass_First_Down'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[14]//text()").get()
                year_meta['Team_Rush_Att'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[15]//text()").get()
                year_meta['Team_Rush_Yds'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[16]//text()").get()
                year_meta['Team_Rush_Tds'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[17]//text()").get()
                year_meta['Team_Rush_Yds_Att'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[18]//text()").get()
                year_meta['Team_Rush_First_Down'] = response.xpath(
                    "//*[@id='team_stats']//tr[1]//td[19]//text()").get()

                year_meta['Opp_PF'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[1]//text()").get()
                year_meta['Opp_Total_Yards'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[2]//text()").get()
                year_meta['Opp_Plays_Offense'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[3]//text()").get()
                year_meta['Opp_yds_per_play_offense'] = response.xpath(
                    "//*[@id='team_stats']//tr[4]//td[1]//text()").get()
                year_meta['Opp_Turnovers'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[5]//text()").get()
                year_meta['Opp_Fumbles'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[6]//text()").get()
                year_meta['Opp_First_down'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[7]//text()").get()
                year_meta['Opp_Pass_Comp'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[8]//text()").get()
                year_meta['Opp_Pass_Att'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[9]//text()").get()
                year_meta['Opp_Pass_Yds'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[10]//text()").get()
                year_meta['Opp_Pass_Td'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[11]//text()").get()
                year_meta['Opp_Pass_Int'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[12]//text()").get()
                year_meta['Opp_Pass_Net_Yds_Att'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[13]//text()").get()
                year_meta['Opp_Pass_First_Down'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[14]//text()").get()
                year_meta['Opp_Rush_Att'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[15]//text()").get()
                year_meta['Opp_Rush_Yds'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[16]//text()").get()
                year_meta['Opp_Rush_Tds'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[17]//text()").get()
                year_meta['Opp_Rush_Yds_Att'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[18]//text()").get()
                year_meta['Opp_Rush_First_Down'] = response.xpath(
                    "//*[@id='team_stats']//tr[2]//td[19]//text()").get()
                roster_url = response.xpath(
                    "//a[contains(text(), 'Starters & Roster')]/@href").get()
                draft_url = response.xpath(
                    "//a[contains(text(), 'Team Draftees')]/@href").get()
                """item['Team'] = year_meta['Team']
                item['Year'] = year_meta['Year']
                item['Wins'] = year_meta['Wins']
                item['Losses'] = year_meta['Losses']
                item['MoV'] = year_meta['MoV']
                item['SoS'] = year_meta['SoS']
                item['SRS'] = year_meta['SRS']
                item['SRS_Off'] = year_meta['SRS_Off']
                item['SRS_Def'] = year_meta['SRS_Def']
                item['Coach'] = year_meta['Coach']
                item['Off_Coor'] = year_meta['Off_Coor']
                item['Def_Coor'] = year_meta['Def_Coor']
                item['Off_Scheme'] = year_meta['Off_Scheme']
                item['Def_Align'] = year_meta['Def_Align']
                item['Team_PF'] = year_meta['Team_PF']
                item['Team_Total_Yards'] = year_meta['Team_Total_Yards']
                item['Team_Plays_Offense'] = year_meta['Team_Plays_Offense']
                item['Team_yds_per_play_offense'] = year_meta['Team_yds_per_play_offense']
                item['Team_Turnovers'] = year_meta['Team_Turnovers']
                item['Team_Fumbles'] = year_meta['Team_Fumbles']
                item['Team_First_down'] = year_meta['Team_First_down']
                item['Team_Pass_Comp'] = year_meta['Team_Pass_Comp']
                item['Team_Pass_Att'] = year_meta['Team_Pass_Att']
                item['Team_Pass_Yds'] = year_meta['Team_Pass_Yds']
                item['Team_Pass_Td'] = year_meta['Team_Pass_Td']
                item['Team_Pass_Int'] = year_meta['Team_Pass_Int']
                item['Team_Pass_Net_Yds_Att'] = year_meta['Team_Pass_Net_Yds_Att']
                item['Team_Pass_First_Down'] = year_meta['Team_Pass_First_Down']
                item['Team_Rush_Att'] = year_meta['Team_Rush_Att']
                item['Team_Rush_Yds'] = year_meta['Team_Rush_Yds']
                item['Team_Rush_Tds'] = year_meta['Team_Rush_Tds']
                item['Team_Rush_Yds_Att'] = year_meta['Team_Rush_Yds_Att']
                item['Team_Rush_First_Down'] = year_meta['Team_Rush_First_Down']
                item['Opp_PF'] = year_meta['Opp_PF']
                item['Opp_Total_Yards'] = year_meta['Opp_Total_Yards']
                item['Opp_Plays_Offense'] = year_meta['Opp_Plays_Offense']
                item['Opp_yds_per_play_offense'] = year_meta['Opp_yds_per_play_offense']
                item['Opp_Turnovers'] = year_meta['Opp_Turnovers']
                item['Opp_Fumbles'] = year_meta['Opp_Fumbles']
                item['Opp_First_down'] = year_meta['Opp_First_down']
                item['Opp_Pass_Comp'] = year_meta['Opp_Pass_Comp']
                item['Opp_Pass_Att'] = year_meta['Opp_Pass_Att']
                item['Opp_Pass_Yds'] = year_meta['Opp_Pass_Yds']
                item['Opp_Pass_Td'] = year_meta['Opp_Pass_Td']
                item['Opp_Pass_Int'] = year_meta['Opp_Pass_Int']
                item['Opp_Pass_Net_Yds_Att'] = year_meta['Opp_Pass_Net_Yds_Att']
                item['Opp_Pass_First_Down'] = year_meta['Opp_Pass_First_Down']
                item['Opp_Rush_Att'] = year_meta['Opp_Rush_Att']
                item['Opp_Rush_Yds'] = year_meta['Opp_Rush_Yds']
                item['Opp_Rush_Tds'] = year_meta['Opp_Rush_Tds']
                item['Opp_Rush_Yds_Att'] = year_meta['Opp_Rush_Yds_Att']
                item['Opp_Rush_First_Down'] = year_meta['Opp_Rush_First_Down']
                item['Week'] = year_meta['Week']
                item['Week_Opp'] = year_meta['Week_Opp']
                item['Week_Points_Scored'] = year_meta['Week_Points_Scored']
                item['Week_Points_Allowed'] = year_meta['Week_Points_Allowed']
                item['Week_First_Downs'] = year_meta['Week_First_Downs']
                item['Week_Total_Off_Yards'] = year_meta['Week_Total_Off_Yards']
                item['Week_Pass_Yards'] = year_meta['Week_Pass_Yards']
                item['Week_Rush_Yards'] = year_meta['Week_Rush_Yards']
                item['Week_Off_Turnovers'] = year_meta['Week_Off_Turnovers']
                item['Week_Def_First_Downs'] = year_meta['Week_Def_First_Downs']
                item['Week_Def_Total_Yards'] = year_meta['Week_Def_Total_Yards']
                item['Week_Def_Pass_Yards'] = year_meta['Week_Def_Pass_Yards']
                item['Week_Def_Rush_Yards'] = year_meta['Week_Def_Rush_Yards']
                item['Week_Def_Turnovers'] = year_meta['Week_Def_Turnovers']"""
                #yield item

        yield response.follow(url=draft_url, callback=self.parse_draft, meta=year_meta, dont_filter=True)

    def parse_roster(self, response):
        item = NflscrapeItem()
        full_roster_meta = response.request.meta
        rem_list = ['depth', 'download_timeout',
                    'download_slot', 'download_latency']
        roster_meta = dict(
            [(key, val) for key, val in full_roster_meta.items() if key not in rem_list])
        rows = response.xpath("//table[@id='starters']//tbody//tr")
        for row in rows:
            if row.xpath(".//td[@data-stat='player']//b//text()").get() in ['Offensive Starters', 'Defensive Starters']:
                pass
            else:
                if row.xpath(".//th[@data-stat='pos']//text()").get() in ['CB', 'DB', 'LCB', 'RCB', 'S', 'SS', 'FS']:
                    roster_meta['Starting_Position'] = 'DB'
                elif row.xpath(".//th[@data-stat='pos']//text()").get() in ['C', 'OL', 'G', 'T']:
                    roster_meta['Starting_Position'] = 'OL'
                elif row.xpath(".//th[@data-stat='pos']//text()").get() in ['DE', 'LDE', 'RDE']:
                    roster_meta['Starting_Position'] = 'DE'
                elif row.xpath(".//th[@data-stat='pos']//text()").get() in ['DT', 'LDT', 'RDT', 'NT']:
                    roster_meta['Starting_Position'] = 'DT'
                elif row.xpath(".//th[@data-stat='pos']//text()").get() in ['FB', 'RB']:
                    roster_meta['Starting_Position'] = 'RB'
                elif row.xpath(".//th[@data-stat='pos']//text()").get() in ['LB', 'LLB', 'MLB', 'RLB', 'LOLB', 'LILB', 'RILB', 'ROLB', 'OLB']:
                    roster_meta['Starting_Position'] = 'LB'
                else:
                    roster_meta['Starting_Position'] = row.xpath(
                        ".//th[@data-stat='pos']//text()").get()
                roster_meta['Starting_Player'] = row.xpath(
                    ".//td[@data-stat='player']//a//text()").get()
                roster_meta['Starting_Player_Age'] = int(roster_meta['Year']) - int(row.xpath(
                    ".//td[@data-stat='age']//text()").get())
                roster_meta['Starting_Player_Yrs'] = row.xpath(
                    ".//td[@data-stat='experience']//text()").get()
                roster_meta['Starting_Player_GS'] = row.xpath(
                    ".//td[@data-stat='gs']//text()").get()
                draft_url = response.xpath(
                    "//a[contains(text(), 'Team Draftees')]/@href").get()
                """item['Team'] = roster_meta['Team']
                item['Year'] = roster_meta['Year']
                item['Wins'] = roster_meta['Wins']
                item['Losses'] = roster_meta['Losses']
                item['MoV'] = roster_meta['MoV']
                item['SoS'] = roster_meta['SoS']
                item['SRS'] = roster_meta['SRS']
                item['SRS_Off'] = roster_meta['SRS_Off']
                item['SRS_Def'] = roster_meta['SRS_Def']
                item['Coach'] = roster_meta['Coach']
                item['Off_Coor'] = roster_meta['Off_Coor']
                item['Def_Coor'] = roster_meta['Def_Coor']
                item['Off_Scheme'] = roster_meta['Off_Scheme']
                item['Def_Align'] = roster_meta['Def_Align']
                item['Team_PF'] = roster_meta['Team_PF']
                item['Team_Total_Yards'] = roster_meta['Team_Total_Yards']
                item['Team_Plays_Offense'] = roster_meta['Team_Plays_Offense']
                item['Team_yds_per_play_offense'] = roster_meta['Team_yds_per_play_offense']
                item['Team_Turnovers'] = roster_meta['Team_Turnovers']
                item['Team_Fumbles'] = roster_meta['Team_Fumbles']
                item['Team_First_down'] = roster_meta['Team_First_down']
                item['Team_Pass_Comp'] = roster_meta['Team_Pass_Comp']
                item['Team_Pass_Att'] = roster_meta['Team_Pass_Att']
                item['Team_Pass_Yds'] = roster_meta['Team_Pass_Yds']
                item['Team_Pass_Td'] = roster_meta['Team_Pass_Td']
                item['Team_Pass_Int'] = roster_meta['Team_Pass_Int']
                item['Team_Pass_Net_Yds_Att'] = roster_meta['Team_Pass_Net_Yds_Att']
                item['Team_Pass_First_Down'] = roster_meta['Team_Pass_First_Down']
                item['Team_Rush_Att'] = roster_meta['Team_Rush_Att']
                item['Team_Rush_Yds'] = roster_meta['Team_Rush_Yds']
                item['Team_Rush_Tds'] = roster_meta['Team_Rush_Tds']
                item['Team_Rush_Yds_Att'] = roster_meta['Team_Rush_Yds_Att']
                item['Team_Rush_First_Down'] = roster_meta['Team_Rush_First_Down']
                item['Opp_PF'] = roster_meta['Opp_PF']
                item['Opp_Total_Yards'] = roster_meta['Opp_Total_Yards']
                item['Opp_Plays_Offense'] = roster_meta['Opp_Plays_Offense']
                item['Opp_yds_per_play_offense'] = roster_meta['Opp_yds_per_play_offense']
                item['Opp_Turnovers'] = roster_meta['Opp_Turnovers']
                item['Opp_Fumbles'] = roster_meta['Opp_Fumbles']
                item['Opp_First_down'] = roster_meta['Opp_First_down']
                item['Opp_Pass_Comp'] = roster_meta['Opp_Pass_Comp']
                item['Opp_Pass_Att'] = roster_meta['Opp_Pass_Att']
                item['Opp_Pass_Yds'] = roster_meta['Opp_Pass_Yds']
                item['Opp_Pass_Td'] = roster_meta['Opp_Pass_Td']
                item['Opp_Pass_Int'] = roster_meta['Opp_Pass_Int']
                item['Opp_Pass_Net_Yds_Att'] = roster_meta['Opp_Pass_Net_Yds_Att']
                item['Opp_Pass_First_Down'] = roster_meta['Opp_Pass_First_Down']
                item['Opp_Rush_Att'] = roster_meta['Opp_Rush_Att']
                item['Opp_Rush_Yds'] = roster_meta['Opp_Rush_Yds']
                item['Opp_Rush_Tds'] = roster_meta['Opp_Rush_Tds']
                item['Opp_Rush_Yds_Att'] = roster_meta['Opp_Rush_Yds_Att']
                item['Opp_Rush_First_Down'] = roster_meta['Opp_Rush_First_Down']
                item['Week'] = roster_meta['Week']
                item['Week_Opp'] = roster_meta['Week_Opp']
                item['Week_Points_Scored'] = roster_meta['Week_Points_Scored']
                item['Week_Points_Allowed'] = roster_meta['Week_Points_Allowed']
                item['Week_First_Downs'] = roster_meta['Week_First_Downs']
                item['Week_Total_Off_Yards'] = roster_meta['Week_Total_Off_Yards']
                item['Week_Pass_Yards'] = roster_meta['Week_Pass_Yards']
                item['Week_Rush_Yards'] = roster_meta['Week_Rush_Yards']
                item['Week_Off_Turnovers'] = roster_meta['Week_Off_Turnovers']
                item['Week_Def_First_Downs'] = roster_meta['Week_Def_First_Downs']
                item['Week_Def_Total_Yards'] = roster_meta['Week_Def_Total_Yards']
                item['Week_Def_Pass_Yards'] = roster_meta['Week_Def_Pass_Yards']
                item['Week_Def_Rush_Yards'] = roster_meta['Week_Def_Rush_Yards']
                item['Week_Def_Turnovers'] = roster_meta['Week_Def_Turnovers']
                item['Starting_Position'] = roster_meta['Starting_Position']
                item['Starting_Player'] = roster_meta['Starting_Player']
                item['Starting_Player_Age'] = roster_meta['Starting_Player_Age']
                item['Starting_Player_Yrs'] = roster_meta['Starting_Player_Yrs']
                item['Starting_Player_GS'] = roster_meta['Starting_Player_GS']
                yield item"""
    
    def parse_draft(self, response):
        item = NflscrapeItem()
        full_draft_meta = response.request.meta
        rem_list = ['depth', 'download_timeout',
                    'download_slot', 'download_latency']
        draft_meta = dict(
            [(key, val) for key, val in full_draft_meta.items() if key not in rem_list])
        rows = response.xpath("//table[@id='draft']//tbody//tr")
        for idx,row in enumerate(rows):
            draft_meta['Draft_Round'] = row.xpath(
                        ".//th[@data-stat='draft_round']//text()").get()
            draft_meta['Draft_Player'] = row.xpath(
                        ".//td[@data-stat='player']//text()").get()
            draft_meta['Draft_Pick'] = row.xpath(
                        ".//td[@data-stat='draft_pick']//text()").get()
            if row.xpath(".//th[@data-stat='pos']//text()").get() in ['CB', 'DB', 'LCB', 'RCB', 'S', 'SS', 'FS']:
                    draft_meta['Draft_Position'] = 'DB'
            elif row.xpath(".//td[@data-stat='pos']//text()").get() in ['C', 'OL', 'G', 'T']:
                draft_meta['Draft_Position'] = 'OL'
            elif row.xpath(".//td[@data-stat='pos']//text()").get() in ['DE', 'LDE', 'RDE']:
                draft_meta['Draft_Position'] = 'DE'
            elif row.xpath(".//td[@data-stat='pos']//text()").get() in ['DT', 'LDT', 'RDT', 'NT']:
                draft_meta['Draft_Position'] = 'DT'
            elif row.xpath(".//td[@data-stat='pos']//text()").get() in ['FB', 'RB']:
                draft_meta['Draft_Position'] = 'RB'
            elif row.xpath(".//td[@data-stat='pos']//text()").get() in ['LB', 'LLB', 'MLB', 'RLB', 'LOLB', 'LILB', 'RILB', 'ROLB', 'OLB']:
                draft_meta['Draft_Position'] = 'LB'
            else:
                draft_meta['Draft_Position'] = row.xpath(
                    ".//td[@data-stat='pos']//text()").get()
            draft_meta['Draft_School'] = row.xpath(
                        ".//td[@data-stat='college_id']//text()").get()
            draft_meta['Draft_Team_Selection'] = (idx +1)

            item['Year'] = (int(draft_meta['Year']) - 1)
            item['Team'] = draft_meta['Team']
            item['Draft_Round'] = draft_meta['Draft_Round']
            item['Draft_Pick'] = draft_meta['Draft_Pick']
            item['Draft_Player'] = draft_meta['Draft_Player']
            item['Draft_Position'] = draft_meta['Draft_Position']
            item['Draft_School'] = draft_meta['Draft_School']
            item['Draft_Team_Selection'] = draft_meta['Draft_Team_Selection']
            yield item


