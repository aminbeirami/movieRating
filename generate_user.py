from random import randint
import psycopg2 as pg


conn = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
cur = conn.cursor()

def create_Database():
	cur.execute("DROP TABLE IF EXISTS users")
	conn.commit()
	cur.execute("CREATE TABLE IF NOT EXISTS users (usr_id SERIAL,lat TEXT,long TEXT)")
	conn.commit()
	print 'relevant databases created successfully!'

def choose_random_city():
	random_city = randint(1,3173958)
	cur.execute('SELECT * FROM list_of_cities WHERE id = (%s)', (random_city,))
	coordination = cur.fetchall()
	return coordination

def create_user():
	for i in range (0,10000):
		random_city = choose_random_city()
		cur.execute("INSERT INTO users(lat,long) VALUES (%s,%s)",(random_city[0][1],random_city[0][2]))
		print i
		if i%100==0:
			conn.commit()
			print 'commited'
	conn.commit()
	cur.close()


create_Database()
create_user()