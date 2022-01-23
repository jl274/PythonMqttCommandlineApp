import hashlib
import requests
import getpass


def LoginMenu() -> list:
    """
    :return: "root" or "user
    """
    while True:
        login = input("Login:\t")
        # password = getpass.getpass(prompt='Password:\t', stream=None)
        password = input("Password:\t")     # temp for testing purposes
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        r = requests.get(f"http://localhost:5000/login/{login}", json={"password": hashed_password}).json()
        if r["logged"]:
            return [r["role"], login]
        print("Invalid login data")
