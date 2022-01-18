from src.Controller import SmartHomeSystem


def heater_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        print("\nTemperature: {} - {}".format(last_data["data"], last_data["date"]))
        sensor_menu = {
            "actions": "Available actions:\t",
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
            last_data["data"] = new_temperature
        else:
            print("Invalid option")