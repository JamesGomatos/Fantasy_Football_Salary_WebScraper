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
        csv_writer.writerow(['Name', 'Position', 'Base Salary',  'Roster Bonus', 'Signing Bonus', 'Option Bonus', 'Workout Bonus', 'Restructure Bonus', 'Incentive Bonus', 'Dead Cap', 'Cap Hit', 'Cap %'])
        for key, value in self.database.items():
            source = requests.get(value).text
            soup = BeautifulSoup(source, 'lxml')
            rows = soup.find_all('tr')
            for entry in rows:
                try: 
                  
                    # parse the player name
                    player_name = entry.find('td', class_='player')
                    player_name = player_name.a.text
                    player_name = player_name.replace('\t', " ")
                    player_name = player_name.split(" ")
                    player_name = player_name[0] + " " + player_name[1]

                    # parse the player position 
                    player_position = entry.find('td', class_='center small')
                    player_position = player_position.span.text

                
                    # parse the base salary
                    base_salary = entry.find('td', class_='right result xs-hide')
                    base_salary = base_salary.span.text
                    
                    all_tds = entry.find_all('td', class_='right')
                    for i in all_tds:

                    
                        column1 = i.find('span', {'title': 'Roster Bonus'})
                        column2 = i.find('span', {'title': 'Signing Bonus'})
                        column3 = i.find('span', {'title': 'Option Bonus'})
                        column4 = i.find('span', {'title': 'Workout Bonus'})
                        column5 = i.find('span', {'title': 'Restructure Bonus'})
                        column6 = i.find('span', {'title': 'Incentive Bonus'})
                    
                        if column1 != None:
                            roster_bonus = column1.text
                        if column2 != None:
                            signing_bonus = column2.text
                        if column3 != None:
                            option_bonus = column3.text 
                        if column4 != None:
                            workout_bonus = column4.text
                        if column5 != None:
                            restructure_bonus = column5.text
                        if column6 != None:
                            incentive_bonus = column6.text
                  
                                       

                    # parse the player dead cap 
                    player_dead_cap = entry.find('input', class_='d').get('value')
                    
                    # parse the player cap hit 
                    player_cap = entry.find('td', class_='right result xs-hide')
                    player_cap = player_cap.span.text
               
                    # parse the cap percentage 
                    cap_percentage = entry.find('td', class_='center')
                    cap_percentage = cap_percentage.text

                    # print and write the row to the console
                    print(player_name, player_position, base_salary, roster_bonus, signing_bonus, option_bonus, workout_bonus, restructure_bonus, incentive_bonus, player_dead_cap,  player_cap, cap_percentage)
                    csv_writer.writerow([player_name, player_position, base_salary, roster_bonus, signing_bonus, option_bonus, workout_bonus, restructure_bonus, incentive_bonus, player_dead_cap,  player_cap, cap_percentage])
                              
                except:
                    print("error")
                    continue
        print("Completed :)")
        csv_file.close()

sports = WebScraper('https://www.spotrac.com/nfl/')
sports.get_all_team_info()
# sports.print_db()
sports.get_team_player_info()