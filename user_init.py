import keyGen as kg
import psycopg2 as pg
import random
db = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
cur = db.cursor()
username = []
def city_max():
	cur.execute("SELECT id FROM list_of_cities ORDER BY id DESC LIMIT 1")
	result = cur.fetchone()
	return result[0]

def return_city(random_city):
	cur.execute('SELECT * FROM list_of_cities WHERE id = (%s)', (random_city,))
	coordination = cur.fetchone()
	return coordination

def username_dbinit(allow = False):
	if allow:
		f = open('half_million.txt')
		cur.execute("DROP TABLE IF EXISTS users")
		cur.execute("DROP SEQUENCE IF EXISTS user_id")
		cur.execute("CREATE SEQUENCE user_id")
		cur.execute("CREATE TABLE users(user_id INT PRIMARY KEY, username TEXT,private_key TEXT, public_key TEXT,lat TEXT ,long TEXT)")
		db.commit()
		for line in iter(f):
			username.append(line)

def insert_username():
	keyGen = kg.RSAEncryption()
	rand_usr = random.sample(xrange(1,len(username)), 5000)
	rand_city = random.sample(xrange(1,city_max()),5000)
	for i in range(0,5000):
		user = username[rand_usr[i]]
		city = return_city(rand_city[i])
		latitude = city[1]
		longitude = city[2].translate(None,'\n')
		publickey, privatekey = keyGen.generate_keys()
		cur.execute("SELECT nextval('user_id')")
		user_id = cur.fetchone()[0]
		user_attribs = [user_id,user,privatekey,publickey,latitude,longitude]
		cur.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s)",user_attribs)
		if i%100 == 0:
			db.commit()
			print i
	cur.close()
if __name__=="__main__":
	username_dbinit(False)
	insert_username()