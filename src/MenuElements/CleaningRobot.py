from src.Controller import SmartHomeSystem


def cleaning_robot_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        cleaning, battery = last_data["data"]["cleaning"], last_data["data"]["battery"]

        if cleaning:
            print("\nCleaning robot is working - {}".format(cleaning, last_data["date"]))
            print("Battery level: {}%".format(battery))
            robot_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tPress \"s\" to stop cleaning",
                "r": "2.\tPress \"r\" to return"
            }
        else:
            print("\nCleaning robot is charging in station - {}".format(cleaning, last_data["date"]))
            print("Battery level: {}%".format(battery))
            robot_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tPress \"s\" to start cleaning",
                "r": "2.\tPress \"r\" to return"
            }

        for robot_menu_option in robot_menu.values():
            print(robot_menu_option)
        selected_robot_menu = input(f'{room_t}/{device_t}#\t')

        if selected_robot_menu == "r":
            break

        elif selected_robot_menu == "s":
            if not cleaning and battery != 100:
                print("Battery must be full charged in order to start cleaning")
                input("Press any key to continue...")
                continue
            last_data["data"]["cleaning"] = not last_data["data"]["cleaning"]
            if cleaning:
                task = "start"
            else:
                task = "stop"
            controller_t.cleaning_robot_controller(task, room_t, device_t)

        else:
            print("Invalid option")
