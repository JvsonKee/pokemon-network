from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# scrapes episode list from serebii.net
# returns array of parsed episodes
def scrape_episodes(driver):
    driver.get("https://www.serebii.net/anime/epiguide/")

    parsed_episodes = []

    unwanted = set([1, 300, 301, 318, 319, 412])
    episode_list = driver.find_element(
        By.XPATH, '//*[@id="content"]/main/table[2]/tbody'
    )
    episodes = episode_list.find_elements(By.TAG_NAME, "tr")

    for index, episode in enumerate(episodes, start=1):
        if index == 1281:
            break

        if unwanted.__contains__(index):
            continue

        parsed = parse_episode(episode, index)

        if parsed is not None:
            parsed_episodes.append(parsed)

    return parsed_episodes


# parses and cleans the necessary data of an episode
# returns episode tuple containing episode number and title
def parse_episode(episode, index):
    number, title, season_number, season_title = (0, None, None, None)

    try:
        str_number = episode.find_element(
            By.XPATH, f'//*[@id="content"]/main/table[2]/tbody/tr[{index}]/td[1]'
        ).text

        if not str_number.isdigit():
            return

        number = int(str_number)

        title = episode.find_element(
            By.XPATH, f'//*[@id="content"]/main/table[2]/tbody/tr[{index}]/td[3]/a'
        ).text

        if "A Sandshrew's Storm! An Ice Hole Double Battle!!" in title:
            number = 1023

        if "Connect to the Future! The Legend of the Blinding One!!" in title:
            number = 1033

        season_number, season_title = get_season(int(number))

    except NoSuchElementException as error:
        print(error)

    if index == 980:
        number = 943

    return (number + 10000, title, season_number, season_title)


# helper function to get the season of an episode
def get_season(episode_number):
    season_mapping = {
        1: {"episodes": range(1, 84), "name": "Indigo League"},
        2: {"episodes": range(84, 119), "name": "Adventures in the Orange Islands"},
        3: {"episodes": range(119, 160), "name": "The Johto Journeys"},
        4: {"episodes": range(160, 212), "name": "Johto League Champions"},
        5: {"episodes": range(212, 277), "name": "Master Quest"},
        6: {"episodes": range(277, 317), "name": "Advanced"},
        7: {"episodes": range(317, 369), "name": "Advanced Challenge"},
        8: {"episodes": range(369, 422), "name": "Advanced Battle"},
        9: {"episodes": range(422, 469), "name": "Battle Frontier"},
        10: {"episodes": range(469, 521), "name": "Diamond and Pearl"},
        11: {"episodes": range(521, 573), "name": "Diamond and Pearl: Battle Dimension"},
        12: {"episodes": range(573, 626), "name": "Diamond and Pearl: Galactic Battles"},
        13: {"episodes": range(626, 660),"name": "Diamond and Pearl: Sinnoh League Victors"},
        14: {"episodes": range(660, 710), "name": "Black and White"},
        15: {"episodes": range(710, 759), "name": "Black and White: Rival Destinies"},
        16: {"episodes": range(759, 804), "name": "Black and White: Adventures in Unova and Beyond"},
        17: {"episodes": range(804, 853), "name": "XY"},
        18: {"episodes": range(853, 897), "name": "XY: Kalos Quest"},
        19: {"episodes": range(897, 944), "name": "XYZ"},
        20: {"episodes": range(944, 987), "name": "Sun & Moon"},
        21: {"episodes": range(987, 1036), "name": "Sun & Moon: Ultra Adventures"},
        22: {"episodes": range(1036, 1090), "name": "Sun & Moon: Ultra Legends"},
        23: {"episodes": range(1090, 1138), "name": "Journeys"},
        24: {"episodes": range(1138, 1180), "name": "Master Journeys"},
        25: {"episodes": range(1180, 1237), "name": "Ultimate Journeys"},
    }

    for season, details in season_mapping.items():
        if episode_number in details["episodes"]:
            return (season, details["name"])

    return (None, None)


# create the edge list of pokemon in episodes
def scrape_pokemon(driver):
    edges = set()

    try:
        for pokemon_index in range(1, 906):
            print(pokemon_index)
            id = get_id(pokemon_index)
            count = 0

            driver.get(f"https://www.serebii.net/anime/dex/{id}.shtml")

            main = driver.find_element(By.TAG_NAME, "main")

            tables = main.find_elements(By.XPATH, "./table")

            # iterate through each table
            for table_index, table in enumerate(tables, start=3):
                if table_index == len(tables):
                    break

                episodes = table.find_elements(
                    By.XPATH, f'//*[@id="content"]/main/table[{table_index}]/tbody/tr'
                )

                for episode_index, episode in enumerate(episodes, start=2):
                    if episode_index == len(episodes):
                        break

                    episode_id = episode.find_element(
                        By.XPATH,
                        f'//*[@id="content"]/main/table[{table_index}]/tbody/tr[{episode_index}]/td[1]',
                    ).text

                    if not episode_id.isdigit():
                        continue

                    href = episode.find_element(
                        By.XPATH,
                        f'//*[@id="content"]/main/table[{table_index}]/tbody/tr[{episode_index}]/td[2]/a',
                    )
                    href_value = href.get_attribute("href")

                    if "pokemon2023" in href_value:
                        continue

                    edges.add((pokemon_index, int(episode_id) + 10000))
                    count += 1

            if count == 0:
                edges.add((pokemon_index, None))

        return edges

    except NoSuchElementException as error:
        print(error)


# helper function to convert pokemon entry number to be used in url
def get_id(index):
    id = index

    if index > 999:
        id = f"{index}"

    if index < 100:
        id = f"0{index}"

    if index < 10:
        id = f"00{index}"

    return id
