# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from .models import db_connect, create_table, TeamYearSummary, Weeks
import logging


"""class DuplicatesPipeline:
    def __init__(self):
        self.teams_seen = set()

    def process_item(self, item, spider):
        id = item['Team']
        if id in self.teams_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.teams_seen.add(id)
            return item"""


class SavestatsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        logging.info("****SavestatsPipeline: database connected****")

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        teamyearsummary = TeamYearSummary()
        #team = Team()
        #year = Year()
        #coachingstaff = Coachingstaff()
        #summary = Summary()
        weeks = Weeks()
        #player = Player()
        #draft = Draft()

        teamyearsummary.team = item['Team']
        teamyearsummary.year = item['Year']
        teamyearsummary.coach = item['Coach']
        teamyearsummary.offcoor = item['Off_Coor']
        teamyearsummary.defcoor = item['Def_Coor']
        teamyearsummary.offscheme = item['Off_Scheme']
        teamyearsummary.defalign = item['Def_Align']
        #team.name = item['Team']
        #year.year = item['Year']

        #year.year = item['Year']
        #year.year = item['Draft_Year']

        """coachingstaff.Coach = item['Coach']
        coachingstaff.Off_Coor = item['Off_Coor']
        coachingstaff.Def_Coor = item['Def_Coor']
        coachingstaff.Off_Scheme = item['Off_Scheme']
        coachingstaff.Def_Align = item['Def_Align']
        coachingstaff.Team_PF = item['Team_PF']"""

        weeks.Week = item['Week']
        weeks.Week_Opp = item['Week_Opp']
        weeks.Week_Points_Scored = item['Week_Points_Scored']
        weeks.Week_Points_Allowed = item['Week_Points_Allowed']
        weeks.Week_First_Downs = item['Week_First_Downs']
        weeks.Week_Total_Off_Yards = item['Week_Total_Off_Yards']
        weeks.Week_Pass_Yards = item['Week_Pass_Yards']
        weeks.Week_Rush_Yards = item['Week_Rush_Yards']
        weeks.Week_Off_Turnovers = item['Week_Off_Turnovers']
        weeks.Week_Def_First_Downs = item['Week_Def_First_Downs']
        weeks.Week_Def_Total_Yards = item['Week_Def_Total_Yards']
        weeks.Week_Def_Pass_Yards = item['Week_Def_Pass_Yards']
        weeks.Week_Def_Rush_Yards = item['Week_Def_Rush_Yards']
        weeks.Week_Def_Turnovers = item['Week_Def_Turnovers']

        #starters.Starting_Position = item['Starting_Position']
        #starters.Starting_Player = item['Starting_Player']
        #starters.Starting_Player_Age = item['Starting_Player_Age']
        #starters.Starting_Player_Yrs = item['Starting_Player_Yrs']
        #starters.Starting_Player_GS = item['Starting_Player_GS']

        """summary.Wins = item['Wins']
        summary.Losses = item['Losses']
        summary.MoV = item['MoV']
        summary.SoS = item['SoS']
        summary.SRS = item['SRS']
        summary.SRS_Off = item['SRS_Off']
        summary.SRS_Def = item['SRS_Def']
        summary.Team_PF = item['Team_PF']
        summary.Team_Total_Yards = item['Team_Total_Yards']
        summary.Team_Plays_Offense = item['Team_Plays_Offense']
        summary.Team_yds_per_play_offense = item['Team_yds_per_play_offense']
        summary.Team_Turnovers = item['Team_Turnovers']
        summary.Team_Fumbles = item['Team_Fumbles']
        summary.Team_First_down = item['Team_First_down']
        summary.Team_Pass_Comp = item['Team_Pass_Comp']
        summary.Team_Pass_Att = item['Team_Pass_Att']
        summary.Team_Pass_Yds = item['Team_Pass_Yds']
        summary.Team_Pass_Td = item['Team_Pass_Td']
        summary.Team_Pass_Int = item['Team_Pass_Int']
        summary.Team_Pass_Net_Yds_Att = item['Team_Pass_Net_Yds_Att']
        summary.Team_Pass_First_Down = item['Team_Pass_First_Down']
        summary.Team_Rush_Att = item['Team_Rush_Att']
        summary.Team_Rush_Yds = item['Team_Rush_Yds']
        summary.Team_Rush_Tds = item['Team_Rush_Tds']
        summary.Team_Rush_Att = item['Team_Rush_Yds_Att']
        summary.Team_Rush_First_Down = item['Team_Rush_First_Down']
        summary.Opp_PF = item['Opp_PF']
        summary.Opp_Total_Yards = item['Opp_Total_Yards']
        summary.Opp_Plays_Offense = item['Opp_Plays_Offense']
        summary.Opp_yds_per_play_offense = item['Opp_yds_per_play_offense']
        summary.Opp_Turnovers = item['Opp_Turnovers']
        summary.Opp_Fumbles = item['Opp_Fumbles']
        summary.Opp_First_down = item['Opp_First_down']
        summary.Opp_Pass_Comp = item['Opp_Pass_Comp']
        summary.Opp_Pass_Att = item['Opp_Pass_Att']
        summary.Opp_Pass_Yds = item['Opp_Pass_Yds']
        summary.Opp_Pass_Td = item['Opp_Pass_Td']
        summary.Opp_Pass_Int = item['Opp_Pass_Int']
        summary.Opp_Pass_Net_Yds_Att = item['Opp_Pass_Net_Yds_Att']
        summary.Opp_Pass_First_Down = item['Opp_Pass_First_Down']
        summary.Opp_Rush_Att = item['Opp_Rush_Att']
        summary.Opp_Rush_Yds = item['Opp_Rush_Yds']
        summary.Opp_Rush_Tds = item['Opp_Rush_Tds']
        summary.Opp_Rush_Att = item['Opp_Rush_Yds_Att']
        summary.Opp_Rush_First_Down = item['Opp_Rush_First_Down']

        #draft.Year = item['Draft_Year']
        #draft.Round = item['Draft_Round']
        #draft.Pick = item['Draft_Pick']
        #draft.Drafted_Player = item['Draft_Player']
        #draft.Draft_Position = item['Draft_Position']
        #draft.Draft_School = item['Draft_School']
        #draft.Team_Selection = item['Draft_Team_Selection']
        #draft.Team = item['Draft_Team']

        player.name = item['Starting_Player']
        player.Position = item['Starting_Position']
        #player.name = item['Draft_Player']
        #player.Position = item['Draft_Position']
        player.age = item['Starting_Player_Age']"""

        """exist_year = session.query(Year).filter_by(year=year.year).first()
        if exist_team is not None:
            team.year = exist_team
        else:
            team.year = year

        exist_ = session.query().filter_by().Opp_First_down
        if exist_ is not None:
            = exist_
        else:
        
        exist_ = session.query().filter_by().Opp_First_down
        if exist_ is not None:
            = exist_
        else:"""

        try:
            session.add_all([teamyearsummary, weeks])

            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class NflscrapePipeline:
    def process_item(self, item, spider):
        return item
