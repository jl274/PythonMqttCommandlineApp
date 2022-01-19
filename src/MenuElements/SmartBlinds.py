from src.Controller import SmartHomeSystem


def smart_blinds_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        open_status = last_data["data"]
        print("\nBlinds are: {} - {}".format(open_status, last_data["date"]))

        blinds_menu = {}
        if open_status == "Opening..." or open_status == "Closing...":
            blinds_menu = {
                "actions": "Available actions:\t",
                "r": "1.\tPress \"r\" to return"
            }
        else:
            blinds_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tPress \"s\" to change blinds mode",
                "r": "2.\tPress \"r\" to return"
            }

        for blinds_menu_option in blinds_menu.values():
            print(blinds_menu_option)

        selected_blinds_menu = input(f'{room_t}/{device_t}#\t')

        if selected_blinds_menu == "r":
            break

        elif selected_blinds_menu == "s" and open_status not in ["Opening...", "Closing..."]:
            if open_status == "Open":
                pass
                last_data["data"] = "Closing..."
            elif open_status == "Closed":
                pass
                last_data["data"] = "Opening..."

        else:
            print("Invalid option")