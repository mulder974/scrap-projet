import requests
from bs4 import BeautifulSoup

import csv

import pandas as pd

all_results = [] # initialize a list to store results for all pages together
for i in range(1,251,50):
    page = f"https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start={i}&ref_=adv_nxt"
    response = requests.get(page)  
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        movies = soup.find_all("div", "lister-item-content") # parse html looking for each movie container
        for movie in movies:
            movie_results = {} # initialize a dictionnary to store each film result.
            movie_results["title"] = movie.h3.a.text 
            movie_results["year"] = year = movie.h3.find("span", "lister-item-year").text.replace(")","").replace("(","").replace("I","")
            movie_results["stars"] = movie.div.div.strong.text 
            # certificate
            try:
                movie_results["certificate"] = movie.find("p", "text-muted").find("span", "certificate").text # OK
            except:
                movie_results["certificate"] = None
            # runtime
            runtime = movie.find("p", "text-muted").find("span", "runtime").text 
            runtime = runtime.replace(" min","")
            movie_results["runtime"] = runtime
            movie_results["genre"] = genre = movie.find("p", "text-muted").find("span", "genre").text.replace("\"","").strip()
            # votes and gross
            numbers = movie.find("p", "sort-num_votes-visible")
            try:
                votes = numbers.find_all("span")[1].text
                movie_results["votes"] = votes.replace(",","")
            except:
                movie_results["votes"] = None
            try:
                gross = numbers.find_all("span")[4].text
                gross = gross.replace("$","")
                gross = gross.replace("M","")
                movie_results["gross"] = gross
            except:
                movie_results["gross"] = None
            # actors
            actors = movie.find_all("p")[2].text.split("|")[1]
            actors = actors.split(":")[1]
            actors = actors.replace("\n","")
            actors = actors.replace(" \n","")
            actors = actors.strip()
            actors = actors.split(",")
            actors = (str(actors)).strip("[]").replace("'","")
            movie_results["actors"] = actors
            # directors
            directors = movie.find_all("p")[2].text.split("|")[0]
            directors = directors.split(":")[1]
            directors = directors.replace("\n","")
            directors = directors.replace(" \n","")
            directors = directors.strip()
            directors = directors.split(",")
            directors = (str(directors)).strip("[]").replace("'","")
            movie_results["directors"] = directors
            # add each dictionnary of my current page to list   
            all_results.append(movie_results) 
    else:
        print(f"problème lors de la requête HTTP :{response}")
#return all_results




with open("movies.csv", "w") as output_file:
    keys = all_results[0].keys()
    writer = csv.DictWriter(output_file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(all_results)



