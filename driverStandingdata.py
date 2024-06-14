import pandas as pd
import requests

def query_driver_standings(rounds):
    driver_standings = {'season': [], 'round': [], 'driver': [], 'driver_points': [], 'driver_wins': [], 'driver_standings_pos': []}
    for n in range(len(rounds)):
        for i in rounds[n][1]:
            url = f'https://ergast.com/api/f1/{rounds[n][0]}/{i}/driverStandings.json'
            r = requests.get(url)
            json = r.json()
            for item in json['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:
                driver_standings['season'].append(json['MRData']['StandingsTable']['StandingsLists'][0].get('season', None))
                driver_standings['round'].append(json['MRData']['StandingsTable']['StandingsLists'][0].get('round', None))
                driver_standings['driver'].append(item['Driver'].get('driverId', None))
                driver_standings['driver_points'].append(item.get('points', None))
                driver_standings['driver_wins'].append(item.get('wins', None))
                driver_standings['driver_standings_pos'].append(item.get('position', None))
    return pd.DataFrame(driver_standings)

if __name__ == "__main__":
    rounds = [
        [2022, list(range(1, 23))],
        [2023, list(range(1, 23))]
    ]
    driver_standings_data = query_driver_standings(rounds)
    driver_standings_data.to_csv('data/driver_standings_data.csv', index=False)
