
import pandas as pd
import requests

def query_race_data(start_year=1950, end_year=2024):
    races = {'season': [], 'round': [], 'circuit_id': [], 'lat': [], 'long': [], 'country': [], 'date': [], 'url': []}
    for year in range(start_year, end_year):
        url = f'https://ergast.com/api/f1/{year}.json'
        r = requests.get(url)
        json = r.json()
        for item in json['MRData']['RaceTable']['Races']:
            races['season'].append(item.get('season', None))
            races['round'].append(item.get('round', None))
            races['circuit_id'].append(item['Circuit'].get('circuitId', None))
            races['lat'].append(item['Circuit']['Location'].get('lat', None))
            races['long'].append(item['Circuit']['Location'].get('long', None))
            races['country'].append(item['Circuit']['Location'].get('country', None))
            races['date'].append(item.get('date', None))
            races['url'].append(item.get('url', None))
    return pd.DataFrame(races)

if __name__ == "__main__":
    race_data = query_race_data()
    race_data.to_csv('data/race_data.csv', index=False)
