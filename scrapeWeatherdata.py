# scrape_weather_info.py
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_weather_info(races):
    weather = races[['season', 'round', 'circuit_id']].copy()
    info = []
    for link in races['url']:
        try:
            df = pd.read_html(link)[0]
            if 'Weather' in df.iloc[:, 0].tolist():
                info.append(df.loc[df.iloc[:, 0] == 'Weather', 1].values[0])
            else:
                info.append('not found')
        except:
            info.append('not found')
    weather['weather'] = info
    weather_dict = {'weather_warm': ['soleggiato', 'clear', 'warm', 'hot', 'sunny', 'fine', 'mild', 'sereno'],
                    'weather_cold': ['cold', 'fresh', 'chilly', 'cool'],
                    'weather_dry': ['dry', 'asciutto'],
                    'weather_wet': ['showers', 'wet', 'rain', 'pioggia', 'damp', 'thunderstorms', 'rainy'],
                    'weather_cloudy': ['overcast', 'nuvoloso', 'clouds', 'cloudy', 'grey', 'coperto']}
    weather_df = pd.DataFrame(columns=weather_dict.keys())
    for col in weather_df:
        weather_df[col] = weather['weather'].map(lambda x: 1 if any(i in x.lower() for i in weather_dict[col]) else 0)
    return pd.concat([weather, weather_df], axis=1)

if __name__ == "__main__":
    race_data = pd.read_csv('data/race_data.csv')
    weather_data = scrape_weather_info(race_data)
    weather_data.to_csv('data/weather_data.csv', index=False)
