"""
Yahya Çakıcı 22050951010
Emirhan Tıpırdamaz 21050911015
"""

def welcoming():
    print("==================================================")
    print("                     Welcome                      ")
    print("         Please Select One Option From Below:     ")
    print("                     1-Register                   ")
    print("                     2-Sign In                    ")
    print("                     3-Exit                       ")
    print("==================================================")


def customer_menu():
    print("==================================================")
    print("        Basic Social Media Platform System        ")
    print("             1-Change Password                    ")
    print("             2-Change Username                    ")
    print("             3-Add Friend                         ")
    print("             4-Delete Friend                      ")
    print("             5-Show Friend List                   ")
    print("             6-Show Account Details               ")
    print("             7-Exit                               ")
    print("==================================================")


def registration():
    global all_names
    user_name = input("Please enter a user name: ")
    while True:
        all_names = []
        account = open("P_account_details.txt", "r")
        data = account.readlines()
        for i in data:
            k = i.rsplit(";")
            all_names.append(k[0])
        if user_name in all_names:
            user_name = input("This name has already taken. Please select try another user name: ")
            pass
        else:
            account.close()
            break

    password = input("Please enter a password: ")
    while True:
        number = False
        symbol = False
        lower = False
        upper = False
        character = False
        if len(password) >= 8:
            character = True
        else:
            print("Your Password Must Contain At Least Eight Character")
        for i in password:
            if i in numbers:
                number = True
            if i in symbols:
                symbol = True
            if i in lowercase:
                lower = True
            if i in uppercase:
                upper = True
        if number is False:
            print("Your Password Must Contain At Least One Number")
        if symbol is False:
            print("Your Password Must Contain At Least One Symbol")
        if lower is False:
            print("Your Password Must Contain At Least One Lowercase Letter")
        if upper is False:
            print("Your Password Must Contain At Least One Uppercase Letter")
        if number is True and symbol is True and lower is True and upper is True and character is True:
            temp_password = password
            password = input("Please enter your password once again: ")
            if temp_password == password:
                account = open("P_account_details.txt", "a")
                account.write(str(user_name) + ";" + str(password) + ";" + str(friend_list) + "\n")
                account.close()
                print("Account Has Been Successfully Created")
                break
            else:
                print("The passwords you entered are not the same. Please try again...")
                password = input("Please enter a password: ")
        else:
            password = input("Please enter a suitable password: ")


def sign_in():
    global user_name
    global password
    while True:
        a = 1
        user_name = input("Please enter your user name: ")
        password = input("Please enter your password: ")
        account = open("P_account_details.txt", "r")
        data = account.readlines()
        for i in data:
            k = i.rsplit(";")
            if user_name == k[0] and password == k[1]:
                account.close()
                print("You have successfully entered...")
                print("You are being redirected...")
                a = 0
        if a == 1:
            print("The information you entered is incorrect. Please try again...")
            pass
        else:
            break
    return user_name, password


def change_username():
    global new_username
    while True:
        all_names = []
        account = open("P_account_details.txt", "r")
        data = account.readlines()
        for i in data:
            k = i.rsplit(";")
            all_names.append(k[0])
        if new_username in all_names:
            new_username = input("This name has already taken. Please select try another new user name: ")
            pass
        else:
            account.close()
            break


def change_password():
    global new_password
    while True:
        number = False
        symbol = False
        lower = False
        upper = False
        character = False
        if len(password) >= 8:
            character = True
        else:
            print("Your Password Must Contain At Least Eight Character")
        for i in new_password:
            if i in numbers:
                number = True
            if i in symbols:
                symbol = True
            if i in lowercase:
                lower = True
            if i in uppercase:
                upper = True
        if number is False:
            print("Your Password Must Contain At Least One Number")
        if symbol is False:
            print("Your Password Must Contain At Least One Symbol")
        if lower is False:
            print("Your Password Must Contain At Least One Lowercase Letter")
        if upper is False:
            print("Your Password Must Contain At Least One Uppercase Letter")
        if number is True and symbol is True and lower is True and upper is True and character is True:
            temp_password = new_password
            new_password = input("Please enter your password once again: ")
            if temp_password == new_password:
                return new_password
            else:
                print("The passwords you entered are not the same. Please try again...")
                new_password = input("Please enter a new password: ")
        else:
            new_password = input("Please enter a new suitable password: ")


def add_friend():
    global friends_password
    global friend_list
    global friend_list2
    global friend
    global all_names
    while True:
        all_names = []
        account = open("P_account_details.txt", "r")
        data = account.readlines()
        account.close()
        for i in data:
            k = i.rsplit(";")
            all_names.append(k[0])
            if user_name == k[0]:
                a = k[2].rsplit("'")
                a = a[1::2]
                friend_list = a
            if friend == k[0]:
                friends_password = k[1]
                b = k[2].rsplit("'")
                b = b[1::2]
                friend_list2 = b
        if friend not in all_names:
            friend = input("This username does not exist. Please try another username: ")
            pass
        elif friend == user_name:
            friend = input("You cannot add yourself as a friend. Please try another username: ")
            pass
        elif friend in friend_list:
            friend = input("This user is already in your friend list. Please try another username: ")
        else:
            temp_friendlist = tuple(friend_list)
            temp_friendlist = list(temp_friendlist)
            temp_friendlist2 = tuple(friend_list2)
            temp_friendlist2 = list(temp_friendlist2)
            friend_list.append(friend)
            friend_list2.append(user_name)
            account = open("P_account_details.txt", "r")
            data = account.read()
            data = data.replace(user_name+";"+password+";"+str(temp_friendlist),
                                user_name+";"+password+";"+str(friend_list))
            data = data.replace(friend+";"+friends_password+";"+str(temp_friendlist2),
                                friend+";"+friends_password+";"+str(friend_list2))
            account = open("P_account_details.txt", "w")
            account.write(data)
            print("User has been added to your friend list...")
            account.close()
            return friend_list


def del_friend():
    global friends_password
    global friend_list
    global friend_list2
    global friend
    global all_names
    while True:
        all_names = []
        account = open("P_account_details.txt", "r")
        data = account.readlines()
        account.close()
        for i in data:
            k = i.rsplit(";")
            all_names.append(k[0])
            if user_name == k[0]:
                a = k[2].rsplit("'")
                a = a[1::2]
                friend_list = a
            if friend == k[0]:
                friends_password = k[1]
                b = k[2].split("'")
                b = b[1::2]
                friend_list2 = b
        if friend not in all_names:
            friend = input("This username does not exist. Please try another username: ")
            pass
        elif friend == user_name:
            friend = input("You cannot delete yourself from friend list. Please try another username: ")
            pass
        elif friend not in friend_list:
            friend = input("This user is not already in your friend list.. Please try another username: ")
        else:
            temp_friendlist = tuple(friend_list)
            temp_friendlist = list(temp_friendlist)
            temp_friendlist2 = tuple(friend_list2)
            temp_friendlist2 = list(temp_friendlist2)
            friend_list.remove(friend)
            friend_list2.remove(user_name)
            account = open("P_account_details.txt", "r")
            data = account.read()
            data = data.replace(user_name + ";" + password + ";" + str(temp_friendlist),
                                user_name + ";" + password + ";" + str(friend_list))
            data = data.replace(friend + ";" + friends_password + ";" + str(temp_friendlist2),
                                friend + ";" + friends_password + ";" + str(friend_list2))
            account = open("P_account_details.txt", "w")
            account.write(data)
            print("User has been deleted from your friend list...")
            account.close()
            return friend_list


def show_friend_list():
    global friend_list
    while True:
        account = open("P_account_details.txt", "r")
        data = account.readlines()
        account.close()
        for i in data:
            k = i.rsplit(";")
            if user_name == k[0]:
                a = k[2].rsplit("'")
                friend_list = a[1:len(a) - 1]
        break
    return friend_list


numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["<", ">", "|", "!", "'", "£", "^", "#", "+", "$", "%", "&", "/", "{", "(", "[", "]", ")", "}", "=", "*", "?",
           "-", "_", "@", ".", ":", ","]
lowercase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
             "v", "w", "x", "y", "z"]
uppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]

while True:
    all_names = []
    friend_list = []
    friend_list2 = []
    user_name = ""
    friends_password = ""
    password = ""
    welcoming()
    choice1 = str(input(">"))
    if choice1 == "1":
        registration()
    elif choice1 == "2":
        sign_in()
        while True:
            customer_menu()
            choice2 = str(input(">"))
            if choice2 == "1":
                with open("P_account_details.txt", "r") as account:
                    data = account.read()
                    new_password = input("Please enter your new password: ")
                    change_password()
                    data = data.replace(password, new_password)
                with open("P_account_details.txt", "w") as account:
                    account.write(data)
                    print("Your password has been successfully changed...")
                    break
            elif choice2 == "2":
                with open("P_account_details.txt", "r") as account:
                    data = account.read()
                    data = data.replace(password, "x")
                    new_username = input("Please enter your new username: ")
                    change_username()
                    data = data.replace(user_name, new_username)
                    data = data.replace("x", password)
                with open("P_account_details.txt", "w") as account:
                    account.write(data)
                    print("Your username has been successfully changed...")
                    break
            elif choice2 == "3":
                friend = input("Please enter the username to add friend: ")
                add_friend()
            elif choice2 == "4":
                friend = input("Please enter the username to delete from friend list: ")
                del_friend()
            elif choice2 == "5":
                print("Here is your friend list:"+ str(show_friend_list()))
            elif choice2 == "6":
                print("Current Username: " + str(user_name) + "\n" + "Current Password: " + str(password))
            elif choice2 == "7":
                print("Exiting from the system...")
                break
            else:
                print("Please Select a Valid Option!")
    elif choice1 == "3":
        print("Exiting from the system...")
        break
    else:
        print("Please Select a Valid Option!")

