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
                    {'N.º (serie)': 'Temporada', 'N.º (temp.)': 'Episodio'},
                    axis=1
                    )

            if i < 2:
                table['Temporada'] = i+1
            elif i == 2:
                table.loc[table.Episodio < 14,'Temporada'] = i+1
                table.loc[table.Episodio >= 14,'Temporada'] = i+2
                table.loc[table.Episodio >= 14,'Episodio'] = range(1, 22)
            elif i > 2:
                table['Temporada'] = i+2

            if i == 0:
                final_table = table.copy()
            else:
                final_table = pd.concat([final_table, table], axis=0)
            i += 1

    final_table.to_csv(filename, index=False)


def get_random_episode(filename='./episodes.csv', seasons=None, verbose=True):
    episodes = pd.read_csv(filename)
    if seasons is None:
        episode = episodes.sample(n=1).values[0]
    else:
        episode = episodes[episodes.Temporada.isin(seasons)].sample(n=1).values[0]

    if verbose:
        print(f'\n[+]  T{episode[0]} E{episode[1]} - {episode[2][1:-1]}\n')
    return episode
