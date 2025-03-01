from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import util

def main():
    options = Options()
    driver = webdriver.Chrome(options=options)

    print('Scraping...')

    # scrape episodes
    episodes = util.scrape_episodes(driver)

    episodes_df = pd.DataFrame(episodes, columns=['Id', 'Label', 'season_number', 'season_title'])
    episodes_df.to_csv('../../datasets/clean/episode_list.csv', index=False)

    # scrape for pokemon in each episode
    edges = util.scrape_pokemon(driver)

    edge_df = pd.DataFrame(list(edges), columns=['Source', 'Target'])
    edge_df.to_csv('../../datasets/clean/edge_list.csv', index=False)

    print('\nScraping completed')

if __name__ == '__main__':
    main()
