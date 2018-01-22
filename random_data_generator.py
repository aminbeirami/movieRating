import psycopg2 as pg
from random import randint
DATABASE = 'movierating'
USERNAME = 'postgres'
PASSWORD = 'amin1234'
SERVER = 'localhost'
setting = "dbname= " + DATABASE+ " user= " + USERNAME + " host=" + SERVER + " password="+ PASSWORD
print setting
conn = pg.connect(setting)
# conn = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
cur = conn.cursor()

def create_Database(): 
  cur.execute("CREATE TABLE IF NOT EXISTS rating (id SERIAL,usr_id INT,mv_name TEXT,rating INT, lat TEXT,long TEXT)")
  conn.commit()
  print 'relevant databases created successfully!'

def records_no():
  cur.execute("SELECT COUNT(*) FROM rating")
  size = cur.fetchone()
  return size[0]

def random_delete():
  random_records = randint(1,records_no())
  cur.execute("DELETE FROM rating WHERE id IN (SELECT id FROM rating ORDER BY RANDOM() LIMIT %s)",(random_records,))
  conn.commit()
  print str(random_records) + " number of records deleted"

def update_records():
  random_records = randint(1,records_no())
  random_rating = randint(1,5)
  cur.execute("UPDATE rating SET rating = (%s) WHERE id IN (SELECT id FROM rating ORDER BY RANDOM() LIMIT %s)",(random_rating,random_records))
  conn.commit()
  print str(random_records) + " number of records updated."

def random_user():
  user_id = randint(1,1000)
  cur.execute("SELECT * FROM users WHERE usr_id = (%s)", (user_id,))
  usr_data = cur.fetchone()
  print usr_data
  return usr_data

def random_movie():
  movie_id = randint(1,1682)
  cur.execute("SELECT mv_name FROM movies WHERE id = (%s)",(movie_id,))
  movie_name = cur.fetchone()
  return movie_name

def insert_rating ():
  random_rating = randint(1,5)
  usr = random_user()
  movie = random_movie()
  cur.execute("INSERT INTO rating(usr_id,mv_name,rating,lat,long) VALUES(%s,%s,%s,%s,%s)",(usr[0],movie[0],random_rating,usr[1],usr[2]))
  print 'the movie '+ movie[0] + ' by user '+str(usr[0])+ ' located at '+ str(usr[1])+ '-'+ str(usr[2])+ ' received '+str(random_rating)+ ' stars.'

def random_data(intervals):
  for i in range (0, intervals):
    number_of_recs = records_no()
    if number_of_recs > 200:
      random_transaction = randint(1,3)
      if random_transaction == 1:
        insert_rating()
      elif random_transaction ==2:
        update_records()
      else:
        random_delete()
      if intervals > 200:
        if i%100 == 0:
          conn.commit()
    else:
      insert_rating()
  conn.commit()

create_Database()
intervals = randint(0,1000)
print str(intervals) + " number of intervals were chosen."
random_data(intervals)

