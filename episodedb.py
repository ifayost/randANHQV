import pandas as pd
import requests

from bs4 import BeautifulSoup
from io import StringIO



def get_episode_database(link, filename='./episodes.csv'):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    tables = soup.find_all('table')
    tables = [str(tables[i]) for i in range(3, 13, 1)]
    tables = [t for t in tables if ('Audiencia' in t) | ('Fecha de emisión' in t)]
    tables = [pd.read_html(StringIO(t))[0] for t in tables]
    i = 0
    for table in tables:
        if len(set(['Audiencia', 'Fecha de emisión']) - set(table.columns)) == 0:
            table = table.drop(['Audiencia', 'Fecha de emisión'], axis=1)
            table = table.rename(
                    {'N.º (serie)': 'Season', 'N.º (temp.)': 'Episode'},
                    axis=1
                    )

            if i < 2:
                table['Season'] = i+1
            elif i == 2:
                table.loc[table.Episode < 14,'Season'] = i+1
                table.loc[table.Episode >= 14,'Season'] = i+2
                table.loc[table.Episode >= 14,'Episode'] = range(1, 22)
            elif i > 2:
                table['Season'] = i+2

            if i == 0:
                final_table = table.copy()
            else:
                final_table = pd.concat([final_table, table], axis=0)
            i += 1
    final_table['episode_count'] = 0
    final_table['season_count'] = 0

    final_table.to_csv(filename, index=False)

def compute_probs(episodes, seasons=None, normalize=True, power=1, p_season=1):
    episodes = episodes.copy()
    if 'episode_count' not in episodes.columns:
        episodes['episode_count'] = 0
    if 'season_count' not in episodes.columns:
        episodes['season_count'] = 0

    if seasons is not None:
        episodes = episodes.loc[episodes.Season.isin(seasons)]
    episodes.loc[:, 'pseudo_probs'] = 1 / (1 + episodes['episode_count']) ** power
    if normalize:
        seasons = ([1, 2, 3, 4, 5, 6] if seasons is None else seasons)
        normalize = {
                s: (1 + episodes[episodes.Season != s].groupby('Season')
                .agg({'season_count': 'first'}).sum()['season_count']) ** p_season
                for s in seasons 
                }
        episodes.loc[:, 'pseudo_probs'] = episodes['pseudo_probs'] / episodes['Season'].map(normalize)
    episodes.loc[:, 'probs'] = episodes['pseudo_probs'] / sum(episodes['pseudo_probs'])
    return episodes.drop('pseudo_probs', axis=1)

def get_random_episode(
        filename='./episodes.csv', seasons=None, normalize=True, verbose=True, weights=True,
        power=1, p_season=1
        ):
    episodes = pd.read_csv(filename)
    if weights:
        episodes = compute_probs(episodes, seasons, normalize, power, p_season)
        episode = episodes.sample(n=1, weights=episodes.probs).values[0]
    else:
        seasons = ([1, 2, 3, 4, 5, 6] if seasons is None else seasons)
        episode = episodes[episodes.Season.isin(seasons)].sample(n=1).values[0]
    if verbose:
        print(f'\n[+]  T{episode[0]} E{episode[1]} - {episode[2][1:-1]}\n')

    return episode[:3]

def reset_statistics(filename='./episodes.csv'):
    episodes = pd.read_csv(filename)
    episodes['episode_count'] = 0
    episodes['season_count'] = 0
    episodes.to_csv(filename, index=False)
    print('\n[+]  Successfully reset stats.')

def update_statistics(episode_number, season_number, filename='./episodes.csv', verbose=True):
    episodes = pd.read_csv(filename)
    episode_mask = (episodes['Episode'] == episode_number) & (episodes['Season'] == season_number)
    season_mask = (episodes['Season'] == season_number)
    episodes.loc[episode_mask, 'episode_count'] += 1
    episodes.loc[season_mask, 'season_count'] += 1
    episodes.to_csv(filename, index=False)
    if verbose:
        print(f"[+]  Updated statistics for S{season_number} E{episode_number}\n")
