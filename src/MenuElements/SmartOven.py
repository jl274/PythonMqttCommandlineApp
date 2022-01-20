from src.Controller import SmartHomeSystem


def smart_oven_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        is_on, temp, time = last_data["data"]["is_on"], last_data["data"]["temp"], last_data["data"]["time"]

        if is_on:
            print("\nOven is is on - {}".format(last_data["date"]))
            print(
                "Temperature: {}°C, Timer: {} seconds left"
                .format(last_data["data"]["temp"], last_data["data"]["time"])
            )
            if time > 0 or temp > 0:
                oven_menu = {
                    "actions": "Available actions:\t",
                    "s": "1.\tPress \"s\" to cancel cooking and turn it off",
                    "r": "2.\tPress \"r\" to return"
                }
            else:
                oven_menu = {
                    "actions": "Available actions:\t",
                    "s": "1.\tPress \"s\" to turn it off",
                    "h": "2.\tPress \"h\" to set temperature and cooking time",
                    "r": "3.\tPress \"r\" to return"
                }
        else:
            print("\nOven is off - {}".format(last_data["date"]))
            oven_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tPress \"s\" to turn it on",
                "r": "2.\tPress \"r\" to return"
            }

        for oven_menu_option in oven_menu.values():
            print(oven_menu_option)

        selected_oven_menu = input(f'{room_t}/{device_t}#\t')

        if selected_oven_menu == "r":
            break

        elif selected_oven_menu == "s":
            controller_t.control_smart_oven(not is_on, temp, time, room_t, device_t)
            last_data["data"]["is_on"] = not last_data["data"]["is_on"]

        elif selected_oven_menu == "h" and is_on:
            while True:
                new_temp = int(input("Enter cooking temperature in °C\t"))
                if new_temp not in range(60, 221):
                    print("Temperature should be between 60°C and 220°C")
                    continue
                new_time = int(input("Enter cooking time (in seconds)\t"))
                if new_time not in range(10, 18000):
                    print("Time should be between 10 and 18 000 seconds")
                    continue
                controller_t.control_smart_oven(is_on, new_temp, new_time, room_t, device_t)
                last_data["data"]["temp"] = int(new_temp)
                last_data["data"]["time"] = int(new_time)
                break

        else:
            print("Invalid option")
