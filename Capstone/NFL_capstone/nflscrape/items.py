# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NflscrapeItem(scrapy.Item):
    Team = scrapy.Field()
    Year = scrapy.Field()
    Wins = scrapy.Field()
    Losses = scrapy.Field()
    SoS = scrapy.Field()
    MoV = scrapy.Field()
    SRS = scrapy.Field()
    SRS_Off = scrapy.Field()
    SRS_Def = scrapy.Field()
    Coach = scrapy.Field()
    Off_Coor = scrapy.Field()
    Def_Coor = scrapy.Field()
    Off_Scheme = scrapy.Field()
    Def_Align = scrapy.Field()
    Team_PF = scrapy.Field()
    Team_Total_Yards = scrapy.Field()
    Team_Plays_Offense = scrapy.Field()
    Team_yds_per_play_offense = scrapy.Field()
    Team_Turnovers = scrapy.Field()
    Team_Fumbles = scrapy.Field()
    Team_First_down = scrapy.Field()
    Team_Pass_Comp = scrapy.Field()
    Team_Pass_Att = scrapy.Field()
    Team_Pass_Yds = scrapy.Field()
    Team_Pass_Td = scrapy.Field()
    Team_Pass_Int = scrapy.Field()
    Team_Pass_Net_Yds_Att = scrapy.Field()
    Team_Pass_First_Down = scrapy.Field()
    Team_Rush_Att = scrapy.Field()
    Team_Rush_Yds = scrapy.Field()
    Team_Rush_Tds = scrapy.Field()
    Team_Rush_Yds_Att = scrapy.Field()
    Team_Rush_First_Down = scrapy.Field()
    Opp_PF = scrapy.Field()
    Opp_Total_Yards = scrapy.Field()
    Opp_Plays_Offense = scrapy.Field()
    Opp_yds_per_play_offense = scrapy.Field()
    Opp_Turnovers = scrapy.Field()
    Opp_Fumbles = scrapy.Field()
    Opp_First_down = scrapy.Field()
    Opp_Pass_Comp = scrapy.Field()
    Opp_Pass_Att = scrapy.Field()
    Opp_Pass_Yds = scrapy.Field()
    Opp_Pass_Td = scrapy.Field()
    Opp_Pass_Int = scrapy.Field()
    Opp_Pass_Net_Yds_Att = scrapy.Field()
    Opp_Pass_First_Down = scrapy.Field()
    Opp_Rush_Att = scrapy.Field()
    Opp_Rush_Yds = scrapy.Field()
    Opp_Rush_Tds = scrapy.Field()
    Opp_Rush_Yds_Att = scrapy.Field()
    Opp_Rush_First_Down = scrapy.Field()
    Team_Score_Percent = scrapy.Field()
    Opp_Score_Percent = scrapy.Field()
    Week = scrapy.Field()
    Week_Opp = scrapy.Field()
    Week_Points_Scored = scrapy.Field()
    Week_Points_Allowed = scrapy.Field()
    Week_First_Downs = scrapy.Field()
    Week_Total_Off_Yards = scrapy.Field()
    Week_Pass_Yards = scrapy.Field()
    Week_Rush_Yards = scrapy.Field()
    Week_Off_Turnovers = scrapy.Field()
    Week_Def_First_Downs = scrapy.Field()
    Week_Def_Total_Yards = scrapy.Field()
    Week_Def_Pass_Yards = scrapy.Field()
    Week_Def_Rush_Yards = scrapy.Field()
    Week_Def_Turnovers = scrapy.Field()
    Starting_Position = scrapy.Field()
    Starting_Player = scrapy.Field()
    Starting_Player_Age = scrapy.Field()
    Starting_Player_Yrs = scrapy.Field()
    Starting_Player_GS = scrapy.Field()
    Draft_Round = scrapy.Field()
    Draft_Pick = scrapy.Field()
    Draft_Player = scrapy.Field()
    Draft_Position = scrapy.Field()
    Draft_School = scrapy.Field()
    Draft_Team_Selection = scrapy.Field()
    #Draft_Year = scrapy.Field()
    #Draft_Team = scrapy.Field()
