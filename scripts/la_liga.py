import pandas

class Utility:

    """
        class blueprint that contains utility methods working with the datasets
    """

    @staticmethod
    def average(col: any) -> float:
        return sum(col) / len(col)

    @staticmethod
    def extract_team_wins(df, source: str, col: str, name: str,mode: str="H") -> int:
        """extracts a team from a column
        
        df: the dataframe we want to extract the team -> pandas DataFrame

        source: the name of the column we want to split the dataframe from -> str

        col: the name of the column we wish to extract from -> str
        
        name: the name of the team we want to extract -> str
        """
        names = df[df[source] == name]
        temp = names[col]
        res = 0
        for item in temp:
            if item == mode:
                res += 1
        return res

    @staticmethod
    def count(df,source: str,col,team: str) -> int:
        """computes the sum of the required column specified
           
           df : the source dataframe -> pandas DataFrame
           
           source: the source column to extract the team
           
           col: the name of the column we wish to get the sum
           
           team: the name of the team
           
           returns: the sum of the specified column
           
           :rtype int
        """
        matches = df[df[source] == team]
        return matches[col].sum()

    @staticmethod
    def get_goal_difference(df,source: str, col: str, against: str, team: str) -> tuple:
        """computes the goal difference for a team
        
           df: the dataframe we wish to use -> pandas DataFrame
           
           col: the goal scored by the team
           
           against: the goal scored against the team
           
           team: the team we are computing for
           
           :retrns -> a tuple of the goal difference, goals scored and goals against
        """
        matches = df[df[source] == team]
        goal_scored = matches[col].sum()
        goal_against = matches[against].sum()
        return goal_scored - goal_against, goal_scored, goal_against


    @staticmethod
    def create_league_table(df: pandas.DataFrame) -> pandas.DataFrame:
        """
        creates league table from datasets by calculating the required statistics

        wins -> number of wins

        loss -> number of losses

        draws -> numer of draws

        points -> points gathered

        goals_scored -> number of goal scored

        goals_conceded -> number of goals conceded

        goals_difference -> the differnce between goals scored and goals conceded

        rturns:

            res -> dataframe representing the league
        """
        home = list(df["HomeTeam"].unique())
        res = pandas.DataFrame(index=range(1,21))
        wins = []
        loss = []
        draws = []
        points = []
        goals_scored = []
        goals_conceded = []
        goals_difference = []
        for team in home:
            home_wins = Utility.extract_team_wins(df,"HomeTeam","FTR",team)
            home_losses = Utility.extract_team_wins(df,"HomeTeam","FTR",team,mode="A")
            away_wins = Utility.extract_team_wins(df,"AwayTeam","FTR",team,mode="A")
            away_losses = Utility.extract_team_wins(df,"AwayTeam","FTR",team)

            total_wins = home_wins + away_wins
            total_loss = home_losses + away_losses
            total_draws = 38 - (total_wins + total_loss)
            wins.append(total_wins)
            loss.append(total_loss)
            draws.append(38 - total_wins + total_loss)
            points.append((total_wins * 3) + total_draws)

            home_goal_diff,home_goal_scored,home_goal_against = Utility.get_goal_difference(df,"HomeTeam","FTHG","FTAG",team)
            away_goal_diff,away_goal_scored,away_goal_against = Utility.get_goal_difference(df,"AwayTeam","FTAG","FTHG",team)

            goals_scored.append(home_goal_scored + away_goal_scored)
            goals_conceded.append(home_goal_against + away_goal_against)
            goals_difference.append(home_goal_diff + away_goal_diff)

        res["Team"] = home
        res["Pld"] = [38 for _ in range(20)]
        res["W"] = wins
        res["D"] = draws
        res["L"] = loss
        res["GF"] = goals_scored
        res["GA"] = goals_conceded
        res["GD"] = goals_difference
        res["Pts"] = points

        res = res.sort_values(by="Pts",axis=0,ascending=False)
        res.set_index(pandas.Index(range(1,21)),inplace=True)

        return res