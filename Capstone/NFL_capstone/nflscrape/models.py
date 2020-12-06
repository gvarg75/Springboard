from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings
from sqlalchemy.sql.schema import ForeignKeyConstraint, UniqueConstraint

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


# Association tables
# starter_table = Table('Starter', Base.metadata,
 #                     Column('year_id', String(35), ForeignKey('year.id')),
  #                    Column('player_id', Integer, ForeignKey('player.id'))
   #                   )

# team_year_table = Table('team_year', Base.metadata,
#                        Column('team_id', Integer, ForeignKey('team.id')),
#                        Column('year_id', Integer, ForeignKey('year.id')))

class TeamYearSummary(Base):
    __tablename__ = 'teamyearsummary'
    __table_args__ = (UniqueConstraint(
        'team', 'year', sqlite_on_conflict='IGNORE'),)
    id = Column(Integer, primary_key=True)
    team = Column('team', String(35))
    year = Column('year', Integer)
    coach = Column('coach', String(35))
    offcoor = Column('offcoor', String(35))
    defcoor = Column('defcoor', String(35))
    offscheme = Column('offscheme', String(35))
    defalign = Column('defalign', String(35))


class Weeks(Base):
    __tablename__ = 'weeks'
    __table_args__ = (UniqueConstraint(
                                       'Team','Year', 'Week', sqlite_on_conflict='IGNORE'),)
    id = Column(Integer, primary_key=True)
    Team = Column('Team', String(35))
    Year = Column('Year', Integer) 
    Week = Column('Week', Integer)
    WeekOpp = ('Week_Opp', String(35))
    Week_Points_Scored = Column('Week_Points_Scored', Integer)
    Week_Points_Allowed = Column('Week_Points_Allowed', Integer)
    Week_First_Downs = Column('Week_First_Downs', Integer)
    Week_Total_Off_Yards = Column('Week_Total_Off_Yards', Integer)
    Week_Pass_Yards = Column('Week_Pass_Yards', Integer)
    Week_Rush_Yards = Column('Week_Rush_Yards', Integer)
    Week_Off_Turnovers = Column('Week_Off_Turnovers', Integer)
    Week_Def_First_Downs = Column('Week_Def_First_Downs', Integer)
    Week_Def_Total_Yards = Column('Week_Def_Total_Yards', Integer)
    Week_Def_Pass_Yards = Column('Week_Def_Pass_Yards', Integer)
    Week_Def_Rush_Yards = Column('Week_Def_Rush_Yards', Integer)
    Week_Def_Turnovers = Column('Week_Def_Turnovers', Integer)


"""class Team(Base):
    __tablename__ = 'team'
    #__table_args__ = (UniqueConstraint('name', sqlite_on_conflict='IGNORE'),)
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(35), unique=True,)
    year_child = relationship(
        "Year", secondary=team_year_table, backref="team_parent")
    UniqueConstraint('')"""


"""class Year(Base):
    __tablename__ = 'year'
    __table_args__ = (UniqueConstraint('year', sqlite_on_conflict='IGNORE'),)
    id = Column('id', Integer, primary_key=True)
    year = Column('year', Integer, unique=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    #coaching_staff_child = relationship("Coachingstaff", backref="year")
    # draft = relationship('Draft')"""


"""class Coachingstaff(Base):
    __tablename__ = 'coachingstaff'
    id = Column(Integer, primary_key=True)
    year_id = Column(Integer, ForeignKey('year.id'))
    Coach = Column('Coach', String(35))
    Off_Coor = Column('Off_Coor', String(35))
    DefCoor = Column('Def_Coor', String(35))
    OffScheme = Column('Off_Scheme', String(35))
    DefScheme = Column('Def_Align', String(35))
    summary_child = relationship('Summary', backref="coachingstaff")


class Summary(Base):
    __tablename__ = 'summary'
    id = Column(Integer, primary_key=True)
    coaching_staff_id = Column(Integer, ForeignKey('coachingstaff.id'))
    Wins = Column('Wins', Integer)
    Losses = Column('Losses', Integer)
    MoV = Column('MoV', Integer)
    SoS = Column('SoS', Float)
    SRS = Column('SRS', Float)
    SRS_Off = Column('SRS_Off', Float)
    SRS_Def = Column('SRS_Def', Float)
    Team_PF = Column('Team_PF', Integer)
    Team_Total_Yards = Column('Team_Total_Yards', Integer)
    Team_Plays_Offense = Column('Team_Plays_Offense', Integer)
    Team_yds_per_play_offense = Column('Team_yds_per_play_offense', Integer)
    Team_Turnovers = Column('Team_Turnovers', Integer)
    Team_Fumbles = Column('Team_Fumbles', Integer)
    Team_First_down = Column('Team_First_down', Integer)
    Team_Pass_Comp = Column('Team_Pass_Comp', Integer)
    Team_Pass_Att = Column('Team_Pass_Att', Integer)
    Team_Pass_Yds = Column('Team_Pass_Yds', Integer)
    Team_Pass_Td = Column('Team_Pass_Td', Integer)
    Team_Pass_Int = Column('Team_Pass_Int', Integer)
    Team_Pass_Net_Yds_Att = Column('Team_Pass_Net_Yds_Att', Integer)
    Team_Pass_First_Down = Column('Team_Pass_First_Down', Integer)
    Team_Rush_Att = Column('Team_Rush_Att', Integer)
    Team_Rush_Yds = Column('Team_Rush_Yds', Integer)
    Team_Rush_Tds = Column('Team_Rush_Tds', Integer)
    Team_Rush_Yds_Att = Column('Team_Rush_Yds_Att', Integer)
    Team_Rush_First_Down = Column('Team_Rush_First_Down', Integer)

    Opp_PF = Column('Opp_PF', Integer)
    Opp_Total_Yards = Column('Opp_Total_Yards', Integer)
    Opp_Plays_Offense = Column('Opp_Plays_Offense', Integer)
    Opp_yds_per_play_offense = Column('Opp_yds_per_play_offense', Integer)
    Opp_Turnovers = Column('Opp_Turnovers', Integer)
    Opp_Fumbles = Column('Opp_Fumbles', Integer)
    Opp_First_down = Column('Opp_First_down', Integer)
    Opp_Pass_Comp = Column('Opp_Pass_Comp', Integer)
    Opp_Pass_Att = Column('Opp_Pass_Att', Integer)
    Opp_Pass_Yds = Column('Opp_Pass_Yds', Integer)
    Opp_Pass_Td = Column('Opp_Pass_Td', Integer)
    Opp_Pass_Int = Column('Opp_Pass_Int', Integer)
    Opp_Pass_Net_Yds_Att = Column('Opp_Pass_Net_Yds_Att', Integer)
    Opp_Pass_First_Down = Column('Opp_Pass_First_Down', Integer)
    Opp_Rush_Att = Column('Opp_Rush_Att', Integer)
    Opp_Rush_Yds = Column('Opp_Rush_Yds', Integer)
    Opp_Rush_Tds = Column('Opp_Rush_Tds', Integer)
    Opp_Rush_Yds_Att = Column('Opp_Rush_Yds_Att', Integer)
    Opp_Rush_First_Down = Column('Opp_Rush_First_Down', Integer)
    weeks = relationship("Weeks", backref="summary")"""


"""class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    Name = Column('Player', String(50))
    Age = Column('Starting_Player_Age', Integer)
    Position = Column('Position', String(50))
    # draft = relationship("Draft")


class Draft(Base):
    __tablename__ = 'draft'
    id = Column(Integer, primary_key=True)
    year_id = Column(Integer, ForeignKey('year.id'))
    Draft_Player = Column(Integer, ForeignKey('player.id'))
    Draft_Round = Column('Draft_Round', Integer)
    Draft_Pick = Column('Draft_Pick', Integer)
    Draft_Position = Column('Draft_Position', String(35))
    Draft_School = Column('Draft_School', String(35))
    Draft_Team_Selection = Column('Draft_Team_Selection', Integer)
    Draft_Team = Column('Draft_Team', String(35))"""
