# Necessary Libraries
from bs4 import BeautifulSoup
import requests
import csv 

# source = 'https://www.spotrac.com/nfl/'

# Define my class object
class WebScraper:
    def __init__(self, source, database=None):
        # the source for webscraping
        self.source = source 
        # my db of data
        self.database = {}

    def add_to_db(self, key, val):
        self.database[key] = val
    
    def print_db(self):
        for key, value in self.database.items():
            print(key, value)
            print()

    # Method to scrape and retrieve all the data from the initial page
    def get_page(self):
        source = requests.get(self.source).text
        # Grab the first web page 
        soup = BeautifulSoup(source, 'lxml')
        return soup 

    def get_all_team_info(self):
        page = self.get_page()
        # Get all the data on the first webpage
        teamlist = page.find('div', class_="teamlist")

        # Loop over all the team and gather team name and team link into database dictionary
        for entry in teamlist.find_all('div', class_="teamitem"):
            # Pull the specific team names
            team_name = entry.find('div', class_="teamname")
            team_name = team_name.find('a', class_="team-name").text

            # Pull the specific the links to the specific pages of link 
            team_link = entry.find('div', class_="teamname")
            team_link = team_link.find('a', href=True)['href']

            # add my data 
            self.add_to_db(team_name, team_link)


    def get_team_player_info(self):
        csv_file = open('fantasy_players.csv', 'w')
        csv_writer = csv.writer(csv_file,  lineterminator='\n')
        csv_writer.writerow(['Name', 'Cap Hit'])
        for key, value in self.database.items():
            source = requests.get(value).text
            soup = BeautifulSoup(source, 'lxml')
            rows = soup.find_all('tr')
            for entry in rows:
                try: 
                    # parse the string
                    player_name = entry.find('td', class_='player')
                    player_name = player_name.a.text
                    player_name = player_name.replace('\t', " ")
                    player_name = player_name.split(" ")
                    player_name = player_name[0] + " " + player_name[1]

                    # 
                    player_cap = entry.find('td', class_='right result')
                    player_cap = player_cap.span.text
                    print(player_name, player_cap)
                    csv_writer.writerow([player_name, player_cap])
                except:
                    continue
        print("Completed :)")
        csv_file.close()


sports = WebScraper('https://www.spotrac.com/nfl/')
sports.get_all_team_info()
#sports.print_db()
sports.get_team_player_info()