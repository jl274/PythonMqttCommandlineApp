from src.Controller import SmartHomeSystem


def speaker_menu_component(room_t, device_t, controller_t: SmartHomeSystem):
    last_data = controller_t.find_last_report(f'{room_t}/{device_t}')
    songs_from_db = {
        "Short song": 25,
        "Medium song": 115,
        "Long song": 220
    }
    while True:
        [is_on, is_playing, song, time_left] = [
            last_data["data"]["is_on"], last_data["data"]["is_playing"],
            last_data["data"]["song"], last_data["data"]["time_left"]
        ]
        is_speaker_on = "off"

        speaker_menu = {
            "actions": "Available actions:\t",
            "s": "1.\tEnter \"s\" to switch power",
            "r": "2.\tEnter \"r\" to return"
        }
        print("\nSpeaker is {}".format(is_speaker_on))

        if is_on:
            if is_playing:
                print("Status: playing now {}. Time left: {}".format(song, time_left))
                speaker_menu = {
                    "actions": "Available actions:\t",
                    "s": "1.\tEnter \"s\" to switch power",
                    "f": "2.\tEnter \"f\" to stop playing permanently",
                    "ls": "3.\tEnter \"ls\" to list all songs",
                    "r": "4.\tEnter \"r\" to return"
                }
            else:
                print("Status: not playing anything")
                speaker_menu = {
                    "actions": "Available actions (enter song title to play it):\t",
                    "s": "1.\tEnter \"s\" to switch power",
                    "ls": "2.\tEnter \"ls\" to list all songs",
                    "r": "3.\tEnter \"r\" to return"
                }

        for speaker_menu_option in speaker_menu.values():
            print(speaker_menu_option)
        selected_speaker_menu = input(f'{room_t}/{device_t}#\t')

        if selected_speaker_menu == "r":
            break

        elif selected_speaker_menu == "s":

            controller_t.use_speaker_remote(not is_on, song, is_playing, time_left, room_t, device_t)
            last_data["data"]["is_on"] = not last_data["data"]["is_on"]

        elif selected_speaker_menu == "ls" and is_on:
            for song in songs_from_db:
                print(f'\t* {song}')
            input("Press any key to continue...")

        elif selected_speaker_menu == "f" and is_on and is_playing:
            controller_t.use_speaker_remote(is_on, song, not is_playing, time_left, room_t, device_t)
            last_data["data"]["is_playing"] = not last_data["data"]["is_playing"]

        elif selected_speaker_menu in songs_from_db.keys() and is_on and not is_playing:
            controller_t.use_speaker_remote(
                is_on, selected_speaker_menu, True, songs_from_db[selected_speaker_menu], room_t, device_t
            )
            last_data["data"]["is_playing"] = True
            last_data["data"]["song"] = selected_speaker_menu
            last_data["data"]["time_left"] = songs_from_db[selected_speaker_menu]

        else:
            print("Invalid option")