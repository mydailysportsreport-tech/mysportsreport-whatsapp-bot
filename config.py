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
]

SOCCER_SECTIONS = ["results", "today_matches", "standings"]

SOCCER_SECTION_LABELS = {
    "results": "Yesterday's Results",
    "today_matches": "Today's Fixtures",
    "standings": "Standings",
}

MLS_TEAMS = [
    "Inter Miami", "LAFC", "LA Galaxy", "Atlanta United", "Austin FC",
    "Charlotte FC", "Chicago Fire", "Cincinnati", "Colorado Rapids",
    "Columbus Crew", "D.C. United", "FC Dallas", "Houston Dynamo",
    "Minnesota United", "Montreal", "Nashville SC", "New England Revolution",
    "New York City FC", "New York Red Bulls", "Orlando City",
    "Philadelphia Union", "Portland Timbers", "Real Salt Lake",
    "San Jose Earthquakes", "Seattle Sounders", "Sporting KC",
    "St. Louis City", "Toronto FC", "Vancouver Whitecaps",
]

MLS_SECTIONS = ["results", "team_focus"]

COLOR_THEMES = ["blue", "green", "red", "purple", "gold", "navy"]

DEFAULT_NBA_SECTIONS = ["scores", "top_scorers", "standings", "todays_games"]
DEFAULT_NBA_SECTIONS_WITH_TEAM = ["scores", "team_focus", "top_scorers", "standings", "todays_games"]
DEFAULT_SOCCER_SECTIONS = ["results", "standings"]
DEFAULT_MLS_SECTIONS = ["results", "team_focus"]

SETTINGS_URL = "https://mydailysportsreport.com/signup.html"
