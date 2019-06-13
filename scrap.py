    # parse the string
                    player_name = entry.find('td', class_='player')
                    player_name = player_name.a.text
                    player_name = player_name.replace('\t', " ")
                    player_name = player_name.split(" ")
                    player_name = player_name[0] + " " + player_name[1]

                    # parse the player position 
                    player_position = entry.find('td', class_='center small')
                    player_position = player_position.span.text

                    # parse the base salary
                    base_salary = entry.find('td', class_='right xs-hide')
                    base_salary = base_salary.span.text

                    values = entry.find_all('td')
                    print(values)

                    # parse the player cap hit 
                    player_cap = entry.find('td', class_='right result')
                    player_cap = player_cap.span.text

                    roster_bonus = 0
                    print(player_name, player_position, base_salary, roster_bonus, player_cap)
                    csv_writer.writerow([player_name, player_position, base_salary, roster_bonus, player_cap])