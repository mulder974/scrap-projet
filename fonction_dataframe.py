import numpy as np
import pandas as pd


import seaborn as sns
sns.set_theme(style="whitegrid")

import matplotlib.pyplot as plt
from math import pi

from sklearn import preprocessing



#création des dataframe pour les acteurs, réalisateurs, genres
def create_df_genres(df):
    #GENRES - Création d'un dataframe spécifique
    # create a list of all distinct genres
    genres = ["Action", "Adventure", "Animation", "Biography", "Crime", "Comedy", "Drama", "Fantasy", "History", "Romance", "Sci-Fi", "Thriller", "War"]
    # Step 2 - implement a DF to store values concerning actors
    df_genres = pd.DataFrame()
    for genre in set(genres):
        dic = {}
        intermediate_df = df[df['genre'].str.contains(genre)] # the same syntax as new_df = df[df.col>10]
        dic['Genre'] = genre
        dic["Nombre d'apparitions"] = len(intermediate_df)
        dic["Gains cumulés"] = intermediate_df["gross"].sum()
        dic["Gains moyens"] = intermediate_df["gross"].mean()
        dic["Note moyenne"] = intermediate_df["stars"].mean()
        dic["Nombre de votes"] = intermediate_df["votes"].sum()
        df_genres = df_genres.append(dic, ignore_index = True)
    return df_genres

def add_df_genres(df):
    #GENRES - Rajout des colonnes genre dans le dataframe initial pour viz
    df["genre_action"] = df["genre"].apply(lambda x: "Action" in x)
    df["genre_adventure"] = df["genre"].apply(lambda x: "Adventure" in x)
    df["genre_animation"] = df["genre"].apply(lambda x: "Animation" in x)
    df["genre_biography"] = df["genre"].apply(lambda x: "Biography" in x)
    df["genre_crime"] = df["genre"].apply(lambda x: "Crime" in x)
    df["genre_comedy"] = df["genre"].apply(lambda x: "Comedy" in x)
    df["genre_drama"] = df["genre"].apply(lambda x: "Drama" in x)
    df["genre_fantasy"] = df["genre"].apply(lambda x: "Fantasy" in x)
    df["genre_history"] = df["genre"].apply(lambda x: "History" in x)
    df["genre_romance"] = df["genre"].apply(lambda x: "Romance" in x)
    df["genre_sf"] = df["genre"].apply(lambda x: "Sci-Fi" in x)
    df["genre_thriller"] = df["genre"].apply(lambda x: "Thriller" in x)
    df["genre_war"] = df["genre"].apply(lambda x: "War" in x)
    return df

def create_df_actors(df):
    #ACTEURS
    # Step 1 - create a list for all different actors
    actors = []
    for row in df.actors:
        for actor in row.split(","):
            if actor not in actors:
                actors.append(actor.replace('"','').strip())  

    # Step 2 - implement a DF to store values concerning actors
    df_actors = pd.DataFrame()
    for actor in set(actors):
        dic = {}
        intermediate_df = df[df['actors'].str.contains(actor)] # the same syntax as new_df = df[df.col>10]
        dic['Acteur'] = actor
        dic["Nombre d'apparitions"] = len(intermediate_df)
        dic["Gains cumulés"] = intermediate_df["gross"].sum()
        dic["Gains moyens"] = intermediate_df["gross"].mean()
        dic["Note moyenne"] = intermediate_df["stars"].mean()
        dic["Total votes"] = intermediate_df["votes"].sum()
        dic["Moy votes"] = intermediate_df["votes"].mean()
        df_actors = df_actors.append(dic, ignore_index = True)
    return df_actors
    
def create_df_directors(df):
    #DIRECTORS
    # Step 1 - create a list for all different directors
    directors = []
    for row in df.directors:
        for director in row.split(","):
            if director not in directors:
                directors.append(director.replace('"','').strip())
    print(len(directors))
    print(len(set(directors)))

    # Step 2 - implement a DF to store values concerning actors
    df_directors = pd.DataFrame()
    for director in set(directors):
        dic = {}
        intermediate_df = df[df['directors'].str.contains(director)] # the same syntax as new_df = df[df.col>10]
        dic['Réalisateur'] = director
        dic["Nombre d'apparitions"] = len(intermediate_df)
        dic["Gains cumulés"] = intermediate_df["gross"].sum()
        dic["Gains moyens"] = intermediate_df["gross"].mean()
        dic["Note moyenne"] = intermediate_df["stars"].mean()
        df_directors = df_directors.append(dic, ignore_index = True)
    return df_directors

def create_df_year_mean(df):
    #YEARS - Création de deux dataframes spécifique pour travailler sur les années. Rajout d'une colonne sur la moyenne glissante du runtime
    df_year_mean = df.groupby("year").mean()
    df_year_mean = df_year_mean.reset_index()
    df_year_mean["moyenne_glissante"] = df_year_mean["runtime"].rolling(5).mean()
    return df_year_mean

def make_df_quartile(df):
    df3 = df.sort_values("gross", axis=0, ascending=False)
    liste = []

    df_last_quartile = df3[:63]
    df_third_quartile = df3[63:126]
    df_second_quartile = df3[124:187]
    df_first_quartile = df3[187:]

    liste.append(df_first_quartile)
    liste.append(df_second_quartile)
    liste.append(df_third_quartile)
    liste.append(df_last_quartile)

    liste_group = ['1er quartile','2nd quartile','3eme quartile','dernier quartile']
    liste_durée = []
    liste_votes = []
    liste_score = []
    liste_action = []
    liste_comedy = []
    liste_drame = []
    liste_box_office = []

    for item in liste :
        liste_durée.append(df['runtime'].mean())
        liste_votes.append(df['votes'].mean())
        liste_score.append(df['stars'].mean())
        liste_action.append(df['genre_action'].sum())
        liste_comedy.append(df['genre_comedy'].sum())
        liste_drame.append(df["genre_drama"].sum())
    # Set data
    df4 = pd.DataFrame({
        'quartile':liste_group,
        'durée':liste_durée,
        'votes':liste_votes,
        'score':liste_score,
        "action":liste_action,
        'comedy':liste_comedy,
        'drame':liste_drame,
    })

    df5 = df4
    min_max_scaler = preprocessing.MinMaxScaler()

    array_durée =[120.3968254, 127.03174603, 134.95238095, 135.52380952]
    array_votes =[141218, 321190, 694092, 1031668]
    array_score = [8.244444, 8.277778, 8.298413, 8.377778]
    array_action = [8,5,7,23]
    array_comedy = [12,11,12,9]
    array_drame = [52,49,48,38]

    array_durée = np.array(array_durée).reshape(-1,1)
    array_votes = np.array(array_votes).reshape(-1,1)
    array_score = np.array(array_score).reshape(-1,1)
    array_action = np.array(array_action).reshape(-1,1)
    array_comedy = np.array(array_comedy).reshape(-1,1)
    array_drame = np.array(array_drame).reshape(-1,1)


    array_durée_norm = min_max_scaler.fit_transform(array_durée)+1
    array_votes_norm = min_max_scaler.fit_transform(array_votes)+1
    array_score_norm = min_max_scaler.fit_transform(array_score)+1
    array_action_norm = min_max_scaler.fit_transform(array_action)+1
    array_comedy_norm = min_max_scaler.fit_transform(array_comedy)+1
    array_drame_norm = min_max_scaler.fit_transform(array_drame)+1

    array_durée = array_durée_norm.reshape(-1,1)
    array_votes = array_votes_norm.reshape(-1,1)
    array_score = array_score_norm.reshape(-1,1)
    array_action = array_action_norm.reshape(-1,1)
    array_comedy = array_comedy_norm.reshape(-1,1)
    array_drame = array_drame_norm.reshape(-1,1)

    df5['durée']=array_durée
    df5['score']=array_score
    df5['votes']=array_votes
    df5['action']=array_action
    df5['comedy']=array_comedy
    df5['drame']=array_drame
    return df5


def make_spider(df5, row, title, color) :

    # number of variable(durée, score, vote, box office)
        N = 6

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(2,2,row+1, polar=True, )

        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        #title
        plt.title(title, size=15, color=color, y=1.1)


        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], df5.columns[1:7], color='grey')
        
         # Ind1
        values=df5.loc[row].drop('quartile').values.flatten().tolist()
        values += values[:1]
        ax.set_ylim(0,2)
        ax.plot(angles, values, color=color, linewidth=1, linestyle='solid')
        ax.fill(angles, values, color= color, alpha=0.4)



