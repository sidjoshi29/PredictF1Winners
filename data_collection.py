import pandas as pd
import requests

BASE_URL = "https://api.openf1.org/v1"


def get_json_response(endpoint, params):
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    return response.json()


def fetch_data(year=2023):
    # Fetch data for races
    races_params = {"year": year}
    races_data = get_json_response("meetings", races_params)
    races_df = pd.DataFrame(races_data)

    # Print the DataFrame columns and first few rows to inspect
    print("Races DataFrame Columns: ", races_df.columns)
    print(races_df.head())

    # Fetch data for drivers
    drivers_data = []
    for index, row in races_df.iterrows():
        meeting_key = row['meeting_key']
        drivers_params = {"meeting_key": meeting_key}
        drivers_data.extend(get_json_response("drivers", drivers_params))
    drivers_df = pd.DataFrame(drivers_data)

    # Fetch data for qualifying
    qualifying_data = []
    for index, row in races_df.iterrows():
        meeting_key = row['meeting_key']
        qualifying_params = {"meeting_key": meeting_key}
        qualifying_data.extend(get_json_response("laps", qualifying_params))

        qualifying_df = pd.DataFrame(qualifying_data)

        # Fetch data for driver standings
        driver_standings_data = []
        for index, row in races_df.iterrows():
            meeting_key = row['meeting_key']
            standings_params = {"meeting_key": meeting_key}
            driver_standings_data.extend(get_json_response("intervals", standings_params))
        driver_standings_df = pd.DataFrame(driver_standings_data)

        # Fetch data for constructor standings
        constructor_standings_data = []
        for index, row in races_df.iterrows():
            meeting_key = row['meeting_key']
            standings_params = {"meeting_key": meeting_key}
            constructor_standings_data.extend(get_json_response("intervals", standings_params))
        constructor_standings_df = pd.DataFrame(constructor_standings_data)

        # Fetch weather data
        weather_data = []
        for index, row in races_df.iterrows():
            meeting_key = row['meeting_key']
            weather_params = {"meeting_key": meeting_key}
            weather_data.extend(get_json_response("weather", weather_params))
        weather_df = pd.DataFrame(weather_data)

        # Save data to CSV files
        races_df.to_csv('races.csv', index=False)
        drivers_df.to_csv('drivers.csv', index=False)
        qualifying_df.to_csv('qualifying.csv', index=False)
        driver_standings_df.to_csv('driver_standings.csv', index=False)
        constructor_standings_df.to_csv('constructor_standings.csv', index=False)
        weather_df.to_csv('weather.csv', index=False)

        return races_df, drivers_df, qualifying_df, driver_standings_df, constructor_standings_df, weather_df

    if __name__ == "__main__":
        fetch_data()

