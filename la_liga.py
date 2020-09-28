class Utility:

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