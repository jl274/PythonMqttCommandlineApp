from src.Controller import SmartHomeSystem


def light_switch_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        is_on = "off"
        if last_data["data"] is True:
            is_on = "on"
        print("\nLight is {} - {}".format(is_on, last_data["date"]))
        sensor_menu = {
            "actions": "Available actions:\t",
            "s": "1.\tPress \"s\" to switch light",
            "r": "2.\tPress \"r\" to return"
        }
        for sensor_menu_option in sensor_menu.values():
            print(sensor_menu_option)
        selected_sensor_menu = input(f'{room_t}/{device_t}#\t')
        if selected_sensor_menu == "r":
            break
        elif selected_sensor_menu == "s":
            controller_t.switch_light(not last_data["data"], room_t, device_t)
            last_data["data"] = not last_data["data"]
        else:
            print("Invalid option")
