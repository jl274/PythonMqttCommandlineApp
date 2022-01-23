from src.Controller import SmartHomeSystem


def cleaning_robot_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        cleaning, battery = last_data["data"]["cleaning"], last_data["data"]["battery"]

        if cleaning:
            print("\nCleaning robot is working - {}".format(last_data["date"]))
            print("Battery level: {}%".format(battery))
            robot_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tEnter \"s\" to stop cleaning",
                "r": "2.\tEnter \"r\" to return"
            }
        else:
            print("\nCleaning robot is charging in station - {}".format(last_data["date"]))
            print("Battery level: {}%".format(battery))
            robot_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tEnter \"s\" to start cleaning",
                "d": "2.\tEnter \"d\" to start cleaning with delay",
                "r": "3.\tEnter \"r\" to return"
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
                task = "stop"
            else:
                task = "start"
            controller_t.cleaning_robot_controller(task, room_t, device_t)

        elif selected_robot_menu == "d" and not cleaning:
            try:
                delay_time = int(input("Delay time in seconds: "))
                if delay_time not in range(1, 21600):
                    print("Time must be between 1 and 21 600 seconds!")
                    input("Press any key to continue...")
                    continue
                controller_t.cleaning_robot_controller("delay", room_t, device_t, delay=delay_time)
                input(f"Cleaning will start in {delay_time} seconds\nPress any key to continue...")
            except:
                print("Invalid delay time")

        else:
            print("Invalid option")
