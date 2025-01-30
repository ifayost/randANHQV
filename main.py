import os
import signal
import sys
import time

from bs4 import BeautifulSoup, BeautifulStoneSoup
import bs4
from credentials import save_credentials, read_credentials
from episodedb import get_episode_database, get_random_episode
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



CREDS = './credentials'
EPISODES = './episodes.csv'

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
    print(banner)

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

    banner()

    files = os.listdir('./')

    if EPISODES.split('/')[-1] not in files:
        get_episode_database(LINKS['episode_list'], EPISODES)
    season, episode, title = get_random_episode(EPISODES)

    password = None
    if CREDS.split('/')[-1] not in files:
        password = save_credentials(CREDS)
    username, password = read_credentials(password, CREDS)
     
    driver = webdriver.Safari()
    driver.implicitly_wait(10)

    reject_cookies(driver)
    driver.get(LINKS['anhqv_s'+str(season)])
    login(driver, username, password)
    time.sleep(7)
    episode_link = get_episode_link(driver, episode)
    driver.get(episode_link)
    time.sleep(0.5)
    driver.fullscreen_window()

    while True:
        pass
