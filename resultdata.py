import pandas as pd
import requests

def query_results_data(rounds):
    results = {'season': [], 'round': [], 'circuit_id': [], 'driver': [], 'date_of_birth': [], 'nationality': [], 'constructor': [], 'grid': [], 'time': [], 'status': [], 'points': [], 'podium': []}
    for n in range(len(rounds)):
        for i in rounds[n][1]:
            url = f'http://ergast.com/api/f1/{rounds[n][0]}/{i}/results.json'
            r = requests.get(url)
            json = r.json()
            for item in json['MRData']['RaceTable']['Races'][0]['Results']:
                results['season'].append(json['MRData']['RaceTable']['Races'][0].get('season', None))
                results['round'].append(json['MRData']['RaceTable']['Races'][0].get('round', None))
                results['circuit_id'].append(json['MRData']['RaceTable']['Races'][0]['Circuit'].get('circuitId', None))
                results['driver'].append(item['Driver'].get('driverId', None))
                results['date_of_birth'].append(item['Driver'].get('dateOfBirth', None))
                results['nationality'].append(item['Driver'].get('nationality', None))
                results['constructor'].append(item['Constructor'].get('constructorId', None))
                results['grid'].append(item.get('grid', None))
                results['time'].append(item.get('Time', {}).get('millis', None))
                results['status'].append(item.get('status', None))
                results['points'].append(item.get('points', None))
                results['podium'].append(item.get('position', None))
    return pd.DataFrame(results)

if __name__ == "__main__":
    rounds = [
        [2022, list(range(1, 23))],
        [2023, list(range(1, 23))]
    ]
    results_data = query_results_data(rounds)
    results_data.to_csv('data/results_data.csv', index=False)
