import psycopg2 as pg
db = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
c = db.cursor()
f = open('world-cities.txt')
for line in iter(f):
	city = line.split(',')
	c.execute("INSERT INTO list_of_cities(lat,long) VALUES (%s,%s)",(city[5],city[6]))
	print city[5] + '/' + city[6]
db.commit()
f.close()
c.close()