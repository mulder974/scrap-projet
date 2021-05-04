import sqlite3



def create_table_films():
    con = sqlite3.connect('films.db')

    cur = con.cursor()

    cur.execute('''CREATE TABLE films
                   (id int key, titre text, annee int, note int, votes int, realisateur text, recettes int)''')

    con.commit()

    con.close()

def create_table_acteurs():
    con = sqlite3.connect('films.db')

    cur = con.cursor()

    cur.execute('''CREATE TABLE acteurs
                   (id int primary key, name text)''')


    con.commit()

    con.close()

def create_table_jointure_casting():
    pass
    # con = sqlite3.connect('example.db')
    #
    # cur = con.cursor()
    #
    # cur.execute('''CREATE TABLE stocks
    #                (date text, trans text, symbol text, qty real, price real)''')
    #
    # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    #
    # con.commit()
    #
    # con.close()

create_table_films()
create_table_acteurs()
