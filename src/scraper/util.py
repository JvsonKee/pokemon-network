from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# scrapes episode list from serebii.net
# returns array of parsed episodes
def scrape_episodes(driver):
    driver.get('https://www.serebii.net/anime/epiguide/')

    parsed_episodes = []

    unwanted = set([1, 300, 301, 318, 319, 412])
    episode_list = driver.find_element(By.XPATH, '//*[@id="content"]/main/table[2]/tbody')
    episodes = episode_list.find_elements(By.TAG_NAME, 'tr')

    for index, episode in enumerate(episodes, start=1):
        if index == len(episodes):
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
    number, title, season_number, season_title = (None, None, None, None)

    try:
        number = episode.find_element(By.XPATH, f'//*[@id="content"]/main/table[2]/tbody/tr[{index}]/td[1]').text

        if not number.isdigit(): return

        title = episode.find_element(By.XPATH, f'//*[@id="content"]/main/table[2]/tbody/tr[{index}]/td[3]/a').text

        season_number, season_title = get_season(int(number))

    except NoSuchElementException as error:
        print(error)

    if index == 980:
        number = 943

    return(number, title, season_number, season_title)

# parses special double episodes
# returns tuple of the first and second special episodes
def parse_double_special_episode(f_episode, s_episode, f_index):
    number, f_title, s_title = (None, None, None)
    f_number, s_number = (None, None)

    try:
        number = f_episode.find_element(By.XPATH, f'//*[@id="content"]/main/table[2]/tbody/tr[{f_index}]/td[1]').text

        f_number, s_number = (f'{number}:1', f'{number}:2')

        f_title = f_episode.find_element(By.XPATH, f'//*[@id="content"]/main/table[2]/tbody/tr[{f_index}]/td[3]/a').text

        s_title = s_episode.find_element(By.XPATH, f'//*[@id="content"]/main/table[2]/tbody/tr[{f_index + 1}]/td[2]/a').text

    except NoSuchElementException as error:
        print(error)

    first = (f_number, f_title)
    second = (s_number, s_title)

    return (first, second)


def get_season(episode_number):
    season_mapping = {
        1: {'episodes': range(1, 84), 'name': 'Indigo League'},
        2: {'episodes': range(84, 119), 'name': 'Adventures in the Orange Islands'},
        3: {'episodes': range(119, 160), 'name': 'The Johto Journeys'},
        4: {'episodes': range(160, 212), 'name': 'Johto League Champions'},
        5: {'episodes': range(212, 277), 'name': 'Master Quest'},
        6: {'episodes': range(277, 317), 'name': 'Advanced'},
        7: {'episodes': range(317, 369), 'name': 'Advanced Challenge'},
        8: {'episodes': range(369, 422), 'name': 'Advanced Battle'},
        9: {'episodes': range(422, 469), 'name': 'Battle Frontier'},
        10: {'episodes': range(469, 521), 'name': 'Diamond and Pearl'},
        11: {'episodes': range(521, 573), 'name': 'Diamond and Pearl: Battle Dimension'},
        12: {'episodes': range(573, 626), 'name': 'Diamond and Pearl: Galactic Battles'},
        13: {'episodes': range(626, 660), 'name': 'Diamond and Pearl: Sinnoh League Victors'},
        14: {'episodes': range(660, 710), 'name': 'Black and White'},
        15: {'episodes': range(710, 759), 'name': 'Black and White: Rival Destinies'},
        16: {'episodes': range(759, 804), 'name': 'Black and White: Adventures in Unova and Beyond'},
        17: {'episodes': range(804, 853), 'name': 'XY'},
        18: {'episodes': range(853, 897), 'name': 'XY: Kalos Quest'},
        19: {'episodes': range(897, 944), 'name': 'XYZ'},
        20: {'episodes': range(944, 987), 'name': 'Sun & Moon'},
        21: {'episodes': range(987, 1036), 'name': 'Sun & Moon: Ultra Adventures'},
        22: {'episodes': range(1036, 1090), 'name': 'Sun & Moon: Ultra Legends'},
        23: {'episodes': range(1090, 1138), 'name': 'Journeys'},
        24: {'episodes': range(1138, 1180), 'name': 'Master Journeys'},
        25: {'episodes': range(1180, 1237), 'name': 'Ultimate Journeys'},
    }

    for season, details in season_mapping.items():
        if episode_number in details['episodes']:
            return (season, details['name'])

    return (None, None)

def scrape_pokemon(driver):
    for i in range(1, 999):
        id = i

        if i > 999:
            id = f'{i}'

        if i < 100:
            id = f'0{i}'

        if i < 10:
            id = f'00{i}'

        print(id)
        driver.get(f'https://www.serebii.net/anime/dex/{id}.shtml')
