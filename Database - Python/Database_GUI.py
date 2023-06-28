# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 10:04:21 2023

@author: Stuck
"""
import tkinter as tk
import psycopg2
from config import config
from Database_Initial import *
import Database_Globals as DG


def main():
    
    global loginWindow
    loginWindow = tk.Tk()
    # Variables

    global userNameVar 
    userNameVar= tk.StringVar()
    global passVar 
    passVar = tk.StringVar()
    
    loginWindow.geometry("600x400")
    greeting = tk.Label(loginWindow, text="--------------------SSG Inventory Database--------------------")
    loginButton = tk.Button(
        loginWindow,
        text = "Login",
        width = 5,
        command = submitLogin
    )
    
    userNameLabel = tk.Label(loginWindow, text = 'Username', font=('calibre', 12, 'bold'))
    userNameEntry = tk.Entry(loginWindow, textvariable=userNameVar, font=('calibre', 12, 'normal'))
    passwordLabel = tk.Label(loginWindow, text = 'Password', font=('calibre', 12, 'bold'))
    passwordEntry = tk.Entry(loginWindow, textvariable=passVar, show="*", font=('calibre', 12, 'normal'))

    loginWindow.bind('<Return>', lambda e: submitLogin())

    greeting.place(relx=.5, rely=.1, anchor='center')
    userNameLabel.place(relx=.3, rely=.2, anchor='center')
    userNameEntry.place(relx=.6, rely=.2, anchor='center')
    passwordLabel.place(relx=.3, rely=.3, anchor='center')
    passwordEntry.place(relx=.6, rely=.3, anchor='center')
    
    loginButton.place(relx=.5, rely=.4, anchor='center')
    
    loginWindow.mainloop()
    
#
# Adjust to play with sql database of usernames/passwords
def submitLogin():
    username = userNameVar.get()
    password = passVar.get()
    if(username.lower() == 'admin'):
        if(password == 'password'):
            loginWindow.destroy()
            mainMenuAdmin()
            
def mainMenuAdmin():
    global mainMenuWindow
    mainMenuWindow = tk.Tk()
    
    viewAllButton = tk.Button(
        mainMenuWindow,
        text = "Display Full Inventory",
        command = displayFullInventory
    )
    viewAllButton.place(relx=.5, rely=.5, anchor='center')
    mainMenuWindow.mainloop()
    

# Needs to be written
# Display all inventory entries, scrollable list of some sort
################################
def displayFullInventory():
# =============================================================================
#     cur = conn.cursor()
#     sql = '''SELECT * FROM main_inventory'''
#     cur.execute(sql) 
#     
#     fullRecords = cur.fetchall()
#     clear()
#     printTable(fullRecords, 1)     
#     cur.close()
# =============================================================================
    displayAll()
    return
################################    

if __name__ == '__main__':
    DG.main()
    main()
    close()
    