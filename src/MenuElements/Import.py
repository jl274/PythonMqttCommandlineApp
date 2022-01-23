from src.Controller import SmartHomeSystem
import requests


def import_menu(controller_t: SmartHomeSystem):

    if controller_t.role != "root":
        return 0

    backups = requests.get("http://localhost:5000/backup").json()

    while True:

        sensor_menu = {
            "actions": "\nAvailable actions (enter backup number to load it):\t",
            "ls": "1.\tEnter \"ls\" to list all devices",
            "r": "2.\tEnter \"r\" to return"
        }
        for logs_menu_option in sensor_menu.values():
            print(logs_menu_option)
        selected_logs_menu = input(f'logs#\t')

        if selected_logs_menu == "r":
            break

        elif selected_logs_menu == "ls":
            for index in range(len(backups)):
                devices = 0
                devices += int(len(list(backups[index]["devices"].values())))
                print(f"---{index+1}---")
                print("Date: {}".format(backups[index]["date"]))
                print("Rooms: {}, devices number: {}".format(backups[index]["rooms"], devices))
            input("Press any key to continue...")

        elif len(selected_logs_menu) in range(1, 3):
            try:
                if int(selected_logs_menu) in range(1, len(backups)+1):

                    selected_backup = backups[int(selected_logs_menu)-1]
                    for room in selected_backup["rooms"]:
                        controller_t.add_room(room)
                        for device in selected_backup["devices"][room]:
                            device_name = device
                            device_type = selected_backup["devices"][room][device]
                            controller_t.add_device(device_name, room, device_type)
                    print("Import completed")
                    input("Press any key to continue...")

                else:
                    print("Invalid backup number")
                    continue
            finally:
                continue

        else:
            print("Invalid option")