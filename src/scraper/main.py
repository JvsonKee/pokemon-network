from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import util

def main():
    options = Options()
    driver = webdriver.Chrome(options=options)

    print('Scraping...')
    episodes = util.scrape_episodes(driver)
    print('\nScraping completed')

    df = pd.DataFrame(episodes, columns=['episode_number', 'Title', 'season_number', 'season_title'])

    df.index.name = 'id'
    df.to_csv('../../datasets/clean/episode_list.csv')

if __name__ == '__main__':
    main()
