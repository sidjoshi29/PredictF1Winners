import pandas as pd
import requests

def query_constructor_standings(constructor_rounds):
    constructor_standings = {'season': [], 'round': [], 'constructor': [], 'constructor_points': [], 'constructor_wins': [], 'constructor_standings_pos': []}
    for n in range(len(constructor_rounds)):
        for i in constructor_rounds[n][1]:
            url = f'https://ergast.com/api/f1/{constructor_rounds[n][0]}/{i}/constructorStandings.json'
            r = requests.get(url)
            json = r.json()
            for item in json['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']:
                constructor_standings['season'].append(json['MRData']['StandingsTable']['StandingsLists'][0].get('season', None))
                constructor_standings['round'].append(json['MRData']['StandingsTable']['StandingsLists'][0].get('round', None))
                constructor_standings['constructor'].append(item['Constructor'].get('constructorId', None))
                constructor_standings['constructor_points'].append(item.get('points', None))
                constructor_standings['constructor_wins'].append(item.get('wins', None))
                constructor_standings['constructor_standings_pos'].append(item.get('position', None))
    return pd.DataFrame(constructor_standings)

if __name__ == "__main__":
    # Example constructor rounds data; this should be replaced with actual data
    constructor_rounds = [
        [2022, list(range(1, 23))],
        [2023, list(range(1, 23))]
    ]
    constructor_standings_data = query_constructor_standings(constructor_rounds)
    constructor_standings_data.to_csv('data/constructor_standings_data.csv', index=False)
