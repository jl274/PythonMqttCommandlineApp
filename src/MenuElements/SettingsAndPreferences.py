from src.Controller import SmartHomeSystem
import requests
import hashlib


def settings(controller_t: SmartHomeSystem):
    while True:
        if controller_t.role == "root":
            settings_menu = {
                "actions": "Available actions:\t",
                "a": "1.\tEnter \"a\" to add user",
                "ls": "2.\tEnter \"ls\" to list users",
                "d": "1.\tEnter \"d\" to select and delete user",
                "r": "1.\tEnter \"r\" to return"
            }
        else:
            settings_menu = {
                "actions": "Available actions:\t",
                "r": "1.\tEnter \"r\" to return"
            }
        for settings_menu_option in settings_menu.values():
            print(settings_menu_option)
        selected_settings_menu = input(f'settings#\t')

        if selected_settings_menu == "r":
            break

        elif selected_settings_menu == "a" and controller_t.role == "root":
            print()
            login = input("Create login:\t")
            password = input("Create password:\t")
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            print("Select role for new user (enter option number):\n1.\tAdmin\n2.\tRegular user")
            role = input('settings#\t')
            if role == "1":
                role = "root"
            elif role == "2":
                role = "user"
            r = requests.post(
                "http://localhost:5000/login",
                json={"login": login, "password": hashed_password, "role": role}
            )
            if r.status_code == 200:
                print("New user successfully created\n")
            else:
                print("Error occurred. Try again...")

        elif selected_settings_menu == "s":
            pass

        else:
            print("Invalid option")
