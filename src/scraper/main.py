from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import util


def main():
    options = Options()
    options.page_load_strategy = "eager"
    driver = webdriver.Chrome(options=options)

    print("Scraping...")

    # scrape episodes
    # episodes = util.scrape_episodes(driver)
    #
    # episodes_df = pd.DataFrame(
    #     episodes, columns=["Id", "Label", "season_number", "season_title", "node_type"]
    # )
    # episodes_df.to_csv("../../datasets/clean/episodes.csv", index=False)
    #
    # # scrape for pokemon in each episode
    # edges = util.scrape_pokemon(driver)
    #
    # edge_df = pd.DataFrame(list(edges), columns=["Source", "Target"])
    # edge_df.to_csv("../../datasets/clean/edge_list.csv", index=False).astype("Int64")

    # scrape episode ratings
    ratings = util.scrape_ratings(driver)
    ratings_df = pd.DataFrame(list(ratings), columns=["season", "episode", "rating"])
    ratings_df.to_csv("../../datasets/clean/ratings.csv", index=False)

    print("\nScraping completed")


if __name__ == "__main__":
    main()
