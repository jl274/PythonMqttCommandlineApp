from src.Controller import SmartHomeSystem


def smoke_detector_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        smoke_level, alarm = last_data["data"]["smoke"], last_data["data"]["alarm"]
        print("\nSmoke level: {} - {}".format(smoke_level, last_data["date"]))
        if alarm:
            print("ALARM! It is hazardous level. Open window now!")
        else:
            print("Normal level is between 0 and 85")
        smoke_menu = {
            "actions": "Available actions:\t",
            "s": "1.\tPress \"s\" to simulate opening window",
            "r": "2.\tPress \"r\" to return"
        }
        for smoke_menu_option in smoke_menu.values():
            print(smoke_menu_option)
        selected_smoke_menu = input(f'{room_t}/{device_t}#\t')
        if selected_smoke_menu == "r":
            break
        elif selected_smoke_menu == "s":
            controller_t.simulate_opening_window(room_t, device_t)
            last_data["data"]["smoke"] = 50
        else:
            print("Invalid option")
