from src.Controller import SmartHomeSystem


def smart_coffee_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        is_on, status, bean_level, water_level = last_data["data"]["is_on"], last_data["data"]["status"], \
                                                 last_data["data"]["bean"], last_data["data"]["water"]

        if is_on:
            print("\nSmart coffee maker is on - {}".format(last_data["date"]))
            print("Water level {}%, Coffee beans level {}%".format(water_level*100, bean_level*100))
            if status != "":
                print("Coffee status: {}".format(status))
            coffee_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tPress \"s\" to switch it off",
                "m": "2.\tEnter \"m\" to make coffee",
                "r": "3.\tPress \"r\" to return"
            }
        else:
            print("\nSmart coffee maker is off - {}".format(last_data["date"]))
            coffee_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tPress \"s\" to switch it on",
                "r": "2.\tPress \"r\" to return"
            }

        for coffee_menu_option in coffee_menu.values():
            print(coffee_menu_option)

        selected_coffee_maker_menu = input(f'{room_t}/{device_t}#\t')

        if selected_coffee_maker_menu == "r":
            break

        elif selected_coffee_maker_menu == "s":
            controller_t.coffee_maker_controller(not is_on, False, room_t, device_t)
            last_data["data"]["is_on"] = not last_data["data"]["is_on"]

        elif selected_coffee_maker_menu == "m" and is_on:
            controller_t.coffee_maker_controller(is_on, "coffee", room_t, device_t)
            last_data["data"]["status"] = "Making coffee..."

        else:
            print("Invalid option")
