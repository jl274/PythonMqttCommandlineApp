from src.Controller import SmartHomeSystem


def temp_sensor_menu(room_t, device_t, controller_t: SmartHomeSystem):
    while True:
        sensor_menu = {
            "actions": "\nAvailable actions:\t",
            "s": "1.\tPress \"s\" to set temperature",
            "r": "2.\tPress \"r\" to return"
        }
        for sensor_menu_option in sensor_menu.values():
            print(sensor_menu_option)
        selected_sensor_menu = input(f'{room_t}/{device_t}#\t')
        if selected_sensor_menu == "r":
            break
        elif selected_sensor_menu == "s":
            new_temperature = input("Set temperature:\t")
            controller_t.set_temperature(int(new_temperature), room_t, device_t)

if __name__ == "__main__":
    controller = SmartHomeSystem()
    menu = {
        0: "\nSmart home controller menu:",
        "q": "1.\tEnter \"q\" to quit",
        "r": "2.\tEnter \"r\" to go to rooms list"
        # ,"a": "2.\tEnter \"a\" to add new device"
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
                print("\nAvailable rooms: ", end="\t")
                if len(rooms) == 0:
                    print("No rooms added yet", end=" ")
                else:
                    for room in rooms:
                        print(room, end=" ")
                print(
                    "\nEnter room name to continue" +
                    "\nEnter \"r\" to return" +
                    "\nEnter \"a\" to add new room"
                )
                selected_room = input("#\t")
                if selected_room in rooms:

                    # inside rooms menu
                    while True:

                        print(f"\nAvailable devices in {selected_room}:\t")
                        devices_in_room = controller.get_room_devices(selected_room)
                        for room_device in devices_in_room:
                            print("\t" + room_device)

                        room_menu_options = {
                            "r": "1.\tEnter \"r\" to return",
                            "a": "2.\tEnter \"a\" to add new device"
                        }
                        for room_menu_option in room_menu_options.values():
                            print(room_menu_option)
                        selected_room_menu_option = input(f'{selected_room}#\t')

                        # setting new temperature
                        if selected_room_menu_option in devices_in_room:
                            temp_sensor_menu(selected_room, selected_room_menu_option, controller)
                        if selected_room_menu_option == "r":
                            break
                        elif selected_room_menu_option == "a":

                            # add device menu
                            while True:
                                print("\nAvailable devices (enter option number):")
                                devices = {
                                    "cancel": "Enter \"c\" to Cancel",
                                    "temp_sensor": "1.\tTemperature sensor"
                                }
                                for device in devices.values():
                                    print(device)
                                selected_device = input("#\t")
                                if selected_device == "c":
                                    break
                                elif selected_device == "1":
                                    is_added = False
                                    while not is_added:
                                        device_name = input(f'Name your device:\t')
                                        is_added = controller.add_device(device_name, selected_room, 'temp_sensor')
                                        if not is_added:
                                            print("Name already taken")
                                    break
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

        else:
            print("Invalid option")
