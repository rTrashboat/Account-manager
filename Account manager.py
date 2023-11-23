import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import random
from cryptography.fernet import Fernet
import os

def main_thing():

    remove_list = []
    accounts =[]
    numbre_list = []
    try:
        broomed = False
        remove_command = False
        sealed = False
        layout2 = [
        [sg.Text("Title"),sg.Input(key="Input2-4",expand_x=True)],
        [sg.Text("Name"),sg.Input(key="Input2-1",expand_x=True)],
        [sg.Text("Email"),sg.Input(key="Input2-2",expand_x=True)],
        [sg.Text("Password"),sg.Input(key="Input2-3",expand_x=True),sg.Button("🔄",key="Button2-2"),sg.Button("⭐",key="Button2-3"),sg.Text("? of 10",key="Rating")],
        [sg.Button("Add", expand_x = True, key = "Button2-1"),sg.Button("🧹",key = "Button2-4")],
        [sg.Text("Accounts:",expand_x = True)]
        ]
        Window2 = sg.Window('Account manager', layout2, finalize = True)
        data3 = open("accounts.bin","r")
        accounts = data3.read()
        accounts = accounts.replace('"', '').replace("'", "").replace("[", "").replace("]", "")
        accounts = list(accounts.split(","))
        
        account_temp_list = []
        account_temp = []
        accounts_created = 0
        elements_scanned = 0
        for account in accounts:
            if elements_scanned == 0:
                Name_element = sg.Text(f"Name: {account}",expand_x=True)
                elements_scanned = 1
            elif elements_scanned == 1:
                Email_element = sg.Text(f"Email: {account}",expand_x=True)
                elements_scanned = 2
                
            elif elements_scanned == 2:
                Password_element = sg.Text(f"Password: {account}",expand_x=True)
                elements_scanned = 3
                
            elif elements_scanned == 3:
                Title_element = sg.Text(f"Title: {account}",expand_x=True)
                Remove_element = sg.Button("❌",key = f"Remove {accounts_created}" )
                 
                account_temp = [[Title_element,Name_element,Email_element,Password_element,Remove_element]]
                account_temp_list.append(account_temp)
                Window2.extend_layout(Window2,account_temp)
                account_temp = []
                remove_list.append(f"Remove {accounts_created}")
                elements_scanned = 0
                accounts_created += 1
    
    except FileNotFoundError:
        pass
    
    while Passwword_correct:
        event, values = Window2.read()
        if event == sg.WIN_CLOSED:
            save_layout(accounts)
            if not remove_command:
                sealed = True
            break
        if event == "Button2-1":
            Name_value = values["Input2-1"]
            Email_value = values["Input2-2"]
            Password_value = values["Input2-3"]
            Title_value = values["Input2-4"]
            if Name_value and Email_value and Password_value and Title_value:
                Name_element = sg.Text(f"Name: {Name_value}",expand_x=True)
                Email_element = sg.Text(f"Email: {Email_value}",expand_x=True)
                Password_element = sg.Text(f"Password: {Password_value}",expand_x=True)
                Title_element = sg.Text(f"Title: {Title_value}",expand_x=True)
                
    
                accounts.append(Name_value)
                accounts.append(Email_value)
                accounts.append(Password_value)
                accounts.append(Title_value)
    
                save_layout(accounts)
                Window2.close()
                remove_command=True
    
        elif event == "Button2-2":
            generated_password = generate_strong_password()
            Window2["Input2-3"].update(generated_password)
    
        elif event == "Button2-3":
            Password_value = values["Input2-3"]
            rating_result = rate_password(Password_value)
            Window2["Rating"].update(f"{rating_result} of 10")
    
        elif event == "Button2-4":
            pass

        elif event[0] == "R":
            remove_pressed = event
            remove_list.remove(remove_pressed)
            Window2[remove_pressed].hide_row()
            remove_pressed = remove_pressed * 4
            number = int(remove_pressed[-1])
            for i in range(4):
                accounts.remove(accounts[number])
            Window2.close()
            remove_command = True
    if not sealed:
        #Window2.close()
        main_thing()


def save_layout(layout):
    data2 = open("accounts.bin", "w")
    data2.write(str(layout))
    data2.close()

with open("Tempcache.key","rb") as mykey:
    mykey = mykey.read()

def generate_strong_password():
    while True:
        letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","/","-", "+", "*","$","_","%","/","-", "+", "*","$","_","%","/","-", "+", "*","$","_","%"]
        password = ""
        for char in range(random.randint(12,18)):
            choice = random.randint(0,4)
            if choice >= 1:
                password += random.choice(letters)
            else: password += str(random.randint(1,9))
        return password
        break

def rate_password(password):
    if password:
        contains_spaces = False
        password_rating = 0
        letters = 0
        numbers = 0
        symbols = 0
        uppercase = 0
        lowercase = 0
        for letter in password:
            if letter.isdigit():
                numbers += 1
            elif str(letter).isalpha():
                letters += 1
                if letter.isupper():
                    uppercase += 1
                elif letter.islower():
                    lowercase +=1
            elif letter.isspace():
                contains_spaces = True
            else:
                symbols += 1
        
        if letters > 0:
            password_rating += 1
        if numbers > 0:
            password_rating += 1
        elif numbers >= 3:
            password_rating += 2
        if uppercase > 0 and lowercase > 0:
            password_rating += 2
        if symbols > 0:
            password_rating += 2
        elif symbols > 2:
            password_rating += 2
        if len(password) > 12:
            password_rating += 2
        if password_rating >2:
            password_rating += 2
        if not contains_spaces:
            return password_rating
        else:
            return 0


Passwword_correct = False

sg.theme('DarkTeal1')
sg.set_options(icon = "icon.ico", font = "qualy")

layout = [
[sg.Text("MasterPassword", justification = "center", expand_x = True, size = (5,1))],
[sg.Input(key = "input1")],
[sg.Button("Confirm", key = "button1", expand_x = True)]
]


Window = sg.Window('Account manager', layout)

password = ""

while not Passwword_correct:
    event, values = Window.read()
    if event == sg.WIN_CLOSED: #or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "button1" and values["input1"] == password:
        Passwword_correct = True

Window.close()





if Passwword_correct:
    main_thing()