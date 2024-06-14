import pandas as pd
from dateutil.relativedelta import relativedelta

def merge_data():
    races = pd.read_csv('data/race_data.csv')
    results = pd.read_csv('data/results_data.csv')
    driver_standings = pd.read_csv('data/driver_standings_data.csv')
    constructor_standings = pd.read_csv('data/constructor_standings_data.csv')
    qualifying = pd.read_csv('data/qualifying_data.csv')
    weather = pd.read_csv('data/weather_data.csv')


    print("Columns in races:", races.columns)
    print("Columns in results:", results.columns)
    print("Columns in driver_standings:", driver_standings.columns)
    print("Columns in constructor_standings:", constructor_standings.columns)
    print("Columns in qualifying:", qualifying.columns)
    print("Columns in weather:", weather.columns)

    df1 = pd.merge(races, weather, how='inner', on=['season', 'round', 'circuit_id']).drop(['lat', 'long', 'country', 'weather'], axis=1)
    df2 = pd.merge(df1, results, how='inner', on=['season', 'round', 'circuit_id']).drop(['points', 'status', 'time'], axis=1)
    df3 = pd.merge(df2, driver_standings, how='left', on=['season', 'round', 'driver'])
    df4 = pd.merge(df3, constructor_standings, how='left', on=['season', 'round', 'constructor'])
    final_df = pd.merge(df4, qualifying, how='inner', on=['season', 'round', 'grid']).drop(['driver_name', 'car'], axis=1)

    final_df['date'] = pd.to_datetime(final_df['date'])
    final_df['date_of_birth'] = pd.to_datetime(final_df['date_of_birth'])
    final_df['driver_age'] = final_df.apply(lambda x: relativedelta(x['date'], x['date_of_birth']).years, axis=1)
    final_df = final_df.drop(['date', 'date_of_birth'], axis=1)

    for col in ['driver_points', 'driver_wins', 'driver_standings_pos', 'constructor_points', 'constructor_wins', 'constructor_standings_pos']:
        final_df[col] = final_df[col].fillna(0).astype(int)

    final_df = final_df.dropna()

    for col in ['weather_warm', 'weather_cold', 'weather_dry', 'weather_wet', 'weather_cloudy']:
        final_df[col] = final_df[col].astype(bool)

    final_df['qualifying_time'] = final_df['qualifying_time'].map(lambda x: 0 if str(x) == '00.000' else (float(str(x).split(':')[1]) + (60 * float(str(x).split(':')[0])) if x != 0 else 0))
    final_df = final_df[final_df['qualifying_time'] != 0]
    final_df = final_df.sort_values(['season', 'round', 'grid'])
    final_df['qualifying_time_diff'] = final_df.groupby(['season', 'round'])['qualifying_time'].diff()
    final_df['qualifying_time'] = final_df.groupby(['season', 'round'])['qualifying_time'].cumsum().fillna(0)
    final_df = final_df.drop('qualifying_time_diff', axis=1)

    df_dum = pd.get_dummies(final_df, columns=['circuit_id', 'nationality', 'constructor'])

    cols_to_drop = [col for col in df_dum.columns if ('nationality' in col and df_dum[col].sum() < 140) or
                    ('constructor' in col and df_dum[col].sum() < 140) or
                    ('circuit_id' in col and df_dum[col].sum() < 70)]

    df_dum = df_dum.drop(columns=cols_to_drop)

    df_dum.to_csv('data/final_data.csv', index=False)

if __name__ == "__main__":
    merge_data()
