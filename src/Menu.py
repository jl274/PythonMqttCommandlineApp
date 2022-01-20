from src.Controller import SmartHomeSystem
from src.MenuElements.Heater import heater_menu
from src.MenuElements.LightSwitch import light_switch_menu
from src.MenuElements.SmartTv import smart_tv_menu
from src.MenuElements.Logs import logs_menu
from src.MenuElements.Speaker import speaker_menu_component
from src.MenuElements.SmartBlinds import smart_blinds_menu
from src.MenuElements.LoginMenu import LoginMenu
from src.MenuElements.SettingsAndPreferences import settings

if __name__ == "__main__":

    controller = None
    while True:

        # login
        user_role = None
        while True:
            user_role = LoginMenu()
            if user_role:
                break

        print("***Logged in***\n")

        # functionality
        if not controller:
            controller = SmartHomeSystem(role=user_role)

        controller.change_active_role(user_role)

        menu = {
            0: "\nSmart home controller menu:",
            "q": "1.\tEnter \"q\" to quit",
            "r": "2.\tEnter \"r\" to go to rooms list",
            "lg": "3.\tEnter \"lg\" to see controller logs",
            "s": "4.\tEnter \"s\" to go to settings"
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
                            if controller.role == "root" and len(devices_in_room) != 0:
                                room_menu_options = {
                                    "r": "1.\tEnter \"r\" to return",
                                    "a": "2.\tEnter \"a\" to add new device",
                                    "m": "3.\tEnter \"m\" to move device to other room",
                                    "d": "4.\tEnter \"d\" to select and delete device"
                                }

                            for room_menu_option in room_menu_options.values():
                                print(room_menu_option)
                            selected_room_menu_option = input(f'{selected_room}#\t')

                            # entering proper menu
                            if selected_room_menu_option in devices_in_room:

                                device_type = controller.get_device_type(selected_room, selected_room_menu_option)
                                if device_type == "heater":
                                    heater_menu(selected_room, selected_room_menu_option, controller)
                                elif device_type == "light_switch":
                                    light_switch_menu(selected_room, selected_room_menu_option, controller)
                                elif device_type == "smart_tv":
                                    smart_tv_menu(selected_room, selected_room_menu_option, controller)
                                elif device_type == "speaker":
                                    speaker_menu_component(selected_room, selected_room_menu_option, controller)
                                elif device_type == "smart_blinds":
                                    smart_blinds_menu(selected_room, selected_room_menu_option, controller)

                            # break
                            if selected_room_menu_option == "r":
                                break

                            # move
                            elif selected_room_menu_option == "m" \
                                    and controller.role == "root" \
                                    and len(devices_in_room) != 0:
                                print()
                                device_name = input(f"Device name:\t")
                                new_room = input(f"New room name:\t")
                                moved = controller.move_device(selected_room, device_name, new_room)
                                if moved:
                                    print(f"Moved successfully {device_name} to {new_room}")
                                else:
                                    print("Problem occurred. Device wasn't moved")

                            # delete
                            elif selected_room_menu_option == "d" \
                                    and controller.role == "root" \
                                    and len(devices_in_room) != 0:
                                print()
                                print("Enter device name:")
                                device_to_delete = input(f"{selected_room}#\t")
                                deleted = controller.delete_device(selected_room, device_to_delete)
                                if deleted:
                                    print(f"Delete {device_to_delete}")
                                else:
                                    print("Problem occurred. Device wasn't deleted")

                            # add
                            elif selected_room_menu_option == "a":

                                # add device menu
                                while True:
                                    print("\nAvailable devices (enter option number):")
                                    devices = {
                                        "cancel": "Enter \"c\" to Cancel",
                                        "heater": "1.\tHeater",
                                        "light_switch": "2.\tLight switch",
                                        "smart_tv": "3.\tSmart TV",
                                        "speaker": "4.\tSpeaker",
                                        "smart_blinds": "5 \tSmart Blinds"
                                    }
                                    for device in devices.values():
                                        print(device)
                                    selected_device = input(f"{selected_room}#\t")
                                    if selected_device == "c":
                                        break
                                    elif selected_device in ["1", "2", "3", "4", "5"]:
                                        is_added = False
                                        while not is_added:
                                            device_name = input(f'Name your device:\t')
                                            if selected_device == "1":
                                                is_added = controller.add_device(device_name, selected_room, 'heater')
                                            elif selected_device == "2":
                                                is_added = controller.add_device(device_name, selected_room, 'light_switch')
                                            elif selected_device == "3":
                                                is_added = controller.add_device(device_name, selected_room, "smart_tv")
                                            elif selected_device == "4":
                                                is_added = controller.add_device(device_name, selected_room, "speaker")
                                            elif selected_device == "5":
                                                is_added = controller.add_device(device_name, selected_room, "smart_blinds")
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

            # logs menu
            elif selected == "lg":
                logs_menu(controller)

            # settings
            elif selected == "s":
                settings(controller)

            else:
                print("Invalid option")
