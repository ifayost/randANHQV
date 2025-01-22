import pandas as pd
import requests

from bs4 import BeautifulSoup
from io import StringIO



def get_episode_database(link, filename='./episodes.csv'):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    tables = soup.find_all('table')
    tables = [pd.read_html(StringIO(str(tables[i])))[0] for i in range(3, 3+2*5, 2)]
    for i, table in enumerate(tables):
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

    final_table.to_csv(filename, index=False)


def get_random_episode(filename='./episodes.csv', verbose=True):
    episode = pd.read_csv(filename).sample(n=1).values[0]
    if verbose:
        print(f'\n[+]  T{episode[0]} E{episode[1]} - {episode[2][1:-1]}\n')
    return episode
