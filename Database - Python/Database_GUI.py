# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 10:04:21 2023

@author: Stuck
"""
import tkinter as tk
from tkinter import ttk
import psycopg2
#from config import config
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
# =============================================================================
#     if(username.lower() == 'a'):
#         if(password == 'p'):
#             loginWindow.destroy()
#             mainMenuAdmin()
# =============================================================================
    # Testing Purposes
    loginWindow.destroy()
    mainMenuAdmin()
    
def removeItem():
    return

def addItem():
    return
    
    
def mainMenuAdmin():
    global mainMenuWindow
    global searchVar
    mainMenuWindow = tk.Tk()
    mainMenuWindow.geometry("600x400")
    mainMenuWindow.title("Main Menu")
    searchVar = tk.StringVar()
    
    # When SQL server is connected, use this instead of dummy list below
    #roomList=DG.roomList()
    
    roomList = ['All', 'Production', 'Manufacturing', 'Main Inventory']
    choiceList = ['Serial Number', 'Item Name']
    
    roomComboBox = ttk.Combobox(
                    state='readonly',
                    values = roomList
                    )
    searchChoiceBox = ttk.Combobox(
                        state='readonly',
                        values = choiceList
                        )
    roomComboBox.set('All')
    searchChoiceBox.set('Serial Number')
    
    searchInventoryLabel = tk.Label(mainMenuWindow, text='Search', font=('calibre', 12, 'bold'))
    searchInventoryEntry = tk.Entry(mainMenuWindow, textvariable = searchVar, font=('calibre', 12, 'bold'))
    viewAllButton = tk.Button(mainMenuWindow, text = "Display Full Inventory", command = lambda: [mainMenuWindow.destroy(), displayFullInventory()])
    addItemButton = tk.Button(mainMenuWindow, text = "Add Item", command = addItem)
    removeItemButton = tk.Button(mainMenuWindow, text = "Remove Item", command = removeItem)
  
    # Row 1
    searchInventoryLabel.place(relx=.085, rely=.1, anchor='center')
    searchInventoryEntry.place(relx=.3, rely=.1, anchor='center')    
    roomComboBox.place(relx=.6, rely=.1, anchor='center')
    searchChoiceBox.place(relx=.85, rely=.1, anchor='center')
    
    # Row 2
    viewAllButton.place(relx=.5, rely=.2, anchor='center')
    
    # Row 3
    addItemButton.place(relx=.5, rely=.3, anchor='center')
    
    # Row 4
    removeItemButton.place(relx=.5, rely=.4, anchor='center')
    

# Needs to be written
# Display all inventory entries, scrollable list of some sort
################################
def displayFullInventory():
    fullInventoryWindow = tk.Tk()
    fullInventoryWindow.geometry('+300+300')
    inventoryFrame = tk.Frame(fullInventoryWindow)
    inventoryFrame.pack(expand=True, padx = 15, pady=20)
    returnFrame = tk.Frame(fullInventoryWindow)
    returnFrame.pack(expand=True, padx = 15, pady = 20)
    
    #vertScroll = tk.Scrollbar(fullInventoryWindow)
    #vertScroll.pack(side = tk.RIGHT, fill = tk.Y)
    
    cur = DG.conn.cursor()
    sql = '''SELECT * FROM main_inventory'''
    cur.execute(sql) 
    records = cur.fetchall()

    rowCount = 0
    for record in records:
        for columnCount in range(len(record)):
            if(columnCount == 0 or columnCount > 2):
                entryField = tk.Entry(inventoryFrame, width=6)
                entryField.grid(row=rowCount, column=columnCount)
                entryField.insert(tk.END, record[columnCount])
            else:
                entryField = tk.Entry(inventoryFrame, width=20)
                entryField.grid(row=rowCount, column=columnCount)
                entryField.insert(tk.END, record[columnCount])
        rowCount = rowCount + 1
    cur.close()
    
    returnButton = tk.Button(
        returnFrame,
        text = "Return",
        command = lambda: [fullInventoryWindow.destroy(), mainMenuAdmin()] 
    )
    returnButton.pack()
    fullInventoryWindow.mainloop()
    
    
    return
################################    

if __name__ == '__main__':
    DG.main()
    main()
    DG.close()
    