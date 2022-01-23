from src.Controller import SmartHomeSystem
import requests


def comments_menu(controller_t: SmartHomeSystem):

    comments = requests.get("http://localhost:5000/comments").json()
    is_root = controller_t.role == "root"

    while True:

        if is_root:
            sensor_menu = {
                "actions": "\nAvailable actions (enter device name or option letter):\t",
                "ls": "1.\tEnter \"ls\" to list last 5 comments",
                "a": "2.\tEnter \"a\" to add new comment",
                "e": "3.\tEnter \"e\" to select and edit post",
                "d": "4.\tEnter \"d\" to select and delete post",
                "r": "5.\tEnter \"r\" to return"
            }
        else:
            sensor_menu = {
                "actions": "\nAvailable actions (enter device name or option letter):\t",
                "ls": "1.\tEnter \"ls\" to list last 5 comments",
                "a": "2.\tEnter \"a\" to add new comment",
                "r": "3.\tEnter \"r\" to return"
            }
        for logs_menu_option in sensor_menu.values():
            print(logs_menu_option)
        selected_logs_menu = input(f'logs#\t')

        if selected_logs_menu == "r":
            break

        elif selected_logs_menu == "ls":
            print()
            if len(comments) >= 5:
                index_range = range(5)
            else:
                index_range = range(len(comments))
            for index in index_range:
                author_login = comments[index]["login"]["login"]
                text = comments[index]["text"]
                date = comments[index]["date"]
                print("---{}---".format(index+1))
                print("\"{}\"".format(text))
                print("~ {} on {}".format(author_login, date))
            print()
            input("Press any key to continue...")

        elif selected_logs_menu == "a":
            text = input("Enter your comment:\n")
            r = requests.post("http://localhost:5000/comments", json={"login": controller_t.login, "text": text})
            if r.status_code == 200:
                print("Added")
                comments = requests.get("http://localhost:5000/comments").json()
            else:
                print("Server error")
                input("Press any key to continue...")

        elif selected_logs_menu == "e" and is_root:
            comment_number = int(input("Enter comment number:\t"))
            new_text = input("New comment text:\t")
            r = requests.patch(
                "http://localhost:5000/comments", json={"id": comments[comment_number-1]["_id"], "text": new_text}
            )
            if r.status_code == 200:
                print("Edited successfully")
                comments[comment_number-1]["text"] = new_text
            else:
                print("Server error")
                input("Press any key to continue...")

        elif selected_logs_menu == "d" and is_root:
            comment_number = int(input("Enter comment number:\t"))
            r = requests.delete("http://localhost:5000/comments/{}".format(comments[comment_number-1]["_id"]))
            if r.status_code == 200:
                print("Deleted successfully")
                del comments[comment_number-1]
            else:
                print("Server error")
                input("Press any key to continue...")

        else:
            print("Invalid option")
