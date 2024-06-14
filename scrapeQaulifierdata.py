import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_qualifying_results(start_year=2000, end_year=2023):
    qualifying_results = pd.DataFrame()
    for year in range(start_year, end_year):
        url = f'https://www.formula1.com/en/results.html/{year}/races.html'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        year_links = [page.get('href') for page in soup.find_all('a', class_="resultsarchive-filter-item-link FilterTrigger") if f'/en/results.html/{year}/races/' in page.get('href')]
        year_df = pd.DataFrame()
        for n, link in enumerate(year_links):
            link = link.replace('race-result.html', 'starting-grid.html')
            df = pd.read_html(f'https://www.formula1.com{link}')[0]
            df['season'] = year
            df['round'] = n + 1
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            year_df = pd.concat([year_df, df])
        qualifying_results = pd.concat([qualifying_results, year_df])
    qualifying_results.rename(columns={'Pos': 'grid', 'Driver': 'driver_name', 'Car': 'car', 'Time': 'qualifying_time'}, inplace=True)
    qualifying_results.drop('No', axis=1, inplace=True)
    return qualifying_results

if __name__ == "__main__":
    qualifying_data = scrape_qualifying_results()
    qualifying_data.to_csv('data/qualifying_data.csv', index=False)
