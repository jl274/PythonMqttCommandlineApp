from src.Controller import SmartHomeSystem


def smart_tv_menu(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    while True:
        [is_on, channel, volume, is_recording] = [
            last_data["data"]["is_on"], last_data["data"]["channel"],
            last_data["data"]["volume"], last_data["data"]["is_recording"]
        ]
        is_tv_on = "off"
        is_tv_recording = "off"
        if is_on:
            is_tv_on = "on"
        if is_recording:
            is_tv_recording = "on"
        print("\nTv is {}".format(is_tv_on))
        tv_menu = {
            "actions": "Available actions:\t",
            "s": "1.\tEnter \"s\" to switch tv power",
            "r": "2.\tEnter \"r\" to return"
        }
        if is_on:
            print("Channel: {}, Volume: {}/100, Recording is {}".format(channel, volume, is_tv_recording))
            tv_menu = {
                "actions": "Available actions:\t",
                "s": "1.\tEnter \"s\" to switch tv power",
                "v": "2.\tEnter \"v\" to control volume",
                "c": "3.\tEnter \"c\" to change channel",
                "rec": "4.\tEnter \"rec\" to switch recording",
                "r": "2.\tEnter \"r\" to return"
            }
        for tv_menu_option in tv_menu.values():
            print(tv_menu_option)
        selected_tv_menu = input(f'{room_t}/{device_t}#\t')

        # menu actions
        if selected_tv_menu == "r":

            break

        elif selected_tv_menu == "s":

            controller_t.use_tv_remote(not is_on, channel, volume, is_recording, room_t, device_t)
            last_data["data"]["is_on"] = not last_data["data"]["is_on"]

        elif is_on and selected_tv_menu == "v":

            while True:
                new_volume = input("Set volume on (enter \"c\" to cancel):\t")
                if new_volume == "c":
                    break
                new_volume = int(new_volume)
                if new_volume in range(0, 101):
                    controller_t.use_tv_remote(not is_on, channel, new_volume, is_recording, room_t, device_t)
                    last_data["data"]["volume"] = new_volume
                    break
                print("Volume must be greater or equal to 0 and less or equal to 100")

        elif is_on and selected_tv_menu == "c":

            while True:
                new_channel = input("Enter channel number or \"c\" to cancel:\t")
                if new_channel == "c":
                    break
                new_channel = int(new_channel)
                if new_channel in range(0, 999):
                    controller_t.use_tv_remote(not is_on, new_channel, volume, is_recording, room_t, device_t)
                    last_data["data"]["channel"] = new_channel
                    break
                print("Channel not found")

        elif is_on and selected_tv_menu == "rec":

            controller_t.use_tv_remote(is_on, channel, volume, not is_recording, room_t, device_t)
            last_data["data"]["is_recording"] = not last_data["data"]["is_recording"]

        else:
            print("Invalid option")
