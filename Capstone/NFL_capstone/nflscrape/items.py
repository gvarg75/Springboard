# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NflscrapeItem(scrapy.Item):
    Team = scrapy.Field()
    Year = scrapy.Field()
    Url = scrapy.Field()
    #Coach = scrapy.Field()
    #Off_Coor = scrapy.Field()
    #Def_Coor = scrapy.Field()
    SRS = scrapy.Field()
    SoS = scrapy.Field()
    Wins = scrapy.Field()
    MoV = scrapy.Field()
    SRS_Off = scrapy.Field()
    SRS_Def = scrapy.Field()
    #Off_Scheme = scrapy.Field()
    #Def_Align = scrapy.Field()
    #Team_PF = scrapy.Field()
    #Team_Y_P = scrapy.Field()
    #Team_Pass_Cmp = scrapy.Field()
    #Team_Pass_Att = scrapy.Field()
    #Team_Pass_Yds = scrapy.Field()
    #Team_Pass_TD = scrapy.Field()
    #Team_Int = scrapy.Field()
    #Team_Pass_NY_A = scrapy.Field()
    #Team_Rush_Att = scrapy.Field()
    #Team_Rush_Yds = scrapy.Field()
    #Team_Rush_TD = scrapy.Field()
    #Team_Rush_Y_A = scrapy.Field()
    #Opp_PF = scrapy.Field()
    #Opp_Y_P = scrapy.Field()
    #Opp_Pass_Cmp = scrapy.Field()
    #Opp_Pass_Att = scrapy.Field()
    #Opp_Pass_Yds = scrapy.Field()
    #Opp_Pass_TD = scrapy.Field()
    #Opp_Int = scrapy.Field()
    #Opp_Pass_NY_A = scrapy.Field()
    #Opp_Rush_Att = scrapy.Field()
    #Opp_Rush_Yds = scrapy.Field()
    #Opp_Rush_TD = scrapy.Field()
    #Opp_Rush_Y_A = scrapy.Field()


class SeasoncrawlItem(scrapy.Item):
    Team = scrapy.Field()
    Year = scrapy.Field()
    Wins = scrapy.Field()
    MoV = scrapy.Field()
    SoS = scrapy.Field()
    SRS = scrapy.Field()
    SRS_Off = scrapy.Field()
    SRS_Def = scrapy.Field()
    Points = scrapy.Field()
