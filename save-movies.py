import psycopg2 as pg
db = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
cur = db.cursor()
f = open('u.item')

cur.execute("DROP TABLE IF EXISTS movies")
db.commit()

cur.execute("CREATE TABLE movies(id SERIAL, mv_name TEXT)")

for line in iter(f):
	movie = line.split('|')
	mv_name = movie[1].decode('latin-1').encode("utf-8")
	cur.execute("INSERT INTO movies(mv_name) VALUES (%s)",(mv_name,))
	print movie[1]+'\n'
db.commit()
f.close()
cur.close()