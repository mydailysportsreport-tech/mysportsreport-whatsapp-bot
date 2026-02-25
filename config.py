"""
Configuration for the WhatsApp bot — available sports, teams, sections.
This mirrors the main report system's config so the bot knows what's valid.
"""

NBA_TEAMS = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
    "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
    "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
    "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
    "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
    "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
    "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
    "Utah Jazz", "Washington Wizards",
]

NBA_SECTIONS = [
    "scores", "team_focus", "top_scorers", "standings",
    "stat_leaders", "todays_games", "three_point_leader",
]

NBA_SECTION_LABELS = {
    "scores": "Yesterday's Scores",
    "team_focus": "Team Box Score",
    "top_scorers": "Top Scorers",
    "standings": "Standings",
    "stat_leaders": "Stat Leaders",
    "todays_games": "Today's Games",
    "three_point_leader": "3-Point Leader",
}

SOCCER_LEAGUES = [
    "Premier League", "La Liga", "Serie A", "Ligue 1", "Bundesliga", "FA Cup",
    "Champions League",
]

SOCCER_SECTIONS = ["results", "today_matches", "standings"]

SOCCER_SECTION_LABELS = {
    "results": "Yesterday's Results",
    "today_matches": "Today's Matches",
    "standings": "Standings",
}

MLS_TEAMS = [
    "Inter Miami", "LAFC", "LA Galaxy", "Atlanta United", "Austin FC",
    "Charlotte FC", "Chicago Fire", "Cincinnati", "Colorado Rapids",
    "Columbus Crew", "D.C. United", "FC Dallas", "Houston Dynamo",
    "Minnesota United", "Montreal", "Nashville SC", "New England Revolution",
    "New York City FC", "New York Red Bulls", "Orlando City",
    "Philadelphia Union", "Portland Timbers", "Real Salt Lake",
    "San Diego FC", "San Jose Earthquakes", "Seattle Sounders", "Sporting KC",
    "St. Louis City", "Toronto FC", "Vancouver Whitecaps",
]

MLS_SECTIONS = ["results", "today_matches", "standings", "team_focus"]

MLS_SECTION_LABELS = {
    "results": "Yesterday's Results",
    "today_matches": "Today's Matches",
    "standings": "Standings",
    "team_focus": "Team Focus",
}

MLB_TEAMS = [
    "Arizona Diamondbacks", "Athletics", "Atlanta Braves", "Baltimore Orioles",
    "Boston Red Sox", "Chicago Cubs", "Chicago White Sox", "Cincinnati Reds",
    "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers", "Houston Astros",
    "Kansas City Royals", "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins",
    "Milwaukee Brewers", "Minnesota Twins", "New York Mets", "New York Yankees",
    "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres",
    "San Francisco Giants", "Seattle Mariners", "St. Louis Cardinals",
    "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals",
]

MLB_DIVISIONS = [
    "AL East", "AL Central", "AL West",
    "NL East", "NL Central", "NL West",
]

MLB_SECTIONS = ["results", "todays_games", "standings", "team_focus"]

MLB_SECTION_LABELS = {
    "results": "Yesterday's Scores",
    "todays_games": "Today's Games",
    "standings": "Standings",
    "team_focus": "Team Focus",
}

NFL_TEAMS = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders",
]

NFL_DIVISIONS = [
    "AFC East", "AFC North", "AFC South", "AFC West",
    "NFC East", "NFC North", "NFC South", "NFC West",
]

NFL_SECTIONS = ["offseason_news", "scores", "standings", "todays_games", "team_focus"]

NFL_SECTION_LABELS = {
    "offseason_news": "Offseason News",
    "scores": "Scores",
    "standings": "Standings",
    "todays_games": "Upcoming Games",
    "team_focus": "Team Focus",
}

WNBA_TEAMS = [
    "Atlanta Dream", "Chicago Sky", "Connecticut Sun", "Dallas Wings",
    "Golden State Valkyries", "Indiana Fever", "Las Vegas Aces",
    "Los Angeles Sparks", "Minnesota Lynx", "New York Liberty",
    "Phoenix Mercury", "Seattle Storm", "Washington Mystics",
]

WNBA_SECTIONS = ["offseason_news", "scores", "standings", "todays_games", "team_focus"]

WNBA_SECTION_LABELS = {
    "offseason_news": "Offseason News",
    "scores": "Yesterday's Scores",
    "standings": "Standings",
    "todays_games": "Today's Games",
    "team_focus": "Team Focus",
}

NWSL_TEAMS = [
    "Angel City FC", "Bay FC", "Chicago Red Stars", "Houston Dash",
    "Kansas City Current", "North Carolina Courage", "NJ/NY Gotham FC",
    "Orlando Pride", "Portland Thorns FC", "Racing Louisville FC",
    "San Diego Wave FC", "Seattle Reign FC", "Utah Royals FC",
    "Washington Spirit",
]

NWSL_SECTIONS = ["offseason_news", "results", "today_matches", "standings", "team_focus"]

NWSL_SECTION_LABELS = {
    "offseason_news": "Offseason News",
    "results": "Yesterday's Results",
    "today_matches": "Today's Matches",
    "standings": "Standings",
    "team_focus": "Team Focus",
}

COLOR_THEMES = ["blue", "green", "red", "purple", "gold", "navy"]

DEFAULT_NBA_SECTIONS = ["scores", "top_scorers", "standings", "todays_games"]
DEFAULT_NBA_SECTIONS_WITH_TEAM = ["scores", "team_focus", "top_scorers", "standings", "todays_games"]
DEFAULT_SOCCER_SECTIONS = ["results", "standings"]
DEFAULT_MLS_SECTIONS = ["results", "today_matches", "standings"]
DEFAULT_MLS_SECTIONS_WITH_TEAM = ["results", "today_matches", "standings", "team_focus"]
DEFAULT_MLB_SECTIONS = ["results", "todays_games", "standings"]
DEFAULT_MLB_SECTIONS_WITH_TEAM = ["results", "todays_games", "standings", "team_focus"]
DEFAULT_NFL_SECTIONS = ["offseason_news"]
DEFAULT_NFL_SECTIONS_WITH_TEAM = ["offseason_news"]
DEFAULT_WNBA_SECTIONS = ["offseason_news"]
DEFAULT_WNBA_SECTIONS_WITH_TEAM = ["offseason_news", "team_focus"]
DEFAULT_NWSL_SECTIONS = ["offseason_news"]
DEFAULT_NWSL_SECTIONS_WITH_TEAM = ["offseason_news", "team_focus"]

SETTINGS_URL = "https://mydailysportsreport.com/signup.html"
