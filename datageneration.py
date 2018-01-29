import psycopg2 as pg
import datetime
from random import randint, randrange
import keyGen as kg

insert = 0
updte = 0
delete = 1

db = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
c = db.cursor()

def init_db(flush=False):
	if flush:
		c.execute("DROP TABLE IF EXISTS timeline")
        c.execute("DROP SEQUENCE IF EXISTS id")
        db.commit()
        c.execute("CREATE SEQUENCE id")
        c.execute("""
             CREATE TABLE timeline AS
             SELECT NEXTVAL('id') AS id,
                   movies.*,
                   0 AS star,
                   0 AS user_id,
                   ' ' AS username,
                   ' ' AS signature,
                   0 as __flag__,
                   current_timestamp as __t__
                   FROM movies
                   LIMIT 0
            """)
        c.execute("alter table timeline add primary key (id)")
        c.execute("ALTER TABLE timeline ALTER COLUMN username TYPE TEXT")
        c.execute("ALTER TABLE timeline ALTER COLUMN signature TYPE TEXT")
        db.commit()

def sign(user_dict,movie_dict,rate):
	keyGen = kg.RSAEncryption()
	movie_message = str(movie_dict['movie_id'])+str(movie_dict['movie_name'])+str(movie_dict['movie_year'])+ \
	str(movie_dict['release_date'])+str(movie_dict['url'])
	user_message = str(user_dict['user_id']) + str(user_dict['username'])
	message_all = movie_message+str(rate)+user_message
	signature = keyGen.generate_signature(message_all,user_dict['private_key'])
	return signature
def get_timeline_atts():
	c.execute("SELECT * FROM timeline LIMIT 1")
	result = [col.name for col in c.description]
	return result

def max_userid():
	c.execute("SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1")
	result = c.fetchone()[0]
	return result

def max_movieid():
	c.execute("SELECT mov_id FROM movies ORDER BY mov_id DESC LIMIT 1")
	result = c.fetchone()[0]
	return result

def select_user(max_userid):
	user_id = randint(1,max_userid)
	c.execute("SELECT * FROM users WHERE user_id = (%s)",(user_id,))
	result = c.fetchone()
	return result

def select_movie(max_movieid):
	movie_id = randint(1,max_movieid)
	c.execute("SELECT * FROM movies WHERE mov_id = (%s)",(movie_id,))
	result = c.fetchone()
	return result

def create_dictionary(user,movie):
	user_dict = {'user_id':user[0],'username':user[1].translate(None,'\n'),'private_key':user[2],'public_key':user[3], \
	'latitude':user[4],'longitude':user[5]}
	movie_dict = {'movie_id':movie[0],'movie_name':movie[1],'movie_year':movie[2],'release_date':movie[3],'url':movie[4]}
	return user_dict,movie_dict

def random_date(start):
   current = start
   curr = current + datetime.timedelta(hours=randrange(48000), seconds = randrange(86400))
   return curr

def random_push(timeline_id, user_dict, movie_dict, rate, signature,ttime,action):
	attr = get_timeline_atts()
	sql = "INSERT INTO timeline VALUES (%s)" %",".join("%s" for i in range(len(attr)))
	timeline_touple = (timeline_id,movie_dict['movie_id'],movie_dict['movie_name'],movie_dict['movie_year'], \
	movie_dict['release_date'],movie_dict['url'],rate,user_dict['user_id'],user_dict['username'],signature,action,ttime)
	c.execute(sql,timeline_touple)

def random_action():
	max_user = max_userid()
	max_movie = max_movieid()
	for i in xrange(1,1000):
		user = select_user(max_user)
		movie = select_movie(max_movie)
		rate = randint(1,5)
		user_dict, movie_dict = create_dictionary(user,movie)
		signature = sign(user_dict,movie_dict,rate)
		ttime = random_date(datetime.datetime(2013, 01, 01))
		c.execute("SELECT nextval('id')")
		timeline_id = c.fetchone()[0]
		random_push(timeline_id,user_dict,movie_dict,rate,signature,ttime,insert)
		if (i%10 == 0):
			db.commit()
			print i


init_db(True)
random_action()
