import requests
from bs4 import BeautifulSoup


def get_game_films():
    liste_films = []
    for e in range(1,251,50):
        r= requests.get(f"https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start={e}&ref_=adv_nxt")
        print(r.status_code)
        soup = BeautifulSoup(r.text,"html.parser")
        print(soup)
        # game_activities = soup.find_all("tr",class_="player_count_row")
