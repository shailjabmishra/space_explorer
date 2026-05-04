
import yaml


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    planets = config["planets"]
while True:
    print("What would you like to do?")

    print("[1]  Explore a planet")
    print("[2]  Get NASA Astronomy Picture of the Day")
    print("[3]  List all planets")
    print("[q]  Quit")
    user_input = input("Enter your choice: ")
    if user_input == "1":
        print("Exploring a planet...")
    elif user_input == "2":
        print("Getting NASA Astronomy Picture of the Day...")
    elif user_input == "3":
        print("Listing all planets...")
    elif user_input == "q":
        print("Quitting...")
        exit(0)
    else:
        print("Invalid choice. Please try again.")
print("Goodbye!")