import psycopg2 as pg
import datetime
db = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
cur = db.cursor()
def movie_name_init(allow = False)
	if allow:
		f = open('u.item')
		cur.execute("DROP TABLE IF EXISTS movies")
		cur.execute("DROP SEQUENCE IF EXISTS mv_id")
		cur.execute("CREATE SEQUENCE mv_id")
		cur.execute("CREATE TABLE movies(mov_id INT PRIMARY KEY, mv_name TEXT,mv_year TEXT,release_date TIMESTAMP, movie_url TEXT)")
		db.commit()
		for line in iter(f):
			movie = line.split('|')
			movie_name = movie[1].decode('latin-1').encode("utf-8")
			movie_url = movie[4]
			release_date = movie[2]
			try:
				release_date = datetime.datetime.strptime(release_date, '%d-%b-%Y').date()
			except Exception as e:
				release_date = 'Unknown'
			movie_year = movie[1][-6:].translate(None, '()')

			if movie_year.isdigit():
				movie_year = movie_year
			else:
				movie_year = 'Unknown'
			if release_date != 'Unknown':
				cur.execute("SELECT nextval('mv_id')")
				movie_id = cur.fetchone()[0]
				cur.execute("INSERT INTO movies VALUES (%s,%s,%s,%s,%s)",(movie_id,movie_name,movie_year,release_date,movie_url))
		db.commit()
		f.close()
		cur.close()

username_init(True)