from src.Controller import SmartHomeSystem

if __name__ == "__main__":
    controller = SmartHomeSystem()
    menu = {0: "Smart home controller menu:", "q": "1.\t press q to quit"}
    while controller.connected():
        for option in menu.values():
            print(option)
        selected = input("#\t")
        if selected == "q":
            print("Goodbye")
            break
        print("Invalid option")