from src.Controller import SmartHomeSystem
from src.MenuElements.TempSensor import temp_sensor_menu
from src.MenuElements.LightSwitch import light_switch_menu
from src.MenuElements.SmartTv import smart_tv_menu
from datetime import datetime

if __name__ == "__main__":
    controller = SmartHomeSystem()
    menu = {
        0: "\nSmart home controller menu:",
        "q": "1.\tEnter \"q\" to quit",
        "r": "2.\tEnter \"r\" to go to rooms list",
        "ls": "3.\tEnter \"ls\" to list all devices",
        "lg": "4.\tEnter \"lg\" to see controller logs"
    }
    while controller.connected():

        # main menu
        for option in menu.values():
            print(option)
        selected = input("#\t")

        # menu options steps

        # quit
        if selected == "q":
            print("Goodbye")
            break
        # rooms menu
        elif selected == "r":

            while True:
                rooms = controller.get_rooms()
                print("\nAvailable rooms (enter room name to continue): ", end="")
                if len(rooms) == 0:
                    print("\n\t*No rooms added yet", end="")
                else:
                    for room in rooms:
                        print("\n\t* " + room, end="")
                print(
                    "\nEnter \"r\" to return" +
                    "\nEnter \"a\" to add new room"
                )
                selected_room = input("#\t")
                if selected_room in rooms:

                    # inside rooms menu
                    while True:

                        print(f"\nAvailable devices in {selected_room}:\t", end="")
                        devices_in_room = controller.get_room_devices(selected_room)
                        for room_device in devices_in_room:
                            print("\n\t* " + room_device, end="")
                        print()

                        room_menu_options = {
                            "r": "1.\tEnter \"r\" to return",
                            "a": "2.\tEnter \"a\" to add new device"
                        }
                        for room_menu_option in room_menu_options.values():
                            print(room_menu_option)
                        selected_room_menu_option = input(f'{selected_room}#\t')

                        # entering proper menu
                        if selected_room_menu_option in devices_in_room:

                            device_type = controller.get_device_type(selected_room, selected_room_menu_option)
                            if device_type == "temp_sensor":
                                temp_sensor_menu(selected_room, selected_room_menu_option, controller)
                            elif device_type == "light_switch":
                                light_switch_menu(selected_room, selected_room_menu_option, controller)
                            elif device_type == "smart_tv":
                                smart_tv_menu(selected_room, selected_room_menu_option, controller)

                        if selected_room_menu_option == "r":
                            break
                        elif selected_room_menu_option == "a":

                            # add device menu
                            while True:
                                print("\nAvailable devices (enter option number):")
                                devices = {
                                    "cancel": "Enter \"c\" to Cancel",
                                    "temp_sensor": "1.\tTemperature sensor",
                                    "light_switch": "2.\tLight switch",
                                    "smart_tv": "3.\tSmart TV"
                                }
                                for device in devices.values():
                                    print(device)
                                selected_device = input(f"{selected_room}#\t")
                                if selected_device == "c":
                                    break
                                elif selected_device in ["1", "2", "3"]:
                                    is_added = False
                                    while not is_added:
                                        device_name = input(f'Name your device:\t')
                                        if selected_device == "1":
                                            is_added = controller.add_device(device_name, selected_room, 'temp_sensor')
                                        elif selected_device == "2":
                                            is_added = controller.add_device(device_name, selected_room, 'light_switch')
                                        elif selected_device == "3":
                                            is_added = controller.add_device(device_name, selected_room, "smart_tv")
                                        if not is_added:
                                            print("Name already taken")
                                    break
                                else:
                                    print("Invalid device")

                        else:
                            print("Invalid option")

                elif selected_room == "r":
                    break

                elif selected_room == "a":
                    new_room = input("New room name =\t")
                    controller.add_room(new_room)

                else:
                    print("Invalid room")

        # list all devices
        elif selected == "ls":
            ls = controller.list_devices()
            if len(ls) > 0:
                print()
                for index in range(len(ls)):
                    room_name = list(ls[index].keys())[0]
                    print(f'{room_name}:')
                    for device in ls[index][room_name]:
                        print(f'{room_name}/{device}')
                    print()
            else:
                print("No devices added yet")
            input("Press any key to continue...")

        # show last 50 logs
        elif selected == "lg":
            print()
            lg = controller.get_logs(50)
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
