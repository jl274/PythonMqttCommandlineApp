from src.Controller import SmartHomeSystem
from datetime import datetime


def logs_menu(controller_t: SmartHomeSystem):

    while True:

        ls = controller_t.list_devices()
        devices_names = []
        for sub_ls in ls:
            for room_and_device in sub_ls.values():
                room_name = list(sub_ls.keys())[0]
                for device in room_and_device:
                    devices_names.append(f'{room_name}/{device}')

        sensor_menu = {
            "actions": "\nAvailable actions (enter device name or option letter):\t",
            "all": "1.\tEnter \"all\" to list last 50 logs from all devices",
            "ls": "2.\tEnter \"ls\" to list all devices",
            "r": "3.\tEnter \"r\" to return"
        }
        for logs_menu_option in sensor_menu.values():
            print(logs_menu_option)
        selected_logs_menu = input(f'logs#\t')

        if selected_logs_menu == "r":
            break

        elif selected_logs_menu in devices_names:
            device_logs = controller_t.get_all_device_logs(selected_logs_menu)
            if len(device_logs) > 0:
                date_now = datetime.now()
                print(f"***Logs for {selected_logs_menu} - {date_now}***")
                for log in device_logs:
                    print("Date: {}, Data: {}".format(log["date"], log["data"]))
                print("*** --- ***")
            else:
                print("No logs registered yet")
            input("Press any key to continue...")

        elif selected_logs_menu == "ls":
            if len(ls) > 0:
                print()
                for index in range(len(ls)):
                    room_name = list(ls[index].keys())[0]
                    print(f'{room_name}:')
                    try:
                        for device in ls[index][room_name]:
                            print(f'{room_name}/{device}')
                    except:
                        pass
                    print()
            else:
                print("No devices added yet")
            input("Press any key to continue...")

        elif selected_logs_menu == "all":
            print()
            lg = controller_t.get_logs(50)
            if len(lg) > 0:
                date_now = datetime.now()
                print(f"***Logs for {date_now}***")
                for log in lg:
                    print("Device: {}, Date: {}, Data: {}".format(log["device"], log["date"], log["data"]))
                print("*** --- ***")
            else:
                print("No logs registered yet")
            input("Press any key to continue...")

        else:
            print("Invalid option")