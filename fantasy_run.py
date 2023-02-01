import pandas as pd
import numpy as np
from scipy import stats
from espn_api.football import League

#Private Info

leagueid = ''
cookie = ''
swid = ''

Function and class definitions
#Class for each owner

# Ignore for now. Implement later
# class TeamRoster:
#     df = 3

# teamroster parameter removed for now
class FantasyTeam:
    def __init__(self, name):
        self.name = name
        # self.teamroster = teamroster
    

    #career stats
    years = 0
    games = 0
    wins = 0
    losses = 0
    winperc = 0
    pf_ranks = []
    pf_avg_ranks = 0
    pa_per_g = 0

    #career superlatives
    highestpf = 0
    lowestpf = 10000
    
    #post season related
    playoff_app = 0
    playoff_wins = 0
    playoff_losses = 0
    championships = 0
    #z-score related
    win_per_z = 0
    playoff_win_z = 0
    playoff_app_z = 0
    avg_pfrank_z = 0
    truevalue = 0



#Function to find the owners FantasyTeam object within an array
def findTeam(array, findteam):
    for team in array:
        if team.name == findteam:
            return team
#Function used to give Connor stats from the time he shared a team with Brett
def connorShare(match, team_list, winloss, homeaway):
    connor = findTeam(team_list, "Connor Hess")
    if winloss:
        connor.wins += 1
    else:
        connor.losses += 1
    connor.games += 1
    if homeaway:
        connor.pa_per_g += match.away_score
    else:
        connor.pa_per_g += match.home_score

#If the home team wins in the regular season
def reghomeWin(match, team_list):
    home = findTeam(team_list, match.home_team.owner)
    away = findTeam(team_list, match.away_team.owner)
    home.wins += 1
    away.losses += 1
    home.games += 1
    away.games += 1
    home.pa_per_g += match.away_score
    away.pa_per_g += match.home_score
    if match.home_score > home.highestpf:
        home.highestpf = match.home_score
    if match.away_score > away.highestpf:
        away.highestpf = match.away_score
    if match.home_score < home.lowestpf:
        home.lowestpf = match.home_score
    if match.away_score < away.lowestpf:
        away.lowestpf = match.away_score

#If a team loses in the regular season
def regawayWin(match, team_list):
    home = findTeam(team_list, match.home_team.owner)
    away = findTeam(team_list, match.away_team.owner)
    away.wins += 1
    home.losses += 1
    home.games += 1
    away.games += 1
    home.pa_per_g += match.away_score
    away.pa_per_g += match.home_score
    if match.home_score > home.highestpf:
        home.highestpf = match.home_score
    if match.away_score > away.highestpf:
        away.highestpf = match.away_score
    if match.home_score < home.lowestpf:
        home.lowestpf = match.home_score
    if match.away_score < away.lowestpf:
        away.lowestpf = match.away_score

#If a team ties in the regular season
def regTie(match, team_list):
    home = findTeam(team_list, match.home_team.owner)
    away = findTeam(team_list, match.away_team.owner)
    home.wins += 0.5
    away.losses += 0.5
    away.wins += 0.5
    home.losses += 0.5
    home.games += 1
    away.games += 1
    home.pa_per_g += match.away_score
    away.pa_per_g += match.home_score
    if match.home_score > home.highestpf:
        home.highestpf = match.home_score
    if match.away_score > away.highestpf:
        away.highestpf = match.away_score
    if match.home_score < home.lowestpf:
        home.lowestpf = match.home_score
    if match.away_score < away.lowestpf:
        away.lowestpf = match.away_score


#Initialize each fantasy team
joey_dicresce = FantasyTeam("joey DiCresce")
joel_fazecas = FantasyTeam("joel faze")
cameron_limke = FantasyTeam("Cameron Limke")
ben_urbano = FantasyTeam("Ben Urbano")
dillon_hong = FantasyTeam("Dillon Hong")
chris_jenkins = FantasyTeam("chris jenkins")
jack_dunn = FantasyTeam("jack dunn")
nick_durand = FantasyTeam("Nick Durand")
brett_nixon = FantasyTeam("Brett Nixon")
connor_hess = FantasyTeam("Connor Hess")
marco_dicresce = FantasyTeam("Marco DiCresce")
nabil_chamra = FantasyTeam("Nabil Chamra")
jack_mooney = FantasyTeam("John Sneg")
will_myers = FantasyTeam("Will Myers")
carson_tuscany = FantasyTeam("Joanne Tuscany")

team_list = np.array([joey_dicresce, joel_fazecas, cameron_limke, ben_urbano, dillon_hong, chris_jenkins, jack_dunn, nick_durand, brett_nixon, connor_hess, marco_dicresce, nabil_chamra, jack_mooney, will_myers, carson_tuscany])



########################################################################################################################
########################################################################################################################
########################################################################################################################


##      Main Code       ##
select_years = [2014,2015,2016,2017,2018,2019,2020,2021,2022]
for year in select_years:
    #Initialize each year
    league_year = year
    league = League(league_id=leagueid, year=league_year, espn_s2=cookie, swid=swid)

#adding pf and how many years played
    fantasy_season = pd.DataFrame()
    for league_team in league.teams:
        for team in team_list:
            if team.name == league_team.owner:
                team.years += 1
                team_pf = pd.DataFrame([[league_team.owner, league_team.points_for]], columns=['team', 'pf'])
                fantasy_season = pd.concat([fantasy_season, team_pf], sort=True)
        
    fantasy_season['rank'] = fantasy_season['pf'].rank(method='max', ascending= False)

    for team in team_list:
        for index, row in fantasy_season.iterrows():
            if team.name == row[1]:
                if team.pf_ranks == []:
                    team.pf_ranks = [row[2]]
                    # Conor and Brett share team
                    if year == 2015 and row[1] == "Brett Nixon":
                        connor_hess.pf_ranks = [row[2]]
                else:
                    team.pf_ranks.append(row[2])

#2014-2018 have to use scoreboard class
    if year < 2019:
        for week in range(1,17):
            boxscore = league.scoreboard(week)
            for match in boxscore:
                if not match.is_playoff:
                    if match.home_score > match.away_score:
                        reghomeWin(match, team_list)
                        #Connor and Brett share team
                        if (year == 2015):
                            if match.home_team.owner == "Brett Nixon":
                                connorShare(match, team_list, True, True)
                            if match.away_team.owner == "Brett Nixon":
                                connorShare(match, team_list, False, False)
                    elif match.home_score < match.away_score:
                        regawayWin(match, team_list)
                        #Connor and Brett share team
                        if (year == 2015):
                            if match.home_team.owner == "Brett Nixon":
                                connorShare(match, team_list, False, True)
                            if match.away_team.owner == "Brett Nixon":
                                connorShare(match, team_list, True, False)
                    else:
                        regTie(match, team_list)
                elif match.is_playoff & (match.matchup_type == 'WINNERS_BRACKET'):
                    for team in team_list:
                        if week == 14:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name:
                                    team.playoff_app += 1
                                    if match.home_score > match.away_score:
                                        team.playoff_wins += 1
                            if match.away_team != 0:
                                if match.away_team.owner == team.name:
                                    team.playoff_app += 1
                                    if match.away_score > match.home_score:
                                        team.playoff_wins += 1
                        elif week == 16:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name and match.home_score > match.away_score:
                                    team.playoff_wins += 1
                                    team.championships += 1
                            if match.home_team != 0:
                                if match.away_team.owner == team.name and match.away_score > match.home_score:
                                    team.playoff_wins += 1
                                    team.championships += 1
                        else:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name and match.home_score > match.away_score:
                                    team.playoff_wins += 1
                            if match.home_team != 0:
                                if match.away_team.owner == team.name and match.away_score > match.home_score:
                                    team.playoff_wins += 1
#2019-2020 have to use box scores
    elif year < 2021:
        for week in range(1,17):
            boxscore = league.box_scores(week)
            for match in boxscore:
                if not match.is_playoff:
                    if match.home_score > match.away_score:
                        reghomeWin(match, team_list)
                    elif match.home_score < match.away_score:
                        regawayWin(match, team_list)
                    else:
                        regTie(match, team_list)
                elif match.is_playoff & (match.matchup_type == 'WINNERS_BRACKET'):
                    for team in team_list:
                        if week == 14:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name:
                                    team.playoff_app += 1
                                    if match.home_score > match.away_score:
                                        team.playoff_wins += 1
                            if match.away_team != 0:
                                if match.away_team.owner == team.name:
                                    team.playoff_app += 1
                                    if match.away_score > match.home_score:
                                        team.playoff_wins += 1
                        elif week == 16:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name and match.home_score > match.away_score:
                                    team.playoff_wins += 1
                                    team.championships += 1
                            if match.home_team != 0:
                                if match.away_team.owner == team.name and match.away_score > match.home_score:
                                    team.playoff_wins += 1
                                    team.championships += 1
                        else:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name and match.home_score > match.away_score:
                                    team.playoff_wins += 1
                            if match.home_team != 0:
                                if match.away_team.owner == team.name and match.away_score > match.home_score:
                                    team.playoff_wins += 1
#2021 and on games were increased to 14 regular season games
    else:
        for week in range(1,18):
            boxscore = league.box_scores(week)
            for match in boxscore:
                if not match.is_playoff:
                    if match.home_score > match.away_score:
                        reghomeWin(match, team_list)
                    elif match.home_score < match.away_score:
                        regawayWin(match, team_list)
                    else:
                        regTie(match, team_list)
                elif match.is_playoff & (match.matchup_type == 'WINNERS_BRACKET'):
                    for team in team_list:
                        if week == 15:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name:
                                    team.playoff_app += 1
                                    if match.home_score > match.away_score:
                                        team.playoff_wins += 1
                            if match.away_team != 0:
                                if match.away_team.owner == team.name:
                                    team.playoff_app += 1
                                    if match.away_score > match.home_score:
                                        team.playoff_wins += 1
                        elif week == 17:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name and match.home_score > match.away_score:
                                    team.playoff_wins += 1
                                    team.championships += 1
                            if match.home_team != 0:
                                if match.away_team.owner == team.name and match.away_score > match.home_score:
                                    team.playoff_wins += 1
                                    team.championships += 1
                        else:
                            if match.home_team != 0:
                                if match.home_team.owner == team.name and match.home_score > match.away_score:
                                    team.playoff_wins += 1
                            if match.home_team != 0:
                                if match.away_team.owner == team.name and match.away_score > match.home_score:
                                    team.playoff_wins += 1



########################################################################################################################


## z-scores
current_team_list = np.array([joey_dicresce, joel_fazecas, cameron_limke, ben_urbano, dillon_hong, chris_jenkins, jack_dunn, nick_durand, brett_nixon, connor_hess, marco_dicresce, nabil_chamra])

for team in current_team_list:
    team.pf_avg_ranks = np.mean(team.pf_ranks)
    team.winperc = team.wins / (team.wins + team.losses)
    team.pa_per_g = team.pa_per_g / team.games

arr = []
for team in current_team_list:
    arr.append(team.winperc)
wp_z_arr = stats.zscore(arr)
for index in range(0,current_team_list.size):
    current_team_list[index].win_per_z = wp_z_arr[index]
arr = []
for team in current_team_list:
    arr.append(team.playoff_wins)
pw_z_arr = stats.zscore(arr)
for index in range(0,current_team_list.size):
    current_team_list[index].playoff_win_z = pw_z_arr[index]
arr = []
for team in current_team_list:
    arr.append(team.playoff_app/team.years)
pa_z_arr = stats.zscore(arr)
for index in range(0,current_team_list.size):
    current_team_list[index].playoff_app_z = pa_z_arr[index]
arr = []
for team in current_team_list:
    arr.append(team.pf_avg_ranks)
pf_z_arr = stats.zscore(arr)
for index in range(0,current_team_list.size):
    current_team_list[index].avg_pfrank_z = -1 * pf_z_arr[index]

#Organize Final Data
final_data = pd.DataFrame()

for team in current_team_list:
    team.truevalue = team.win_per_z + (team.playoff_win_z * 1.35) + team.championships + (team.playoff_app_z * 0.25)+  team.avg_pfrank_z
    team_data = pd.DataFrame([[team.name, team.truevalue, team.wins, team.losses, team.winperc, team.pf_avg_ranks, team.pf_ranks, team.playoff_app, team.playoff_wins, team.championships, team.highestpf, team.lowestpf, team.pa_per_g]], columns=['team', 'truevalue', 'wins', 'losses', 'win per', 'average pf rank', 'pf ranks','playoff app', 'playoff wins', 'championships', 'highest pf', 'lowest pf', 'pa per g'])
    final_data = pd.concat([final_data, team_data], sort=True)

final_data['TRUE Rank'] = final_data['truevalue'].rank(method='max', ascending= False)

final_data.to_csv('finaldata.csv')

########################################################################################################################
########################################################################################################################
########################################################################################################################
##       Printing to Console     ##
# print("----------------------------------")
# print("---------------")
# for team in current_team_list:
#     print("*******************")
#     print("name: ",team.name)
#     print("win percentage: ",team.winperc)
#     print("losses: ", team.losses)
#     print("average pf rank: ",team.pf_avg_ranks)
#     print("playoff appearances: ",team.playoff_app)
#     print("playoff wins: ",team.playoff_wins)
#     print("championships: ",team.championships)
#     print("-----------------------")
#     print("win per z: ",team.win_per_z)
#     print("playoff win z: ",team.playoff_win_z)
#     print("playoff app z: ",team.playoff_app_z)
#     print("average pf rank z: ",team.avg_pfrank_z)
#     print("truevalue: ",team.truevalue)
#     print("highest pf: ", team.highestpf)
#     print("lowest pf: ", team.lowestpf)
#     print("pa per g: ", team.pa_per_g)