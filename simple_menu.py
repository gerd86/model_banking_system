import sys


class Menu:

    def __init__(self):
        self.menu_options = "1. Create an account\n2. Log into account\n0. Exit\n"
        self.login_options = "1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"

    def menu_choice(self):
        user_choice = input(self.menu_options)
        if user_choice == "1":
            print("You selected one")
            sys.exit('Bye')
        elif user_choice == "2":
            login_choice = input(self.login_options)
            self.login_option(login_choice)
        else:
            sys.exit('Bye')

    def login_option(self, inp):
        if inp == '1':
            print(1)
            self.menu_choice()
        elif inp == '2':
            print(2)
            self.menu_choice()
        elif inp == '3':
            print(3)
            self.menu_choice()
        elif inp == '4':
            print(4)
            self.menu_choice()
        elif inp == '5':
            print(5)
            self.menu_choice()
        else:
            sys.exit('Bye')


menu = Menu()

menu.menu_choice()
