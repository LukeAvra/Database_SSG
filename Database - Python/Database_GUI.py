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



def newItemGUI():
    newItemWindow = tk.Tk()
    newItemWindow.geometry("600x400")
    newItemWindow.title('New Item')
    
    # variables for adding items
    newSerialNumber = tk.StringVar()
    newName = tk.StringVar()
    newRoom = tk.StringVar()
    newRack = tk.StringVar()
    newShelf = tk.StringVar()
    newShelfLocation = tk.StringVar()
    newQuantity = tk.StringVar()
    
    #Labels
    serialLabel = tk.Label(newItemWindow, text = 'Serial Number: ', font=('calibre', 12))
    nameLabel = tk.Label(newItemWindow, text = 'Item Name: ', font=('calibre', 12))
    roomLabel = tk.Label(newItemWindow, text = 'Room: ', font=('calibre', 12))
    rackLabel = tk.Label(newItemWindow, text = 'Rack Number: ', font=('calibre', 12))
    shelfLabel = tk.Label(newItemWindow, text = 'Shelf Number: ', font=('calibre', 12))
    shelfLocationLabel = tk.Label(newItemWindow, text = 'Shelf Location (#): ', font=('calibre', 12))
    quantityLabel = tk.Label(newItemWindow, text = 'Quantity: ', font=('calibre', 12))
    
    # Entry Fields
    serialEntry = tk.Entry(newItemWindow, textvariable = newSerialNumber, font=('calibre', 12))
    nameEntry = tk.Entry(newItemWindow, textvariable = newName, font=('calibre', 12))
    roomEntry = tk.Entry(newItemWindow, textvariable = newRoom, font=('calibre', 12))
    rackEntry = tk.Entry(newItemWindow, textvariable = newRack, font=('calibre', 12))
    shelfEntry = tk.Entry(newItemWindow, textvariable = newShelf, font=('calibre', 12))
    shelfLocationEntry = tk.Entry(newItemWindow, textvariable = newShelfLocation, font=('calibre', 12))
    quantityEntry = tk.Entry(newItemWindow, textvariable = newQuantity, font=('calibre', 12))
    
    # Combo Boxes (Can change to combo-boxes once all values are established for rooms, racks and shelves)
# =============================================================================
#     roomCombo = ttk.Combobox(state = 'readonly', values = roomsList)
#     rackCombo = ttk.Combobox(state = 'readonly', values = rackList)
#     shelfCombo = ttk.Combobox(state = 'readonly', values = shelfList)
# =============================================================================

    # Prefill name entry if passed in
    if selectedItem:
        nameEntry.insert(0, item_to_add.get())
    

    serialLabel.place(relx=.2, rely=.1, anchor='center')
    serialEntry.place(relx=.5, rely=.1, anchor='center')
    
    nameLabel.place(relx=.2, rely=.2, anchor='center')
    nameEntry.place(relx=.5, rely=.2, anchor='center')
    
    roomLabel.place(relx=.2, rely=.3, anchor='center')
    roomEntry.place(relx=.5, rely=.3, anchor='center')
    
    rackLabel.place(relx=.2, rely=.4, anchor='center')
    rackEntry.place(relx=.5, rely=.4, anchor='center')
    
    shelfLabel.place(relx=.2, rely=.5, anchor='center')
    shelfEntry.place(relx=.5, rely=.5, anchor='center')
    
    shelfLocationLabel.place(relx=.2, rely=.6, anchor='center')
    shelfLocationEntry.place(relx=.5, rely=.6, anchor='center')
    
    quantityLabel.place(relx=.2, rely=.7, anchor='center')
    quantityEntry.place(relx=.5, rely=.7, anchor='center')
    
    
    
    
    newItemWindow.mainloop()
    
    return

def adjustItemGUI(item_for_adjustment):
    print(item_for_adjustment)
    return

def addDataGUI():
    global selectedItem
    selectedItem = tk.StringVar()
    cur = DG.conn.cursor()
    userInputItem = '%' + item_to_add.get() + '%'
    sql = '''SELECT DISTINCT Name FROM main_inventory WHERE Name ILIKE %s'''
    cur.execute(sql, [userInputItem])
    records = cur.fetchall()
    if(records):
        def adjustItemHelper():
            selectedItem = invListbox.get(invListbox.curselection())
            adjustItemGUI(selectedItem)
            return
        
        invLabel = tk.Label(addItemWindow, text='Similar items found\nSelect item to adjust or click new item')
        invListbox = tk.Listbox(addItemWindow, width=40, height=5, selectmode = 'single')
        invScrollbar = tk.Scrollbar(addItemWindow)
        selectedItem = invListbox.curselection()
        adjustItemButton = tk.Button(addItemWindow, text='Adjust Item', command = adjustItemHelper)
        newItemButton = tk.Button(addItemWindow, text='New Item', command = lambda: [addItemWindow.destroy(), newItemGUI()])
        
        invLabel.place(relx=.4, rely=.3, anchor='center')
        invListbox.place(relx=.4, rely=.5, anchor='center')
        invScrollbar.place(relx=.59, rely=.5, anchor='center')
        adjustItemButton.place(relx=.4, rely=.75, anchor='center')
        newItemButton.place(relx=.6, rely=.75, anchor='center')
        
        
        invListbox.config(yscrollcommand = invScrollbar.set)
        invScrollbar.config(command = invListbox.yview)
        
        
        
        for i in range(len(records)):
            invListbox.insert(i, records[i][0])
            
        
    else:
        newItemGUI()
        return
        
    
        
    return

def addItemGUI():
    global addItemWindow
    addItemWindow = tk.Tk()
    addItemWindow.geometry("600x300")
    addItemWindow.title("Add Item")
    global item_to_add
    item_to_add = tk.StringVar()
    
    addItemLabel = tk.Label(addItemWindow, text = 'Item', font=('calibre', 12, 'bold'))
    addItemEntry = tk.Entry(addItemWindow, textvariable = item_to_add, font=('calibre', 12))
    addItemButton = tk.Button(addItemWindow, text = 'Add Item', command = addDataGUI)
    returnButton = tk.Button(addItemWindow, text = 'Return', command = lambda: [addItemWindow.destroy(), mainMenuAdmin()])
    addItemWindow.bind('<Return>', lambda e: addDataGUI())
    
    addItemLabel.place(relx=.2, rely=.15, anchor='center')
    addItemEntry.place(relx=.4, rely=.15, anchor='center')
    addItemButton.place(relx=.7, rely=.15, anchor='center')
    returnButton.place(relx=.85, rely=.8, anchor = 'center')
    
    
    addItemWindow.mainloop()
    
    return
    
    
def mainMenuAdmin():
    global mainMenuWindow
    global searchVar
    mainMenuWindow = tk.Tk()
    mainMenuWindow.geometry("600x400")
    mainMenuWindow.title("Main Menu")
    searchVar = tk.StringVar()
    
    # When SQL server is connected, use this instead of dummy list below
    rooms = ['All'] + DG.roomList()
    
    #roomList = ['All', 'Production', 'Manufacturing', 'Main Inventory']
    choiceList = ['Serial Number', 'Item Name']
    
    roomComboBox = ttk.Combobox(
                    state='readonly',
                    values = rooms
                    )
    searchChoiceBox = ttk.Combobox(
                        state='readonly',
                        values = choiceList
                        )
    roomComboBox.set('All')
    searchChoiceBox.set('Serial Number')
    
    searchInventoryLabel = tk.Label(mainMenuWindow, text='Search', font=('calibre', 12, 'bold'))
    searchInventoryEntry = tk.Entry(mainMenuWindow, textvariable = searchVar, font=('calibre', 12))
    viewAllButton = tk.Button(mainMenuWindow, text = "Display Full Inventory", command = lambda: [mainMenuWindow.destroy(), displayFullInventory()])
    addItemButton = tk.Button(mainMenuWindow, text = "Add Item", command = lambda: [mainMenuWindow.destroy(), addItemGUI()])
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
    
    mainMenuWindow.mainloop()
    

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
    