import requests
from src.Controller import SmartHomeSystem
from src.MenuElements.Heater import heater_menu
from src.MenuElements.LightSwitch import light_switch_menu
from src.MenuElements.SmartTv import smart_tv_menu
from src.MenuElements.Logs import logs_menu
from src.MenuElements.Speaker import speaker_menu_component
from src.MenuElements.SmartBlinds import smart_blinds_menu
from src.MenuElements.LoginMenu import LoginMenu
from src.MenuElements.SettingsAndPreferences import settings
from src.MenuElements.SmartOven import smart_oven_menu
from src.MenuElements.CoffeeMaker import smart_coffee_menu
from src.MenuElements.CleaningRobot import cleaning_robot_menu
from src.MenuElements.Comments import comments_menu
from src.MenuElements.Import import import_menu
from src.MenuElements.SmokeDetector import smoke_detector_menu

if __name__ == "__main__":

    controller = None
    while True:
        try:

            # login
            user_role = None
            while True:
                login_menu = LoginMenu()
                user_role = login_menu[0]
                login = login_menu[1]
                if user_role:
                    break

            print("***Logged in***\n")

            # functionality
            if not controller:
                controller = SmartHomeSystem(role=user_role, login=login)

            controller.change_active_role(user_role)

            menu = {
                0: "\nSmart home controller menu:",
                "q": "1.\tEnter \"q\" to quit",
                "r": "2.\tEnter \"r\" to go to rooms list",
                "lg": "3.\tEnter \"lg\" to see controller logs",
                "c": "4.\tEnter \"c\" to go to comments",
                "s": "5.\tEnter \"s\" to go to settings"
            }
            if user_role == "root":
                menu = {
                    0: "\nSmart home controller menu:",
                    "q": "1.\tEnter \"q\" to quit",
                    "r": "2.\tEnter \"r\" to go to rooms list",
                    "lg": "3.\tEnter \"lg\" to see controller logs",
                    "c": "4.\tEnter \"c\" to go to comments",
                    "s": "5.\tEnter \"s\" to go to settings",
                    "i": "6.\tEnter \"i\" to go to import menu"
                }
            while controller.connected():

                # main menu
                for option in menu.values():
                    print(option)
                selected = input("#\t")

                # menu options steps

                # quit
                if selected == "q":
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
                                    elif device_type == "smart_oven":
                                        smart_oven_menu(selected_room, selected_room_menu_option, controller)
                                    elif device_type == "smart_coffee_maker":
                                        smart_coffee_menu(selected_room, selected_room_menu_option, controller)
                                    elif device_type == "cleaning_robot":
                                        cleaning_robot_menu(selected_room, selected_room_menu_option, controller)
                                    elif device_type == "smoke_detector":
                                        smoke_detector_menu(selected_room, selected_room_menu_option, controller)

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
                                            "smart_blinds": "5.\tSmart Blinds",
                                            "smart_oven": "6.\tSmart Oven",
                                            "smart_coffee_maker": "7.\tSmart Coffee maker",
                                            "cleaning_robot": "8.\tCleaning robot",
                                            "smoke_detector": "9.\tSmoke detector"
                                        }
                                        for device in devices.values():
                                            print(device)
                                        selected_device = input(f"{selected_room}#\t")
                                        if selected_device == "c":
                                            break
                                        elif selected_device in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
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
                                                elif selected_device == "6":
                                                    is_added = controller.add_device(device_name, selected_room, "smart_oven")
                                                elif selected_device == "7":
                                                    is_added = controller.add_device(device_name, selected_room, "smart_coffee_maker")
                                                elif selected_device == "8":
                                                    is_added = controller.add_device(device_name, selected_room, "cleaning_robot")
                                                elif selected_device == "9":
                                                    is_added = controller.add_device(device_name, selected_room, "smoke_detector")
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

                # comments
                elif selected == "c":
                    comments_menu(controller)

                # import menu
                elif selected == "i" and user_role == "root":
                    import_menu(controller)

                else:
                    print("Invalid option")
        except Exception:
            pass
        except KeyboardInterrupt:
            break
        finally:
            print("\nGoodbye...\n")

        requests.post("http://localhost:5000/backup", json={"devices": controller.get_devices()})