import re
# Below is a function which opens the 'login_credentials' txt file and pulls out the information to put into a dictionary
def read_login_file():
    # read txt file
    file = open(r"C:\Users\Becky\Documents\CoGrammar\myenv\Tasks\login_credentials.txt", "r")
    # create the dictionary
    temp_dictionary = {}
    # for each line in the txt file, split by spaces, storing as a list
    for lines in file:
        temp_file = lines.strip().split(", ")
        # put the contents of the list into a dictionary of format {username : [firstname, surname, pin, balance]}
        temp_dictionary[temp_file[2]] = [temp_file[0], temp_file[1], temp_file[3], float(temp_file[4])]
    return temp_dictionary

# The below function is run when the user would like to login
def login_check():
    while True:
        #ask user for username and pin
        username = input("Please enter your username (this is usually your email address): ")
        username = username.strip()
        pin = input("Please enter your 4-digit pin: ")
        # run read_login_file function to get login details
        temp_dictionary = read_login_file()
        # check if the given username is in the dictionary
        if username not in temp_dictionary.keys():
            print("You have entered an incorrect username. Please try again.")
        # check if the given pin is the pin for that username in the dictionary
        elif pin == temp_dictionary[username][2]:
            print("You have logged in successfully.")
            break
        elif pin != temp_dictionary[username][2]:
            print("You have entered an incorrect pin. Please try again.")
    return username, temp_dictionary

# the function below is run when the user would like to register
def register():
    # ask the user for their first name, create temp name with spaces and hyphens taken out
    # check whether the temp name only contains letters
    first_name = input("Please enter your first name: ").lower()
    while True:
        temp_first_name = first_name.replace(" ","")
        temp_first_name = temp_first_name.replace("-","")
        if temp_first_name.isalpha():
            break
        else:
            first_name = input("Your first name should only contain letters. Please re-enter your first name: ")
    # ask the user for their surname, create temp name with spaces and hyphens taken out
    # check whether the temp name only contains letters
    surname = input("Please enter your surname: ").lower()
    while True:
        temp_surname = surname.replace(" ","")
        temp_surname = temp_surname.replace("-","")
        if temp_surname.isalpha():
            break
        else:
            surname = input("Your surname should only contain letters. Please re-enter your surname: ")
    # ask the user for their username
    username = input("Please input your username (email address): ").lower()
    # get usernames from read_login_file function to check if the username already exists
    temp_dictionary = read_login_file()
     # create regular expression for validating an email
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    while True:
        if username in temp_dictionary.keys():
            username = input("This username already exists. Please input a different username: ").lower()
        # if username is not in the txt file, check if the username doesn't follow the regular expression for an email address
        elif not re.match(regex, username):
            username = input("Your username should be a valid email address. Please re-enter your username: ").lower()
        else:
            break
    # ask user for their pin
    pin_1 = input("Please enter your desired 4 digit pin: ")
    while True:
        # check whether the pin is 4 digits
        if len(pin_1) != 4:
            pin_1 = input("Your pin must contain 4 characters or numbers. Please re-enter your pin: ")
        else:
            pin_2 = input("Please enter your desired pin again: ")
            # check if the pins match each other
            if pin_1 == pin_2:
                break
            else:
                pin_2 = input("Your pins do not match. Please re-enter your pin: ")
    # ask the user to input how much they will be depositing in the bank account
    balance = input("Please enter the amount you will be depositing into your bank account (£): ")
    while True:
        # check whether the user has entered a value without a negative sign and is either a whole number or has 2 decimal places
        if "." not in balance and "-" not in balance or "." in balance and len(balance.rsplit(".")[-1]) == 2:
            # try converting the amount to a float, if this isn't possible, ask user to re-enter the amount
            try:
                balance = float(balance)
            except:
                balance = input("You have entered an invalid amount, please re-enter: (£) ")
            else:
                break
        else:
            balance = input("You have entered an invalid amount, please re-enter: (£) ")
    # add new info to the temp_dictionary
    temp_dictionary[username] = [first_name.capitalize(), surname.capitalize(), pin_1, balance]
    print(temp_dictionary)
    return username, temp_dictionary
       
def transfer_funds(username, temp_dictionary):  
    # ask user to enter the account they want to transfer money to and the amount they would like to transfer     
    transfer_account = input("Please enter the username of the account you would like to transfer to: ")
    while True:
        if transfer_account not in temp_dictionary.keys():
            transfer_account = input("This account does not exist, please re-enter the username: ")
        else:
            break
    transfer_amount = input("Please enter the amount you would like to transfer: (£) ")
    while True:
        # check that the amount has no negative sign and is either a whole number or has 2 decimal places
        if "." not in transfer_amount and "-" not in transfer_amount \
            or "." in transfer_amount and len(transfer_amount.rsplit(".")[-1]) == 2:
            # try converting the amount to a float, if this isn't possible, ask user to re-enter the amount
            try:
                transfer_amount = float(transfer_amount)
            except:
                transfer_amount = input("You have entered an invalid amount, please re-enter: (£) ")
            # if the amount is converted to a float successfully and check if it's less than the user's balance
            else:
                # if the amount is less than the user's balance, break out of the while loop
                if transfer_amount <= temp_dictionary[username][3]:
                    break
                # if the amount is more than the user's balance, ask user to re-enter amount
                else:
                    transfer_amount = input("You do not have enough money in your account. Please re-enter: (£) ")
        else:
            transfer_amount = input("You have entered an invalid amount, please re-enter: (£) ")
    while True:
        # check the transfer amount is less than how much the user has in their account
        if transfer_amount <= temp_dictionary[username][3]:
                # add the amount to the account of the user entered and deduct from the current user 
                temp_dictionary[transfer_account][3] += transfer_amount
                temp_dictionary[username][3] -= transfer_amount
                print(f"""
                    We have transfered £{transfer_amount: .2f} to {transfer_account}.
                    Your new balance is £{temp_dictionary[username][3]: .2f}
                    """)
                break
        else:
            transfer_amount = input("You do not have enough money in your account for this transfer. Please enter another amount (£): ")
    return temp_dictionary

# function for depositing money into the user's account
def deposit_money(username, temp_dictionary):
    deposit_amount = input("Please enter the amount you would like to deposit into your account: (£) ")
    while True:
        # only enter the Try Except block if the amount has no negative sign, and is either a whole number or has 2 decimal places
        if "." not in deposit_amount and "-" not in deposit_amount or "." in deposit_amount and len(deposit_amount.rsplit(".")[-1]) == 2:
            # try converting the amount to a float, if this isn't possible, ask user to re-enter the amount
            try:
                deposit_amount = float(deposit_amount)
            except:
                deposit_amount = input("You have entered an invalid amount, please re-enter: (£) ")
            else:
                break
        else:
            deposit_amount = input("You have entered an invalid amount, please re-enter: (£) ")
    # add the deposit_amount into the user's account and display a message for the user         
    temp_dictionary[username][3] += deposit_amount
    print(f"""
            We have deposited £{deposit_amount: .2f} into your account.
            Your new balance is £{temp_dictionary[username][3]: .2f}
            """)
    return temp_dictionary

# function for withdrawing money from the user's account
def withdraw_money(username, temp_dictionary):
    # ask user to enter the amount they would like to withdraw
    withdraw_amount = input("Please enter the amount you would like to withdraw from your account: (£) ")
    # enter while True loop that continues looping until the amount is valid
    while True:
        # try to convert the withdraw_amount into a float and set this as a separate variable
        try:
            withdraw_amount_float = float(withdraw_amount)
        # if the amount can't be converted to a float, ask user to enter amount in again
        except:
            withdraw_amount = input("You have entered an invalid amount, please re-enter: (£) ")
        # if the withdraw_amount was successfully converted to a float, check if the amount is either a whole number or has 2 decimal places
        else:
            if "." not in withdraw_amount and "-" not in withdraw_amount or "." in withdraw_amount and len(withdraw_amount.rsplit(".")[-1]) == 2:
                # check if the amount is less than the user's available funds, if it is then break out of the while loop
                if withdraw_amount_float <= temp_dictionary[username][3]:
                    break
                else:
                    # if the amount is not less than the user's available funds, ask them to re-enter
                    withdraw_amount = input("You don't have enough money in your account, please re-enter: (£) ")
            else:
                # if the amount was not a whole number or has 2 decimal places, ask user to re-enter the amount
                withdraw_amount = input("You have entered an invalid amount, please re-enter: (£) ")
    # subtract the withdraw_amount from the user's account and display a message for the user         
    temp_dictionary[username][3] -= withdraw_amount_float
    print(f"""
            Your new balance is £{temp_dictionary[username][3]: .2f}
            """)
    return temp_dictionary

# function for changing the user's PIN number
def change_pin(username, temp_dictionary):
    # ask user for their new pin
    new_pin1 = input("Please enter your desired 4 digit pin: ")
    while True:
        # check whether the pin is 4 digits
        if len(new_pin1) != 4:
            new_pin1 = input("Your pin must contain 4 characters or numbers. Please re-enter your pin: ")
        elif new_pin1 == temp_dictionary[username][2]:
            new_pin1 = input("You have entered in the same pin as before. Please re-enter your new pin: ")
        else:
            new_pin2 = input("Please enter your desired pin again: ")
            # check if the pins match each other
            if new_pin1 == new_pin2:
                break
            else:
                new_pin1 = input("Your pins do not match. Please re-enter your pin ")
    # change pin in the txt document
    temp_dictionary[username][2] = new_pin1
    return temp_dictionary

# function for updating the login_credentials.txt once the user exits the program
def change_login_credentials_file(temp_dictionary):
     # set the keys of the temp_dictionary as a list
    keys = list(temp_dictionary.keys())
    # open login_credentials.txt and delete existing info
    file = open(r"C:\Users\Becky\Documents\CoGrammar\myenv\Tasks\login_credentials.txt", "r+")
    file.truncate(0)
    # loop through the number of keys, writing the info from the dictionary as a new line in the file
    for line in range(len(keys)):
        key = keys[line]
        file.write(temp_dictionary[key][0])
        file.write(",")
        file.write(" ")
        file.write(temp_dictionary[key][1])
        file.write(",")
        file.write(" ")
        file.write(key)
        file.write(",")
        file.write(" ")
        file.write(temp_dictionary[key][2])
        file.write(",")
        file.write(" ")
        file.write(str(temp_dictionary[key][3]))
        file.write("\n")
    file.close()

# create function which asks user if they would like to go back to the main menu or exit the program
# create a while loop for this so invalid inputs dealt with
def main_menu():
    menu = input("Enter 1 to go back to the main menu or 2 to exit: ")
    while True:
        # if the user would like to go back to the main menu, break out of the while loop
        if menu == "1":
            break
        # if the user would like to exit the program, update the login_credentials file and break out of the loop
        elif menu == "2":
            change_login_credentials_file(temp_dictionary)
            break
        # if something else is entered, print an error statement and go back through the while loop
        else:
            menu = input("You have entered an invalid number. Please re-enter: ")
    # return the menu option that the user entered
    return menu

while True:
    # ask user if they would like to login or register, convert to lower case and get rid of spaces
    login_or_register = input("Would you like to login or register? ").lower()
    login_or_register = login_or_register.replace(" ","")
    # if the user wants to login, run the login_check function
    if login_or_register == "login":
        login_check = login_check()
        # store the user's username and the temp_dictionary as variables to be used later
        username = login_check[0]
        temp_dictionary = login_check[1]
        break
    elif login_or_register == "register":
        # run the 'register' function and set the outcomes (username and temp_dictionary to variables)
        register = register()
        username = register[0]
        temp_dictionary = register[1]
        break
    # if 'login' or 'register' entered incorrectly, print error statement and go back through while loop
    else:
        print("You haven't entered 'login' or 'register' correctly. Please try again. ")

# print welcome message for user and menu options to select from 
print(f"""
        Hi {temp_dictionary[username][0].capitalize()},
        
        Welcome to your online banking system. 
      """)   
while True:
    print("""
          Please select from one of the following options:
          1 - Check balance
          2 - Transfer Funds
          3 - Deposit money
          4 - Withdraw money
          5 - Change PIN
          6 - Exit
          """)
    # if 'check balance' option is selected, display this amount rounded to 2dp
    option_selected = input("Enter 1, 2, 3, 4, 5 or 6: ")
    if option_selected == "1": 
        balance = temp_dictionary[username][3]
        print(f"Your balance is £{balance: .2f}")
        # ask if user would like to go back to the main menu or exit the program
        # call the main_menu function and set this as variable 'menu'
        menu = main_menu()
        # if the user wants to go back to the main menu, go back through the while loop
        if menu == "1":
            continue
        # if the user wants to exit the program, print a statement and break out
        elif menu == "2":
            print(f'''
                  Bye {temp_dictionary[username][0]}, see you next time!
                  ''')
            break
    
    # if user selects to transfer amount to another account, call the 'transfer_funds' function
    # and return the updated temp_dictionary
    elif option_selected == "2":
        temp_dictionary = transfer_funds(username, temp_dictionary) 
        # ask user if they would like to go back to the main menu or exit
        # call the main_menu function and set this as variable 'menu'
        menu = main_menu()
        # if the user wants to go back to the main menu, go back through the while loop
        if menu == "1":
            continue
        # if the user wants to exit the program, print a statement and break out
        elif menu == "2":
            print(f'''
                  Bye {temp_dictionary[username][0]}, see you next time!
                  ''')
            break

    # if user selects option to deposit money in, call the 'deposit_money' function
    elif option_selected == "3":
        temp_dictionary = deposit_money(username, temp_dictionary)
         # ask user if they would like to go back to the main menu or exit
        # call the main_menu function and set this as variable 'menu'
        menu = main_menu()
        # if the user wants to go back to the main menu, go back through the while loop
        if menu == "1":
            continue
        # if the user wants to exit the program, print a statement and break out
        elif menu == "2":
            print(f'''
                  Bye {temp_dictionary[username][0]}, see you next time!
                  ''')
            break
        
    # if user selects to withdraw money, call the 'withdraw_money" function
    elif option_selected == "4":
        temp_dictionary = withdraw_money(username, temp_dictionary)
        # ask user if they would like to go back to the main menu or exit
        # call the main_menu function and set this as variable 'menu'
        menu = main_menu()
        # if the user wants to go back to the main menu, go back through the while loop
        if menu == "1":
            continue
        # if the user wants to exit the program, print a statement and break out
        elif menu == "2":
            print(f'''
                  Bye {temp_dictionary[username][0]}, see you next time!
                  ''')
            break
        
    # if user selects to change PIN, call the "change_pin" function
    elif option_selected == "5":
        temp_dictionary = change_pin(username, temp_dictionary)
        # ask user if they would like to go back to the main menu or exit
        # call the main_menu function and set this as variable 'menu'
        menu = main_menu()
        # if the user wants to go back to the main menu, go back through the while loop
        if menu == "1":
            continue
        # if the user wants to exit the program, print a statement and break out
        elif menu == "2":
            print(f'''
                  Bye {temp_dictionary[username][0]}, see you next time!
                  ''')
            break
    
    # if option 6 is selected by the user, print a statement and exit the program
    elif option_selected == "6":
        print(f'''
              Bye {temp_dictionary[username][0]}, see you next time!
              ''')
        change_login_credentials_file(temp_dictionary)
        break
    # if user didn't select a valid menu option, print an error statement and go back through the while loop
    else:
        print("Error - Your input was not recognised.")

