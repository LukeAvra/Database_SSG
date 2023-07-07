# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 08:32:28 2023

@author: Luke
"""
import tkinter as tk
from tkinter import ttk
import Database_Globals as DG
import random


def removeItem():
    return


def adjustItemGUI(item_for_adjustment):
    cur = DG.conn.cursor()
    sql = '''SELECT Barcode FROM ssg_test_inventory
            WHERE ManufacturerID = %s'''
    cur.execute(sql, [item_for_adjustment])
    records = cur.fetchall()
    barcode_for_adjustment = records[0][0]
    invRecords, locRecords = DG.searchID(item_for_adjustment)
    
    adjustItemWindow = tk.Tk()
    adjustItemWindow.geometry("600x400")
    adjustItemWindow.title('Adjust Item')
    
    def adjustItem():
        adjustedManID = manIDEntry.get()
        adjustedSupplierPartNum = SupplierPartNumEntry.get()
        adjustedName = NameEntry.get()
        adjustedDescription = DescriptionEntry.get()
        
        if(QuantityEntry.get() == ""):
            adjustedQuantity = None
        else:
            adjustedQuantity = QuantityEntry.get()
            
        adjustedBarcode = BarcodeEntry.get()
        
        if(bomIDEntry.get() == ""):
            adjustedbomID = None
        else:
            adjustedbomID = bomIDEntry.get()
            
        adjustedroom = roomEntry.get()
        if(rackEntry.get() == ""):
            adjustedrack = None
        else:
            adjustedrack = rackEntry.get()
            
        if(shelfEntry.get() == ""):
            adjustedshelf = None
        else:
            adjustedshelf = shelfEntry.get()
            
        if(shelfLocationEntry.get() == ""):
            adjustedshelfLocation = None
        else:
            adjustedshelfLocation = shelfLocationEntry.get()
        
        #ManufacturerID, SupplierPartNum, Name, Description, Quantity, Barcode, BOM_ID
        sql = '''UPDATE ssg_test_inventory
                 SET ManufacturerID = %s, 
                     SupplierPartNum = %s, 
                     Name = %s, 
                     Description = %s, 
                     Quantity = %s, 
                     Barcode = %s, 
                     BOM_ID = %s
                 WHERE Barcode = %s;
                 END'''

        cur.execute(sql, [adjustedManID, adjustedSupplierPartNum, adjustedName, adjustedDescription, adjustedQuantity, adjustedBarcode, adjustedbomID, barcode_for_adjustment])
        
        sql = '''UPDATE ssg_test_locations
                 SET Room = %s,
                     Rack = %s,
                     Shelf = %s,
                     Shelf_Location = %s,
                     Barcode = %s
                 WHERE Barcode = %s;
                 END'''
        cur.execute(sql, [adjustedroom, adjustedrack, adjustedshelf, adjustedshelfLocation, adjustedBarcode, barcode_for_adjustment])
        adjustItemWindow.destroy()
        addItemGUI()
        
    
    manID = tk.StringVar()
    SupplierPartNum = tk.StringVar()
    Name = tk.StringVar()
    Description = tk.StringVar()
    Quantity = tk.StringVar()
    Barcode = tk.StringVar()
    bomID = tk.StringVar()
    room = tk.StringVar()
    rack = tk.StringVar()
    shelf = tk.StringVar()
    shelfLocation = tk.StringVar()
    
    manIDLabel = tk.Label(adjustItemWindow, text = 'Manufacturer ID: ', font=('calibre', 12))
    SupplierPartNumLabel = tk.Label(adjustItemWindow, text = 'Supplier Part Number: ', font=('calibre', 12))
    NameLabel = tk.Label(adjustItemWindow, text = 'Name: ', font=('calibre', 12))
    DescriptionLabel = tk.Label(adjustItemWindow, text = 'Description: ', font=('calibre', 12))
    QuantityLabel = tk.Label(adjustItemWindow, text = 'Quantity: ', font=('calibre', 12))
    BarcodeLabel = tk.Label(adjustItemWindow, text = 'Barcode: ', font=('calibre', 12))
    bomIDLabel = tk.Label(adjustItemWindow, text = 'BOM ID: ', font=('calibre', 12))
    roomLabel = tk.Label(adjustItemWindow, text = 'Room: ', font=('calibre', 12))
    rackLabel = tk.Label(adjustItemWindow, text = 'Rack: ', font=('calibre', 12))
    shelfLabel = tk.Label(adjustItemWindow, text = 'Shelf: ', font=('calibre', 12))
    shelfLocationLabel = tk.Label(adjustItemWindow, text = 'Shelf Location: ', font=('calibre', 12))
    
    manIDEntry = tk.Entry(adjustItemWindow, textvariable = manID, font=('calibre', 12))
    SupplierPartNumEntry = tk.Entry(adjustItemWindow, textvariable = SupplierPartNum, font=('calibre', 12))
    NameEntry = tk.Entry(adjustItemWindow, textvariable = Name, font=('calibre', 12))
    DescriptionEntry = tk.Entry(adjustItemWindow, textvariable = Description, font=('calibre', 12))
    QuantityEntry = tk.Entry(adjustItemWindow, textvariable = Quantity, font=('calibre', 12))
    BarcodeEntry = tk.Entry(adjustItemWindow, textvariable = Barcode, font=('calibre', 12))
    bomIDEntry = tk.Entry(adjustItemWindow, textvariable = bomID, font=('calibre', 12))
    roomEntry = tk.Entry(adjustItemWindow, textvariable = room, font=('calibre', 12))
    rackEntry = tk.Entry(adjustItemWindow, textvariable = rack, font=('calibre', 12))
    shelfEntry = tk.Entry(adjustItemWindow, textvariable = shelf, font=('calibre', 12))
    shelfLocationEntry = tk.Entry(adjustItemWindow, textvariable = shelfLocation, font=('calibre', 12))

    manIDEntry.insert(0, invRecords[0][0])
    SupplierPartNumEntry.insert(0, invRecords[0][1])
    NameEntry.insert(0,invRecords[0][2])
    DescriptionEntry.insert(0, invRecords[0][3])
    QuantityEntry.insert(0, invRecords[0][4])
    BarcodeEntry.insert(0, invRecords[0][5])
    if(invRecords[0][6] != None):
        bomIDEntry.insert(0, invRecords[0][6])
    roomEntry.insert(0, locRecords[0][0])
    rackEntry.insert(0, locRecords[0][1])
    shelfEntry.insert(0, locRecords[0][2])
    shelfLocationEntry.insert(0, locRecords[0][3])
    
    manIDLabel.place(relx=.2, rely=.1, anchor='center')
    manIDEntry.place(relx=.5, rely=.1, anchor='center')
    
    SupplierPartNumLabel.place(relx=.2, rely=.15, anchor='center')
    SupplierPartNumEntry.place(relx=.5, rely=.15, anchor='center')
    
    NameLabel.place(relx=.2, rely=.2, anchor='center')
    NameEntry.place(relx=.5, rely=.2, anchor='center')
    
    DescriptionLabel.place(relx=.2, rely=.25, anchor='center')
    DescriptionEntry.place(relx=.5, rely=.25, anchor='center')
    
    QuantityLabel.place(relx=.2, rely=.3, anchor='center')
    QuantityEntry.place(relx=.5, rely=.3, anchor='center')
    
    BarcodeLabel.place(relx=.2, rely=.35, anchor='center')
    BarcodeEntry.place(relx=.5, rely=.35, anchor='center')
    
    bomIDLabel.place(relx=.2, rely=.4, anchor='center')
    bomIDEntry.place(relx=.5, rely=.4, anchor='center')
    
    roomLabel.place(relx=.2, rely=.45, anchor='center')
    roomEntry.place(relx=.5, rely=.45, anchor='center')
    
    rackLabel.place(relx=.2, rely=.5, anchor='center')
    rackEntry.place(relx=.5, rely=.5, anchor='center')
    
    shelfLabel.place(relx=.2, rely=.55, anchor='center')
    shelfEntry.place(relx=.5, rely=.55, anchor='center')
    
    shelfLocationLabel.place(relx=.2, rely=.6, anchor='center')
    shelfLocationEntry.place(relx=.5, rely=.6, anchor='center')
    
    adjustButton = tk.Button(adjustItemWindow, text = 'Adjust', command = adjustItem)
    adjustButton.place(relx=.5, rely = .8, anchor='center')
    
    returnButton = tk.Button(adjustItemWindow, text = 'Return', command = lambda: [adjustItemWindow.destroy(), addItemGUI()])
    returnButton.place(relx=.7, rely=.8, anchor='center')

    


    return
#################################


def newItemGUI():
    newItemWindow = tk.Tk()
    newItemWindow.geometry("600x400")
    newItemWindow.title('New Item')
    
    cur = DG.conn.cursor()
    
    def newItem():
        newManID = manIDEntry.get()
        newSupplierPartNum = SupplierPartNumEntry.get()
        newName = NameEntry.get()
        newDescription = DescriptionEntry.get()
        if(QuantityEntry.get() == ""):
            newQuantity = None
        else:
            newQuantity = QuantityEntry.get()
        newBarcode = BarcodeEntry.get()
        if(bomIDEntry.get() == ""):
            newbomID = None
        else:   
            newbomID = bomIDEntry.get()
        newroom = roomEntry.get()
        if(rackEntry.get() == ""):
            newRack = None
        else:
            newrack = rackEntry.get()
        
        if(shelfEntry.get() == ""):
            newShelf = None
        else:
            newshelf = shelfEntry.get()
        
        if(shelfLocationEntry.get() == ""):
            newShelfLocation = None
        else:
            newshelfLocation = shelfLocationEntry.get()
        
        sql='''INSERT INTO ssg_test_inventory (ManufacturerID, SupplierPartNum, Name, Description, Quantity, Barcode, BOM_ID)
                 VALUES (%s, %s, %s, %s, %s, %s, %s);
             END'''
        cur.execute(sql, [newManID, newSupplierPartNum, newName, newDescription, newQuantity, newBarcode, newbomID])
        
        sql = '''INSERT INTO ssg_test_locations (Room, Rack, Shelf, Shelf_Location, Barcode)
                    VALUES (%s, %s, %s, %s, %s);
                END'''
        cur.execute(sql, [newroom, newrack, newshelf, newshelfLocation, newBarcode])
        
        print('Item should have been added')
        newItemWindow.destroy()
        addItemGUI()
        
        
        
    
    # variables for adding items
    manID = tk.StringVar()
    SupplierPartNum = tk.StringVar()
    Name = tk.StringVar()
    Description = tk.StringVar()
    Quantity = tk.StringVar()
    Barcode = tk.StringVar()
    bomID = tk.StringVar()
    room = tk.StringVar()
    rack = tk.StringVar()
    shelf = tk.StringVar()
    shelfLocation = tk.StringVar()
    
    # Labels 
    manIDLabel = tk.Label(newItemWindow, text = 'Manufacturer ID: ', font=('calibre', 12))
    SupplierPartNumLabel = tk.Label(newItemWindow, text = 'Supplier Part Number: ', font=('calibre', 12))
    NameLabel = tk.Label(newItemWindow, text = 'Name: ', font=('calibre', 12))
    DescriptionLabel = tk.Label(newItemWindow, text = 'Description: ', font=('calibre', 12))
    QuantityLabel = tk.Label(newItemWindow, text = 'Quantity: ', font=('calibre', 12))
    BarcodeLabel = tk.Label(newItemWindow, text = 'Barcode: ', font=('calibre', 12))
    bomIDLabel = tk.Label(newItemWindow, text = 'BOM ID: ', font=('calibre', 12))
    roomLabel = tk.Label(newItemWindow, text = 'Room: ', font=('calibre', 12))
    rackLabel = tk.Label(newItemWindow, text = 'Rack: ', font=('calibre', 12))
    shelfLabel = tk.Label(newItemWindow, text = 'Shelf: ', font=('calibre', 12))
    shelfLocationLabel = tk.Label(newItemWindow, text = 'Shelf Location: ', font=('calibre', 12))
    
    # Entry Fields
    manIDEntry = tk.Entry(newItemWindow, textvariable = manID, font=('calibre', 12))
    SupplierPartNumEntry = tk.Entry(newItemWindow, textvariable = SupplierPartNum, font=('calibre', 12))
    NameEntry = tk.Entry(newItemWindow, textvariable = Name, font=('calibre', 12))
    DescriptionEntry = tk.Entry(newItemWindow, textvariable = Description, font=('calibre', 12))
    QuantityEntry = tk.Entry(newItemWindow, textvariable = Quantity, font=('calibre', 12))
    BarcodeEntry = tk.Entry(newItemWindow, textvariable = Barcode, font=('calibre', 12))
    bomIDEntry = tk.Entry(newItemWindow, textvariable = bomID, font=('calibre', 12))
    roomEntry = tk.Entry(newItemWindow, textvariable = room, font=('calibre', 12))
    rackEntry = tk.Entry(newItemWindow, textvariable = rack, font=('calibre', 12))
    shelfEntry = tk.Entry(newItemWindow, textvariable = shelf, font=('calibre', 12))
    shelfLocationEntry = tk.Entry(newItemWindow, textvariable = shelfLocation, font=('calibre', 12))
    
    
    manIDLabel.place(relx=.2, rely=.1, anchor='center')
    manIDEntry.place(relx=.5, rely=.1, anchor='center')
    
    SupplierPartNumLabel.place(relx=.2, rely=.15, anchor='center')
    SupplierPartNumEntry.place(relx=.5, rely=.15, anchor='center')
    
    NameLabel.place(relx=.2, rely=.2, anchor='center')
    NameEntry.place(relx=.5, rely=.2, anchor='center')
    
    DescriptionLabel.place(relx=.2, rely=.25, anchor='center')
    DescriptionEntry.place(relx=.5, rely=.25, anchor='center')
    
    QuantityLabel.place(relx=.2, rely=.3, anchor='center')
    QuantityEntry.place(relx=.5, rely=.3, anchor='center')
    
    BarcodeLabel.place(relx=.2, rely=.35, anchor='center')
    BarcodeEntry.place(relx=.5, rely=.35, anchor='center')
    
    bomIDLabel.place(relx=.2, rely=.4, anchor='center')
    bomIDEntry.place(relx=.5, rely=.4, anchor='center')
    
    roomLabel.place(relx=.2, rely=.45, anchor='center')
    roomEntry.place(relx=.5, rely=.45, anchor='center')
    
    rackLabel.place(relx=.2, rely=.5, anchor='center')
    rackEntry.place(relx=.5, rely=.5, anchor='center')
    
    shelfLabel.place(relx=.2, rely=.55, anchor='center')
    shelfEntry.place(relx=.5, rely=.55, anchor='center')
    
    shelfLocationLabel.place(relx=.2, rely=.6, anchor='center')
    shelfLocationEntry.place(relx=.5, rely=.6, anchor='center')
    
    createButton = tk.Button(newItemWindow, text = 'Add', command = newItem)
    createButton.place(relx=.5, rely = .8, anchor='center')
    
    returnButton = tk.Button(newItemWindow, text = 'Return', command = lambda: [newItemWindow.destroy(), addItemGUI()])
    returnButton.place(relx=.7, rely=.8, anchor='center')

    newItemWindow.mainloop()
    
    return


# Present records, maybe in listbox
#
def searchGUI():
    cur = DG.conn.cursor()
    #print(searchVar.get(), searchType.get())
    if(searchType.get() == 'Manufacturer ID'):
        invRecords, locRecords = DG.searchID(searchVar.get())
        return
    ## Need to finish ##########################################################################################################
    elif(searchType.get() == 'Item Name'):
        mainMenuWindow.destroy()
        searchWindow = tk.Tk()
        searchWindow.title("Search Results")
        searchWindow.geometry("600x400")
        
        records = DG.searchByName(searchVar.get())
        if(records):
            def adjustItemHelper():
                selectedItem = invListbox.get(invListbox.curselection())
                sql = '''SELECT ManufacturerID FROM ssg_test_inventory WHERE Name=%s;'''
                cur.execute(sql, [selectedItem])
                ID_for_adjustment = cur.fetchall()
                searchWindow.destroy()
                adjustItemGUI(ID_for_adjustment[0][0])
                return
            
            invLabel = tk.Label(searchWindow, text='Similar items found\nSelect item to adjust or click new item')
            invListbox = tk.Listbox(searchWindow, width=40, height=5, selectmode = 'single')
            invScrollbar = tk.Scrollbar(searchWindow)
            selectedItem = invListbox.curselection()
            adjustItemButton = tk.Button(searchWindow, text='Adjust Item', command = adjustItemHelper)
            
            invLabel.place(relx=.4, rely=.3, anchor='center')
            invListbox.place(relx=.4, rely=.5, anchor='center')
            invScrollbar.place(relx=.59, rely=.5, anchor='center')
            adjustItemButton.place(relx=.4, rely=.75, anchor='center')
            
            invListbox.config(yscrollcommand = invScrollbar.set)
            invScrollbar.config(command = invListbox.yview)
            
            for i in range(len(records)):
                invListbox.insert(i, records[i][0])
        
        return
    
    if(searchVar.get() == ""):
        mainMenu()
    
    
        
    return

def addDataGUI():
    cur = DG.conn.cursor()
    sql = '''SELECT * FROM ssg_test_inventory
             WHERE ManufacturerID = %s'''
    cur.execute(sql, [item_to_add_manID.get()])
    records = cur.fetchall()
    if records:
        addItemWindow.destroy()
        adjustItemGUI(item_to_add_manID.get())
    else:
        addItemWindow.destroy()
        newItemGUI()
        return
    return

def addItemGUI():
    global addItemWindow
    addItemWindow = tk.Tk()
    addItemWindow.geometry("600x300")
    addItemWindow.title("Add Item")
    
    global item_to_add_manID
    item_to_add_manID = tk.StringVar()
    
    addItemManufacturerLabel = tk.Label(addItemWindow, text = 'Manufacturer ID:', font=('calibre', 12, 'bold'))
    addItemManufacturerEntry = tk.Entry(addItemWindow, textvariable = item_to_add_manID, font=('calibre', 12))
    addItemManufacturerButton = tk.Button(addItemWindow, text = 'Add Item', command = addDataGUI)
    returnButton = tk.Button(addItemWindow, text = 'Return', command = lambda: [addItemWindow.destroy(), mainMenu()])
    addItemManufacturerEntry.bind('<Return>', lambda e: addDataGUI())

    addItemManufacturerLabel.place(relx=.116, rely=.15, anchor='center')
    addItemManufacturerEntry.place(relx=.4, rely=.15, anchor='center')
    addItemManufacturerButton.place(relx=.7, rely=.15, anchor='center')
    returnButton.place(relx=.85, rely=.8, anchor = 'center')
    
    addItemWindow.mainloop()
    
    return

def createBOMWindow():
    bomWindow = tk.Tk()
    bomWindow.geometry("600x400")
    bomWindow.title("Bill of Materials")
    bomID = tk.StringVar()
    cur = DG.conn.cursor()
    
    def createBom():
        #print(bomID.get())
        sql='''SELECT * FROM ssg_test_inventory
                WHERE BOM_ID = %s'''
        cur.execute(sql, [bomID.get()])
        records = cur.fetchall()
        if records:
            tk.messagebox.showerror("showerror", "BOM ID already exists")
            bomWindow.destroy()
            createBOMWindow()
        else:
            tableName = "BOM_" + bomID.get()
            
            sql = '''CREATE TABLE IF NOT EXISTS %s(
                       ManufacturerID VARCHAR(100)
                       QuantityNeeded SMALLINT
                    )'''

            cur.execute(sql, [tableName])
            
            return
        
        return
    
    def checkInventory():
        bomString = bomID.get()
        
        bomList = [int(e.strip()) if e.strip().isdigit() else e for e in bomString.split(',')]
        for bom in bomList:
            bomTableName = "BOM_" + str(bom)
            print(bomTableName)
            sql = '''SELECT ManufacturerID FROM %s'''
            cur.execute(sql, [bomTableName])
            records = cur.fetchall()
            if(records):
                for record in records:
                    sql = '''SELECT Quantity from ssg_test_inventory
                            WHERE ManufacturerID = %s;'''
                    cur.execute(sql, [record[0][0]])
                    quantity = cur.fetchall()
                    print("Manufacurer ID: ", record[0][0], "\nQuantity: ", quantity)
    
    
    bomEntry = tk.Entry(bomWindow, textvariable = bomID, font=('calibre', 12))
    createBomButton = tk.Button(bomWindow, text = "Create", command=createBom)
    checkInventoryButton = tk.Button(bomWindow, text="Check Inventory", command=checkInventory)
    
    bomEntry.place(relx=.5, rely=.5, anchor = 'center')
    createBomButton.place(relx=.4, rely=.6, anchor = 'center')
    checkInventoryButton.place(relx=.6, rely=.6, anchor='center')
    
    return

def mainMenu():
    global mainMenuWindow
    global searchVar
    global searchType
    mainMenuWindow = tk.Tk()
    mainMenuWindow.geometry("600x400")
    mainMenuWindow.title("Main Menu")
    searchVar = tk.StringVar()
    searchType = tk.StringVar()
    
    # When SQL server is connected, use this instead of dummy list below
    choiceList = ['Manufacturer ID', 'Item Name']
    
    searchChoiceBox = ttk.Combobox(
                        state='readonly',
                        values = choiceList,
                        textvariable=searchType
                        )
    searchChoiceBox.set('Manufacturer ID')
    
    def generateBarcode():
        barcodeList = []
        odds = 0
        for i in range(0, 11):
            barcodeList.append(random.randrange(0, 10))
        for i in range(0, 11, 2):
            print(i)
            odds = odds + barcodeList[i]
        odds = odds * 3
        print('\n')
        for i in range(1, 10, 2):
            odds = odds + barcodeList[i]
            
        checkDigit = 10 - odds // 10
        print(barcodeList, checkDigit)
        
    
    searchInventoryLabel = tk.Label(mainMenuWindow, text='Search', font=('calibre', 12, 'bold'))
    searchInventoryEntry = tk.Entry(mainMenuWindow, textvariable = searchVar, font=('calibre', 12))  
    searchInventoryEntry.bind('<Return>', lambda e: searchGUI())
    searchButton = tk.Button(mainMenuWindow, text = "Search", command = searchGUI)
    addItemButton = tk.Button(mainMenuWindow, text = "Add Item", command = lambda: [mainMenuWindow.destroy(), addItemGUI()])
    removeItemButton = tk.Button(mainMenuWindow, text = "Remove Item", command = removeItem)
    createBomButton = tk.Button(mainMenuWindow, text = "BOMs", command = lambda: [mainMenuWindow.destroy(), createBOMWindow()])
    barcodeGeneratorButton = tk.Button(mainMenuWindow, text = "Generate Barcode", command = generateBarcode)
    
    # Row 1
    searchInventoryLabel.place(relx=.15, rely=.1, anchor='center')
    searchInventoryEntry.place(relx=.38, rely=.1, anchor='center')    
    searchChoiceBox.place(relx=.67, rely=.1, anchor='center')
    searchButton.place(relx=.85, rely=.1, anchor='center')
    
    # Row 2
    addItemButton.place(relx=.5, rely=.2, anchor='center')
    
    # Row 3
    removeItemButton.place(relx=.5, rely=.3, anchor='center')
    
    # Row 4
    createBomButton.place(relx=.5, rely=.4, anchor='center')
    
    # Row 5
    barcodeGeneratorButton.place(relx=.5, rely=.5, anchor='center')
    
    
    mainMenuWindow.mainloop()

if __name__ == '__main__':
    DG.main()
    
    mainMenu()

    DG.close()