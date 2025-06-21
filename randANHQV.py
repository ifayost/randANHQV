import pdb

import argparse
import os
import signal
import sys
import time

from bs4 import BeautifulSoup, BeautifulStoneSoup
import bs4
from credentials import save_credentials, read_credentials
from episodedb import get_episode_database, get_random_episode, reset_statistics, update_statistics
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



CREDS = './credentials'
EPISODES = './episodes.csv'
POWER = 5 # Higher implies less chance choosing already seen episodes
POWER_SEASON = 0.5 # Higher implies more relevance in the normalization

with open('./links.txt', 'r') as f:
    LINKS = f.read().split('\n')[:-1]
LINKS = {l.split(': ')[0]: l.split(': ')[1] for l in LINKS}

def banner():
    banner = r'''
                    __                     __                
 .---.-.-----.--.--|__|   .-----.-----.   |  |--.---.-.--.--.
 |  _  |  _  |  |  |  |   |     |  _  |   |     |  _  |  |  |
 |___._|__   |_____|__|   |__|__|_____|   |__|__|___._|___  |
          |__|__                       __             |_____|
 .-----.--.--|__.-----.-----.   .--.--|__.--.--.---.-.       
 |  _  |  |  |  |  -__|     |   |  |  |  |  |  |  _  |       
 |__   |_____|__|_____|__|__|    \___/|__|\___/|___._|       
    |__|                                                     
        '''
    return banner

def sigint_handler(signum, frame):
    print('\n[!] Good bye.\n')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)


def reject_cookies(driver):
    driver.get('https://www.primevideo.com')
    time.sleep(0.5)
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        if button.get_attribute('data-testid') == 'consent-reject-all':
            button.click()
    time.sleep(0.5)


def login(driver, username, password):
    time.sleep(0.5)
    html = driver.page_source
    html = BeautifulSoup(html, 'html.parser')
    for link in html.find_all('a'):
        if link.has_attr('aria-label'):
            if link['aria-label'] == 'Identificarse':
                break
    link = 'https://primevideo.com/' + link['href']
    driver.get(link)

    time.sleep(0.5)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    for i in inputs:
        if i.get_attribute('type') == 'email':
            i.send_keys(username)
            i.send_keys(Keys.RETURN)
            break
    time.sleep(1)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    for i in inputs:
        if i.get_attribute('type') == 'password':
            i.send_keys(password)
            i.send_keys(Keys.RETURN)
            break
    time.sleep(1)


def get_episode_link(driver, episode):
    elements = driver.find_elements(By.TAG_NAME, 'a')
    episodes = [] 
    for element in elements:
        if element.get_attribute('data-testid') == 'episodes-playbutton':
            link = element.get_attribute('href')
            if link not in episodes:
                episodes.append(link)
    return episodes[int(episode)-1]



if __name__ == '__main__':

    print(banner())

    parser = argparse.ArgumentParser(
            prog='randANHQV',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=banner() + '\nOpen a random ANHQV episode.'
            )
    parser.add_argument(
            '-s', '--seasons', nargs='*', help='Seasons space separated. Ex: --seasons 3 4 5'
            )
    parser.add_argument('--uniform', action='store_true', help='All episodes have the same chancex of being selected')
    parser.add_argument('--nonorm', action='store_true', help='Disable probability normalization among seasons')
    parser.add_argument('--reset-stats', action='store_true', help='Reset episode statistics before selection')
    args = parser.parse_args()
    seasons = args.seasons
    
    if args.reset_stats:
        reset_statistics(filename=EPISODES)

    if seasons is not None:
        seasons = [int(i) for i in seasons]
        assert all(1 <= int(s) <= 6 for s in seasons), f"Seasons {seasons} must be between 1 and 6"
        if  len(seasons) == 0:
            seasons = None

    files = os.listdir('./')

    if EPISODES.split('/')[-1] not in files:
        get_episode_database(LINKS['episode_list'], EPISODES)

    season, episode, title = get_random_episode(
            EPISODES,
            seasons=seasons,
            normalize=not args.nonorm,
            weights=not args.uniform,
            power=POWER,
            p_season=POWER_SEASON
            )

    # password = None
    # if CREDS.split('/')[-1] not in files:
    #     password = save_credentials(CREDS)
    # username, password = read_credentials(password, CREDS)
     
    # driver = webdriver.Safari()
    # driver.implicitly_wait(10)
    #
    # reject_cookies(driver)
    # driver.get(LINKS['anhqv_s'+str(season)])
    # login(driver, username, password)
    # time.sleep(7)
    # episode_link = get_episode_link(driver, episode)
    # driver.get(episode_link)
    # time.sleep(0.5)
    # driver.fullscreen_window()
    #
    
    update_statistics(episode, season, filename=EPISODES)

    # while True:
    #     pass
