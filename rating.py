from random import randint
import psycopg2 as pg


conn = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
cur = conn.cursor()

def create_Database():
	cur.execute("DROP TABLE IF EXISTS rating")
	conn.commit()
	cur.execute("CREATE TABLE IF NOT EXISTS rating (id SERIAL,usr_id INT,mv_name TEXT,rating INT, lat TEXT,long TEXT)")
	conn.commit()
	print 'relevant databases created successfully!'

def random_user():
	user_id = randint(0,1000)
	cur.execute("SELECT * FROM users WHERE usr_id = (%s)", (user_id,))
	usr_data = cur.fetchone()
	print usr_data
	return usr_data

def random_movie():
	movie_id = randint(0,1682)
	cur.execute("SELECT mv_name FROM movies WHERE id = (%s)",(movie_id,))
	movie_name = cur.fetchone()
	return movie_name

def rating ():
	random_rating = randint(1,5)
	usr = random_user()
	movie = random_movie()
	cur.execute("INSERT INTO rating(usr_id,mv_name,rating,lat,long) VALUES(%s,%s,%s,%s,%s)",(usr[0],movie[0],random_rating,usr[1],usr[2]))
	print 'the movie '+ movie[0] + ' by user '+str(usr[0])+ ' located at '+ str(usr[1])+ '-'+ str(usr[2])+ ' received '+str(random_rating)+ ' stars.'
create_Database()
for i in range(0,100):
	rating()
	conn.commit()
