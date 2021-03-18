import random
import sys
import sqlite3


# ------------------------------------------------------------------------------------------------------

class Bank_DB:

    def __init__(self, name):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()

    def create_tb(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card
        (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)''')
        self.con.commit()

    def add_record(self, num, pin, amount):
        self.cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", (num, pin, amount,))
        self.con.commit()

    def find_record(self, num):
        try:
            self.cur.execute("SELECT * FROM card WHERE number = (?)", (num,))
            # acc_num = self.cur.fetchone()[1]
            # acc_pin = self.cur.fetchone()[2]
            # acc_bal = self.cur.fetchone()[3]
            return self.cur.fetchone()
        except sqlite3.Error:
            return False

    def update_record(self, name, amt):
        self.cur.execute("UPDATE card SET balance = balance + (?) WHERE number = (?)", (amt, name,))
        self.con.commit()

    def delete_record(self, name):
        self.cur.execute("DELETE FROM card WHERE number = (?)", (name,))
        self.con.commit()

    def transfer(self, uname, name, amt):
        self.cur.execute("SELECT balance FROM card WHERE number = (?)", (uname,))
        ub = self.cur.fetchone()[0]
        if ub >= amt:
            self.cur.execute("UPDATE card SET balance = balance + (?) WHERE number = (?)", (amt, name,))
            self.cur.execute("UPDATE card SET balance = balance - (?) WHERE number = (?)", (amt, uname,))
            self.con.commit()
            return True
        else:
            return False

    def exit(self):
        self.con.close()


# --------------------------------------------------------------------------------------------------------
class Bank:

    def __init__(self):
        self.customer_balance = '0'
        self.menu_option = None
        self.login_option = None
        self.check_card = None
        self.receiver_card = None
        self.db = Bank_DB('card.s3db')
        self.db.create_tb()
    @staticmethod
    def luhn(lst):
        new_list = [x * 2 if i % 2 else x for i, x in enumerate(lst, 1)]
        subtract_list = [x - 9 if x > 9 else x for x in new_list]
        return subtract_list

    def create_cnumber(self):
        bank_id = 400000
        acc_id = random.randrange(10 ** 8, 10 ** 9)
        credit_card_number = f'{bank_id}{acc_id}'
        split_list = list(map(int, credit_card_number))
        subtract_list = self.luhn(split_list)
        # What number is the checksum?
        remainder = 10 - (sum(subtract_list) % 10)
        if remainder == 10:
            remainder = 0
        # Add final number to credit card number
        final_number = f'{credit_card_number}{remainder}'
        return final_number

    def luhn_checksum(self, crd_num):
        int_list = list(map(int, crd_num))
        last_digit = int_list.pop()
        minus_nine = self.luhn(int_list)
        sum_plus_last = sum(minus_nine) + last_digit
        if sum_plus_last % 10 == 0:
            return True
        else:
            return False

    @staticmethod
    def create_pnumber():
        return random.randrange(10 ** 3, 10 ** 4)

    def create_acc(self):
        acc_num = self.create_cnumber()
        acc_pin = str(self.create_pnumber())

        self.db.add_record(acc_num, acc_pin, 0)
        print(f'\nYour card has been created\nYour card number:\n{acc_num}'
              f'\nYour card PIN:\n{acc_pin}\n')
        self.check_card = acc_num

    def login(self):
        self.check_card = input('\nEnter your card number: ')
        check_pin = input('Enter your PIN: ')
        res = self.db.find_record(self.check_card)
        if len(self.check_card) != 16 or res is None:
            print('\nWrong card number or PIN!\n')
        elif self.check_card == res[1] and \
                check_pin == res[2]:
            if self.luhn_checksum(self.check_card):
                print('\nYou have successfully logged in!\n')
                return True
            else:
                print('\nWrong card number or PIN!\n')
                return False
        else:
            print('\nWrong card number or PIN!\n')
            return False

    def do_transfer(self):
        print('\nTransfer')
        self.receiver_card = input('\nEnter card number:')
        if not self.luhn_checksum(self.receiver_card):
            print('Probably you made a mistake in the card number. Please try again!')
        elif not self.db.find_record(self.receiver_card):
            print("Such a card does not exist.")
        elif self.receiver_card == self.check_card:
            print("\nYou can't transfer money to the same account!\n")
        else:
            amt = int(input('Enter how much money you want to transfer: '))
            trans = self.db.transfer(self.check_card, self.receiver_card, amt)
            if trans:
                print('\nSuccess!\n')
            else:
                print('\nNot enough money!\n')

    def add_income(self):
        amt = int(input('Enter income: '))
        self.db.update_record(self.check_card, amt)
        print('\nIncome was added!\n')

    def close_account(self):
        self.db.delete_record(self.check_card)
        print('The account has been closed!\n')

    def check_balance(self):
        res = self.db.find_record(self.check_card)
        print(f"\nBalance: {res[3]}\n")

    def logout(self):
        print("\nYou have successfully logged out!\n")

    def exit_message(self):
        self.db.exit()
        sys.exit('\nBye!\n')


# -----------------------------------------------------------------------------------------------------------

class Menu:

    def __init__(self):
        self.menu_options = "1. Create an account\n2. Log into account\n0. Exit\n"
        self.login_options = "1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"
        self.bank = Bank()
        # self.login_choice = login_choice

    def menu_choice(self):
        user_choice = input(self.menu_options)
        if user_choice == "1":
            self.bank.create_acc()
            self.menu_choice()
        elif user_choice == "2":
            if self.bank.login():
                login_choice = input(self.login_options)
                self.login_option(login_choice)
            else:
                self.menu_choice()
        else:
            self.bank.exit_message()

    def login_option(self, inp):
        if inp == '1':
            self.bank.check_balance()
            self.ask_choice()
        elif inp == '2':
            self.bank.add_income()
            self.ask_choice()
        elif inp == '3':
            self.bank.do_transfer()
            self.ask_choice()
        elif inp == '4':
            self.bank.close_account()
            self.menu_choice()
        elif inp == '5':
            self.bank.logout()
            self.menu_choice()
        else:
            self.bank.exit_message()

    def ask_choice(self):
        self.login_option(input(self.login_options))


menu = Menu()

menu.menu_choice()
