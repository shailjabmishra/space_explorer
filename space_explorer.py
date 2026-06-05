
import json

import yaml
import urllib.request
import psycopg2


def get_connection(db_config:dict):
    try:
        connection = psycopg2.connect(
            host =db_config['host'] ,
            port = db_config['port'],
            dbname = db_config['dbname'],
            user = db_config['user'],
            password = db_config['password']
        )
        return connection
    except Exception as e:
        print("Connection failed",e.__traceback__)
    

def create_table(conn):
    with conn.cursor as cur:
        cur.execute(""" 
            CREATE TABLE IF NOT EXISTS planets (
        id        SERIAL PRIMARY KEY,
        name      VARCHAR(100) UNIQUE NOT NULL,
        distance_from_sun_km BIGINT,
        moons     INTEGER DEFAULT 0,
        fun_fact  TEXT,
        visited   BOOLEAN DEFAULT FALSE
        )
                    """
                )
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS apod_history (
        id         SERIAL PRIMARY KEY,
        title      VARCHAR(255),
        date       VARCHAR(20),
        url        TEXT,
        fetched_at TIMESTAMP DEFAULT NOW()
          )
        """
        )
        conn.commit()

def seed_planets_from_config(conn , planets:list):
    with conn.cursor as cur:
        cur.executemany(
            """
            INSERT  INTO planets (id,name,distance_from_sun_km,moons,fun_fact,visited)
            VALUES(%s,%s,%s,%s,%s)
            """,
            planets
        )
        conn.commit()

def get_all_planets(conn)-> list:
    with conn.cursor as cur:
        cur.execute(
            """
            select id , name , distance_from_sun_km, moons,fun_fact,visited 
            from planets
            """
        )
        rows = cur.fetchall()
        planets_list = [
            {
                "id" : rows[0],
                "name":rows[1],
                "distance_from_sun_km":rows[2],
                "moons":rows[3],
                "fun_fact":rows[4],
                "visited":rows[5]
            }
        ]
    return planets_list


def mark_planet_visited(conn, planet_name: str) -> bool:
    with conn.cursor as cur:
        cur.execute(
            """
            UPDATE planets 
            set visited = TRUE
            where planet_name = %s
            """,
            (planet_name,)
        )
        if cur.rowcount>0:
            return True
        return False
    conn.commit()

def delete_planet(conn, planet_name: str) -> bool:
    with conn.cursor as cur:
        cur.execute(
            """
            DELETE from planets
            where planet_name =%s
            """,
            (planet_name,)
        )
        return cur.rowcount>0
    conn.commit()

def save_apod(conn,apod_data: dict):
    with conn.cursor as cur:
        cur.executemany(
            """
            INSERT  INTO apod_history (id,title,date,url)
            VALUES(%s,%s,%s,%s)
            """,
            apod_data
        )
        conn.commit()

def get_apod_history(conn) -> list:
    with conn.cursor as cur:
        cur.execute(
            """
            select id , title,date,url,fetched_at
            from apod_history
            order by fetched_at desc
            """
        )
        rows = cur.fetchall()
        apod_list = [
            {
                "id" :rows[0],
                "title" : rows[1],
                "date" : rows[2],
                "url" : rows[3],
                "fetched_at" : rows[4]
            }
        ]
    return apod_list

def main():
    def read_config():
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            return config
    CONFIG = read_config()
    db_config = CONFIG['Database']
    planets = CONFIG['planets']
    conn = None
    with urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY") as response:
        data = response.read().decode("utf-8")  # bytes → string
        apod_data = json.loads(data)
    try:
        conn = get_connection(db_config)
        create_table(conn)
        seed_planets_from_config(conn,planets)
        save_apod(conn,apod_data)

        while True:
            print("What would you like to do?")

            print("[1]  Explore a planet")
            print("[2]  Get NASA Astronomy Picture of the Day")
            print("[3]  List all planets")
            print("[4]  Mark a planet as visited")
            print("[5]  Delete a planet")
            print("[6]  View APOD history")
            print("[q]  Quit")
            user_input = input("Enter your choice: ")
            if user_input == "1":
                print("Exploring a planet...")
                which_planet = input("Which planet would you like to explore? ")
                for planet in CONFIG['planets']:
                    if planet["name"].lower() == which_planet.lower():
                        print(f"Name: {planet['name']}")
                        print(f"Distance from Sun: {planet['distance_from_sun_km']} million km")
                        print(f"Number of moons: {planet['moons']}")
                        print(f"Fun fact: {planet['fun_fact']}")
            elif user_input == "2":
                print("Getting NASA Astronomy Picture of the Day...")
                try:
                    
                    print(f"Title: {apod_data['title']}")
                    print(f"date: {apod_data['date']}")
                    print(f"Explanation: {apod_data['explanation'][:300]}")
                except Exception as e:
                    print(f"Error occurred while fetching NASA APOD: {e}")
            elif user_input == "3":
                print("Listing all planets...")
                get_all_planets(conn)
                for planets in planets:
                    print(planets)
            
            elif user_input == '4':
                planet_name = input("Enter the planet you want to visit")
                print("Visiting the planet")
                mark_planet_visited(conn,planet_name)
            
            elif user_input=='5':
                planet_name = input("Enter the planet you want the date to be deleted")
                print("Deleting the planet")
                delete_planet(conn,planet_name)

            elif user_input == '6':
                history = get_apod_history(conn)
                for item in history:
                    print(item['id'])
                    print(['title'])
                    print(item['date'])
                    print(item['url'])
                    print(item['fetched_at'])

            elif user_input == "q":
                print("Quitting...")
                exit(0)
            else:
                print("Unknown option. Please type 1, 2, 3, or q.")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()


   