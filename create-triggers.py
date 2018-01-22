import psycopg2 as pg


conn = pg.connect("dbname='movierating' user='postgres' host='localhost' password='amin123'")
cur = conn.cursor()

def create_log():
	cur.execute("DROP TABLE IF EXISTS timeline")
	conn.commit()
	cur.execute('''CREATE TABLE timeline(
		id SERIAL,
		r_id INT,
		username TEXT,
		movie_name TEXT,
		rating INT,
		lat TEXT,
		long TEXT,
		ttime TIMESTAMP DEFAULT NOW(),
		deleted BOOLEAN DEFAULT FALSE)''')
	conn.commit()
	print "log table created."

def create_triggers():
	cur.execute("DROP TRIGGER IF EXISTS base_data_log ON rating")
	cur.execute("DROP FUNCTION IF EXISTS log_data()")
	cur.execute('''
		CREATE FUNCTION log_data()
		RETURNS TRIGGER
		LANGUAGE PLPGSQL
		AS
		$$
		  BEGIN
		    IF (TG_OP = 'DELETE') THEN
		        INSERT INTO timeline (r_id, username, movie_name, rating, lat, long, ttime, deleted)
		        SELECT OLD.id, NULL, NULL, NULL, NULL, NULL, NULL, TRUE;
		        RETURN OLD;
		    ELSIF (TG_OP = 'UPDATE') THEN
		        INSERT INTO timeline (r_id,username, movie_name, rating, lat, long, ttime, deleted)
		        SELECT NEW.id, NEW.usr_id, NEW.mv_name, NEW.rating,NEW.lat,NEW.long,NOW(),FALSE;
		        RETURN NEW;
		    ELSIF (TG_OP = 'INSERT') THEN
		        INSERT INTO timeline (r_id, username, movie_name, rating, lat, long, ttime, deleted)
		        SELECT NEW.id, NEW.usr_id, NEW.mv_name, NEW.rating,NEW.lat,NEW.long,NOW(),FALSE;
		        RETURN NEW;
		    END IF;
		    RETURN NULL;
		  END;
		$$;
		''')
	conn.commit()
	print 'function created.'

	cur.execute('''
		CREATE TRIGGER base_data_log
		AFTER INSERT OR UPDATE OR DELETE ON rating
		FOR EACH ROW EXECUTE PROCEDURE log_data()
		''')
	conn.commit()
	print 'trigger turned on.'

create_log()
create_triggers()
