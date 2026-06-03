
import json

import yaml
import urllib.request
import psycopg2



def read_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        return config
CONFIG = read_config()
def main():
    while True:
        print("What would you like to do?")

        print("[1]  Explore a planet")
        print("[2]  Get NASA Astronomy Picture of the Day")
        print("[3]  List all planets")
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
                with urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY") as response:
                    data = response.read().decode("utf-8")  # bytes → string
                    data_dict = json.loads(data)
                    print(f"Title: {data_dict['title']}")
                    print(f"date: {data_dict['date']}")
                    print(f"Explanation: {data_dict['explanation'][:300]}")
            except Exception as e:
                print(f"Error occurred while fetching NASA APOD: {e}")
        elif user_input == "3":
            print("Listing all planets...")
            for planet in planets:
                print(planet["name"])
        elif user_input == "q":
            print("Quitting...")
            exit(0)
        else:
            print("Unknown option. Please type 1, 2, 3, or q.")

def get_connection(db_config:dict):
    try:
        connection = psycopg2.connect(
            host =db_config['host'] ,
            port = db_config['port'],
            dbname = db_config['dbname'],
            user = db_config['user'],
            password = db_config['password']
        )
    except Exception as e:
        print("Connection failed",e.__traceback__)


main()