# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 08:32:28 2023

@author: Luke
"""
import tkinter as tk
from tkinter import ttk
import Database_Globals as DG
import random
import sys

sys.path.append('C:/Users/Luke/Documents/Python Scripts/Database_SSG/Database - Python')


def searchGUI():
    cur = DG.conn.cursor()
    #
    # WORK ON ME NEXT
    #
    if(searchType.get() == 'Barcode'):
        bar = searchVar.get()
        sql = '''SELECT * FROM barcodes WHERE code = %s'''
        cur.execute(sql, [bar])
        records = cur.fetchall()
        if(not records):
            tk.messagebox.showerror("Error", 'Item not found')
            return
        else:
            sql = '''SELECT ManufacturerID FROM ssg_test_inventory WHERE Barcode = %s'''
            cur.execute(sql, [records[0][0]])
            records = cur.fetchall()
            mainMenuWindow.destroy()
            adjustItemGUI(records[0][0])
            return
        
        return
        
    # Currently pulling full inventory and location records but just calling adjust item with the manufacturer ID
    elif(searchType.get() == 'Manufacturer ID'):
        invRecords, locRecords = DG.searchID(searchVar.get())
        if(invRecords == None or locRecords == None):
            tk.messagebox.showerror('Search Error', "Item not found in inventory")
            return
        else:
            mainMenuWindow.destroy()
            adjustItemGUI(invRecords[0][0])            
    elif(searchType.get() == "Item Name"):
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
        else:
            print("I have no idea how you managed to do that")
        return
    
    if(searchVar.get() == ""):
        mainMenu()      
    return

def addItemGUI():
    global addItemWindow
    addItemWindow = tk.Tk()
    addItemWindow.geometry("600x150")
    addItemWindow.title("Add Item")
    
    def newItem():
        newItemWindow = tk.Tk()
        newItemWindow.geometry("600x600")
        newItemWindow.title('New Item')
        
        cur = DG.conn.cursor()
        
        # If Else statements are to convert empty string to something that can be stored in SMALLINT
        # Could also be used to send warning when user tries to establish something without a data field
        def newItem():
            newManID = manIDEntry.get()
            newSupplierPartNum = SupplierPartNumEntry.get()
            newName = NameEntry.get()
# =============================================================================
#             newDescription = DescriptionEntry.get()
# =============================================================================
            newDescription = DescriptionEntry.get('1.0', tk.END)
            if(QuantityEntry.get() == ""):
                newQuantity = None
            else:
                newQuantity = QuantityEntry.get()
            newBarcode = BarcodeEntry.get()
            if(len(newBarcode) > 12):
                tk.messagebox.showerror('Error', 'Please Enter a valid 12 digit barcode')
                return
            if(bomIDEntry.get() == ""):
                newBomID = None
            else:   
                newBomID = bomIDEntry.get()
            newRoom = roomEntry.get()
            if(rackEntry.get() == ""):
                newRack = None
            else:
                newRack = rackEntry.get()
            
            if(shelfEntry.get() == ""):
                newShelf = None
            else:
                newShelf = shelfEntry.get()
            
            if(shelfLocationEntry.get() == ""):
                newShelfLocation = None
            else:
                newShelfLocation = shelfLocationEntry.get()
                
            # Check if Barcode is already in system, do extraneous checks, adding items doesn't have to be blazing fast
            sql = '''SELECT * FROM barcodes WHERE code = %s'''
            cur.execute(sql, [newBarcode])
            barRecords = cur.fetchall()
            sql = '''SELECT * FROM ssg_test_inventory WHERE Barcode = %s'''
            cur.execute(sql, [newBarcode])
            invBarRecords = cur.fetchall()
            sql = '''SELECT * FROM ssg_test_locations WHERE Barcode = %s'''
            cur.execute(sql, [newBarcode])
            locBarRecords = cur.fetchall()
            if(barRecords or locBarRecords or invBarRecords):
                tk.messagebox.showerror('Error', 'Barcode has already been found in our system')
                return
            
            # Check if Manufacturer ID is already in system
            sql = '''SELECT * FROM ssg_test_inventory WHERE ManufacturerID = %s'''
            cur.execute(sql, [newManID])
            manIDRecords = cur.fetchall()
            if(manIDRecords):
                tk.messagebox.showerror('Error', 'Manufacturer ID has already been found in our system')
                return
            
            
            sql='''INSERT INTO ssg_test_inventory (ManufacturerID, SupplierPartNum, Name, Description, Quantity, Barcode, BOM_ID)
                     VALUES (%s, %s, %s, %s, %s, %s, %s);
                 END'''
            cur.execute(sql, [newManID, newSupplierPartNum, newName, newDescription, newQuantity, newBarcode, newBomID])
            
            sql = '''INSERT INTO ssg_test_locations (Room, Rack, Shelf, Shelf_Location, Barcode)
                        VALUES (%s, %s, %s, %s, %s);
                    END'''
            cur.execute(sql, [newRoom, newRack, newShelf, newShelfLocation, newBarcode])
            
            sql = '''INSERT INTO barcodes (code) VALUES (%s); END'''
            cur.execute(sql, [newBarcode])        
            
            print('Item should have been added')
            newItemWindow.destroy()
            addItemGUI()
            
            
            
        
        # variables for adding items
        manID = tk.StringVar()
        SupplierPartNum = tk.StringVar()
        Name = tk.StringVar()
# =============================================================================
#         Description = tk.StringVar()
# =============================================================================
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
        DescriptionLabel = tk.Label(newItemWindow, text = 'Description: (100 Chars)', font=('calibre', 12))
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
        
# =============================================================================
#         DescriptionEntry = tk.Entry(newItemWindow, textvariable = Description, font=('calibre', 12))
# =============================================================================
        DescriptionEntry = tk.Text(newItemWindow, font = ('calibre', 12), width = 20, height = 3)
        
        QuantityEntry = tk.Entry(newItemWindow, textvariable = Quantity, font=('calibre', 12))
        BarcodeEntry = tk.Entry(newItemWindow, textvariable = Barcode, font=('calibre', 12))
        bomIDEntry = tk.Entry(newItemWindow, textvariable = bomID, font=('calibre', 12))
        roomEntry = tk.Entry(newItemWindow, textvariable = room, font=('calibre', 12))
        rackEntry = tk.Entry(newItemWindow, textvariable = rack, font=('calibre', 12))
        shelfEntry = tk.Entry(newItemWindow, textvariable = shelf, font=('calibre', 12))
        shelfLocationEntry = tk.Entry(newItemWindow, textvariable = shelfLocation, font=('calibre', 12))
        
        
        manIDLabel.place(relx=.05, rely=.1, anchor='w')
        manIDEntry.place(relx=.55, rely=.1, anchor='center')
        
        SupplierPartNumLabel.place(relx=.05, rely=.15, anchor='w')
        SupplierPartNumEntry.place(relx=.55, rely=.15, anchor='center')
        
        NameLabel.place(relx=.05, rely=.2, anchor='w')
        NameEntry.place(relx=.55, rely=.2, anchor='center')
        
        DescriptionLabel.place(relx=.05, rely=.275, anchor='w')
        DescriptionEntry.place(relx=.55, rely=.3, anchor='center')
        
        QuantityLabel.place(relx=.05, rely=.4, anchor='w')
        QuantityEntry.place(relx=.55, rely=.4, anchor='center')
        
        BarcodeLabel.place(relx=.05, rely=.45, anchor='w')
        BarcodeEntry.place(relx=.55, rely=.45, anchor='center')
        
        bomIDLabel.place(relx=.05, rely=.5, anchor='w')
        bomIDEntry.place(relx=.55, rely=.5, anchor='center')
        
        roomLabel.place(relx=.05, rely=.55, anchor='w')
        roomEntry.place(relx=.55, rely=.55, anchor='center')
        
        rackLabel.place(relx=.05, rely=.6, anchor='w')
        rackEntry.place(relx=.55, rely=.6, anchor='center')
        
        shelfLabel.place(relx=.05, rely=.65, anchor='w')
        shelfEntry.place(relx=.55, rely=.65, anchor='center')
        
        shelfLocationLabel.place(relx=.05, rely=.7, anchor='w')
        shelfLocationEntry.place(relx=.55, rely=.7, anchor='center')
        
        if(item_to_add_manID.get() != ""):
            manIDEntry.insert(0, item_to_add_manID.get())
        
        createButton = tk.Button(newItemWindow, text = 'Add', command = newItem)
        createButton.place(relx=.5, rely = .775, anchor='center')
        
        returnButton = tk.Button(newItemWindow, text = 'Return', command = lambda: [newItemWindow.destroy(), addItemGUI()])
        returnButton.place(relx=.7, rely=.775, anchor='center')
        
        barcodeGeneratorButton = tk.Button(newItemWindow, text = "Generate Barcode", command = lambda:[generateBarcode(barcodeEntry, checkDigitLabel)])
        barcodeGeneratorButton.place(relx=.6, rely=.9, anchor='center')
        barcodeEntry = tk.Entry(newItemWindow, font=('calibre', 12))
        barcodeEntry.place(relx=.5, rely=.85, anchor = 'center')
        checkDigitLabel = tk.Label(newItemWindow, text = '', font=('calibre', 12))
        checkDigitLabel.place(relx=.7, rely=.85, anchor = 'center')
        

        newItemWindow.mainloop()
        
        return
    
    def dataCheck():
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
            newItem()
            return
        return
    
    global item_to_add_manID
    item_to_add_manID = tk.StringVar()
    
    addItemManufacturerLabel = tk.Label(addItemWindow, text = 'Manufacturer ID:', font=('calibre', 12, 'bold'))
    addItemManufacturerEntry = tk.Entry(addItemWindow, textvariable = item_to_add_manID, font=('calibre', 12))
    addItemManufacturerButton = tk.Button(addItemWindow, text = 'Add Item', command = dataCheck)
    returnButton = tk.Button(addItemWindow, text = 'Return', command = lambda: [addItemWindow.destroy(), mainMenu()])
    addItemManufacturerEntry.bind('<Return>', lambda e: dataCheck())

    addItemManufacturerLabel.place(relx=.116, rely=.4, anchor='center')
    addItemManufacturerEntry.place(relx=.4, rely=.4, anchor='center')
    addItemManufacturerButton.place(relx=.7, rely=.4, anchor='center')
    returnButton.place(relx=.85, rely=.8, anchor = 'center')
    
    addItemWindow.mainloop()
    
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
# =============================================================================
#         adjustedDescription = DescriptionEntry.get()
# =============================================================================
        adjustedDescription = DescriptionEntry.get('1.0', tk.END)
        
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
        
        sql = '''SELECT * FROM barcodes WHERE code = %s'''
        cur.execute(sql, [barcode_for_adjustment])
        records = cur.fetchall()
        if(records):
            sql='''UPDATE barcodes
                    SET code = %s
                    WHERE code = %s;
                    END'''
            cur.execute(sql, [adjustedBarcode, barcode_for_adjustment])
        else:
            sql = '''INSERT INTO barcodes (code) VALUES (%s)'''
            cur.execute(sql, [adjustedBarcode])
        
        adjustItemWindow.destroy()
        addItemGUI()
    
    # Quality of Life bullshit, work on when you have a minute to avoid extraneous windows sticking around
    # It gets pissy when checking the window state after it's already been destroyed
# =============================================================================
#     def adjustDestruction():
#         if(mainMenuWindow.state() == 'normal'):
#             print("Main Menu Open")
#             adjustItemWindow.destroy()
#         else:
#             adjustItemWindow.destroy()
#             mainMenu()
# =============================================================================
            
            
    manID = tk.StringVar()
    SupplierPartNum = tk.StringVar()
    Name = tk.StringVar()
# =============================================================================
#     Description = tk.StringVar()
# =============================================================================
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
# =============================================================================
#     DescriptionEntry = tk.Entry(adjustItemWindow, textvariable = Description, font=('calibre', 12))
# =============================================================================
    DescriptionEntry = tk.Text(adjustItemWindow, font = ('calibre', 12), width = 20, height = 3)
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
    DescriptionEntry.insert('end', invRecords[0][3])
    QuantityEntry.insert(0, invRecords[0][4])
    BarcodeEntry.insert(0, invRecords[0][5])
    if(invRecords[0][6] != None):
        bomIDEntry.insert(0, invRecords[0][6])
    roomEntry.insert(0, locRecords[0][0])
    rackEntry.insert(0, locRecords[0][1])
    shelfEntry.insert(0, locRecords[0][2])
    shelfLocationEntry.insert(0, locRecords[0][3])
    
# =============================================================================
#     manIDLabel.place(relx=.2, rely=.1, anchor='center')
#     manIDEntry.place(relx=.5, rely=.1, anchor='center')
#     
#     SupplierPartNumLabel.place(relx=.2, rely=.15, anchor='center')
#     SupplierPartNumEntry.place(relx=.5, rely=.15, anchor='center')
#     
#     NameLabel.place(relx=.2, rely=.2, anchor='center')
#     NameEntry.place(relx=.5, rely=.2, anchor='center')
#     
#     DescriptionLabel.place(relx=.2, rely=.25, anchor='center')
#     DescriptionEntry.place(relx=.5, rely=.25, anchor='center')
#     
#     QuantityLabel.place(relx=.2, rely=.3, anchor='center')
#     QuantityEntry.place(relx=.5, rely=.3, anchor='center')
#     
#     BarcodeLabel.place(relx=.2, rely=.35, anchor='center')
#     BarcodeEntry.place(relx=.5, rely=.35, anchor='center')
#     
#     bomIDLabel.place(relx=.2, rely=.4, anchor='center')
#     bomIDEntry.place(relx=.5, rely=.4, anchor='center')
#     
#     roomLabel.place(relx=.2, rely=.45, anchor='center')
#     roomEntry.place(relx=.5, rely=.45, anchor='center')
#     
#     rackLabel.place(relx=.2, rely=.5, anchor='center')
#     rackEntry.place(relx=.5, rely=.5, anchor='center')
#     
#     shelfLabel.place(relx=.2, rely=.55, anchor='center')
#     shelfEntry.place(relx=.5, rely=.55, anchor='center')
#     
#     shelfLocationLabel.place(relx=.2, rely=.6, anchor='center')
#     shelfLocationEntry.place(relx=.5, rely=.6, anchor='center')
# =============================================================================

    manIDLabel.place(relx=.05, rely=.1, anchor='w')
    manIDEntry.place(relx=.55, rely=.1, anchor='center')
    
    SupplierPartNumLabel.place(relx=.05, rely=.15, anchor='w')
    SupplierPartNumEntry.place(relx=.55, rely=.15, anchor='center')
    
    NameLabel.place(relx=.05, rely=.2, anchor='w')
    NameEntry.place(relx=.55, rely=.2, anchor='center')
    
    DescriptionLabel.place(relx=.05, rely=.275, anchor='w')
    DescriptionEntry.place(relx=.55, rely=.3, anchor='center')
    
    QuantityLabel.place(relx=.05, rely=.4, anchor='w')
    QuantityEntry.place(relx=.55, rely=.4, anchor='center')
    
    BarcodeLabel.place(relx=.05, rely=.45, anchor='w')
    BarcodeEntry.place(relx=.55, rely=.45, anchor='center')
    
    bomIDLabel.place(relx=.05, rely=.5, anchor='w')
    bomIDEntry.place(relx=.55, rely=.5, anchor='center')
    
    roomLabel.place(relx=.05, rely=.55, anchor='w')
    roomEntry.place(relx=.55, rely=.55, anchor='center')
    
    rackLabel.place(relx=.05, rely=.6, anchor='w')
    rackEntry.place(relx=.55, rely=.6, anchor='center')
    
    shelfLabel.place(relx=.05, rely=.65, anchor='w')
    shelfEntry.place(relx=.55, rely=.65, anchor='center')
    
    shelfLocationLabel.place(relx=.05, rely=.7, anchor='w')
    shelfLocationEntry.place(relx=.55, rely=.7, anchor='center')
    
    adjustButton = tk.Button(adjustItemWindow, text = 'Adjust', command = adjustItem)
    adjustButton.place(relx=.5, rely = .8, anchor='center')
    
    returnButton = tk.Button(adjustItemWindow, text = 'Home', command = lambda: [adjustItemWindow.destroy(), mainMenu()])
    #returnButton = tk.Button(adjustItemWindow, text = 'Home', command = adjustDestruction)
    returnButton.place(relx=.7, rely=.8, anchor='center')

    


    return

def removeItem():
    mainMenuWindow.destroy()
    removeItemWindow = tk.Tk()
    removeItemWindow.geometry("600x150")
    removeItemWindow.title("Remove Item")
    removeVar = tk.StringVar()
    
    def itemRemoval(item_to_remove):
        cur = DG.conn.cursor()
        sql = '''SELECT * FROM ssg_test_inventory WHERE ManufacturerID = %s'''
        cur.execute(sql, [item_to_remove])
        records = cur.fetchall()
        if(records):
            sql = '''DELETE FROM ssg_test_inventory WHERE ManufacturerID = %s'''
            cur.execute(sql, [item_to_remove])
            sql = '''DELETE FROM ssg_test_locations WHERE Barcode = %s'''
            cur.execute(sql, [records[0][5]])
            sql = '''DELETE FROM barcodes WHERE code = %s'''
            cur.execute(sql, [records[0][5]])
            
            print("Item:", item_to_remove, 'deleted')
        else:
            tk.messagebox.showerror('Error', 'Item not found in inventory')
                
    def removeCheck():
        #Double check that item should actually be removed
        removeCheckWindow = tk.Tk()
        removeCheckWindow.geometry("400x200")
        removeCheckWindow.title("Are you sure?")
        
        removeText = "Are you sure you want to remove item: " + removeVar.get()
        removeLabel = tk.Label(removeCheckWindow, text = removeText, font = ('calibre', 12))
        yesButton = tk.Button(removeCheckWindow, text = "Yes", command = lambda: [itemRemoval(removeVar.get()), removeCheckWindow.destroy()])
        noButton = tk.Button(removeCheckWindow, text = "No", command = removeCheckWindow.destroy)
        
        removeLabel.place(relx=.5, rely=.3, anchor='center')
        yesButton.place(relx=.2, rely=.6, anchor = 'center')
        noButton.place(relx=.8, rely=.6, anchor='center')   
        
        return
    
    removeItemLabel = tk.Label(removeItemWindow, text = "Manufacturer ID:", font=('calibre', 12))
    removeItemEntry = tk.Entry(removeItemWindow, textvariable = removeVar, font=('calibre', 12))  
    removeItemButton = tk.Button(removeItemWindow, text = 'Remove', command = removeCheck)
    homeButton = tk.Button(removeItemWindow, text = 'Home', command = lambda: [removeItemWindow.destroy(), mainMenu()])
    
    removeItemLabel.place(relx=.15, rely=.4, anchor='center')
    removeItemEntry.place(relx=.4, rely=.4, anchor='center')
    removeItemButton.place(relx=.7, rely=.4, anchor='center')
    homeButton.place(relx=.8, rely=.7, anchor='center')

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
            return
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
        
        # Might need to pull the following two lines into a helper function so 'checkInventory' can be called recursively
        # Maybe adjust so the function is called with the bomString variable
        # Or have the full 'bom in bomList' loop called in helper function and call checkInventory each time with 'bom' variable
        # Second one seems like a better idea
        
        bomString = bomID.get()
        bomList = [int(e.strip()) if e.strip().isdigit() else e for e in bomString.split(',')]
        
        
        
        for bom in bomList:
            bomTableName = "bom_" + str(bom)
            sql = '''SELECT * FROM information_schema.tables WHERE table_name = %s''';
            cur.execute(sql, [bomTableName])
            records = cur.fetchall()
            if(records):
                sql = '''SELECT ManufacturerID FROM BOM_%s'''
                cur.execute(sql, [bom])
                records = cur.fetchall()
                if(records):
                    for record in records:
                        sql = '''SELECT Quantity from ssg_test_inventory
                                WHERE ManufacturerID = %s;'''
                        cur.execute(sql, [record[0]])
                        quantity = cur.fetchall()
                        print("Manufacurer ID: ", record[0], "\nQuantity: ", quantity[0][0])
                        
                        sql = '''SELECT QuantityNeeded from BOM_%s WHERE ManufacturerID = %s'''
                        cur.execute(sql, [bom, record[0]])
                        bomQuantity = cur.fetchall()
                        print("Required: ", bomQuantity[0][0])
                        
            else:
                errorMessage = 'No BOM found for BOM #' + str(bom) 
                tk.messagebox.showerror('Error', errorMessage)
            
            
    
    
    bomEntry = tk.Entry(bomWindow, textvariable = bomID, font=('calibre', 12))
    bomEntry.focus()
    bomEntry.bind('<Return>', lambda e: checkInventory())
    createBomButton = tk.Button(bomWindow, text = "Create", command=createBom)
    checkInventoryButton = tk.Button(bomWindow, text="Check Inventory", command=checkInventory)
    returnButton = tk.Button(bomWindow, text = 'Return', command = lambda:[bomWindow.destroy(), mainMenu()])
    
    bomEntry.place(relx=.5, rely=.5, anchor = 'center')
    createBomButton.place(relx=.4, rely=.6, anchor = 'center')
    checkInventoryButton.place(relx=.6, rely=.6, anchor='center')
    returnButton.place(relx=.75, rely=.8, anchor='center')
    
    return

def generateBarcode(barcodeEntry, checkDigitLabel):
    cur = DG.conn.cursor()
    barcodeList = []
    barcodeString = ''
    odds = 0
    for i in range(0, 11):
        barcodeList.append(random.randrange(0, 10))
    for i in range(0, 11, 2):
        odds = odds + barcodeList[i]
    odds = odds * 3
    for i in range(1, 10, 2):
        odds = odds + barcodeList[i]            
    if(odds % 10 != 0):
        checkDigit = 10 - odds % 10
    else:
        checkDigit = 0
        
    for num in barcodeList:
        barcodeString += str(num)
    sqlCheck = barcodeString + str(checkDigit)        
    sql = '''SELECT * FROM barcodes WHERE code=%s'''
    cur.execute(sql, [sqlCheck])
    records = cur.fetchone()
    if records:
        generateBarcode(barcodeEntry, checkDigitLabel)
        return
    else:
        barcodeEntry.delete(0, tk.END)    
        barcodeEntry.insert(0, barcodeString)
        checkDigitLabel.configure(text=str(checkDigit))

def mainMenu():
    global mainMenuWindow
    global searchVar
    global searchType
    mainMenuWindow = tk.Tk()
    mainMenuWindow.geometry("600x400")
    mainMenuWindow.title("Main Menu")
    searchVar = tk.StringVar()
    searchType = tk.StringVar()
    mainMenuWindow.focus_set()
    
    # When SQL server is connected, use this instead of dummy list below
    choiceList = ['Barcode', 'Manufacturer ID', 'Item Name']
    
    searchChoiceBox = ttk.Combobox(
                        state='readonly',
                        values = choiceList,
                        textvariable=searchType
                        )
    searchChoiceBox.set('Barcode')
    
    def searchHelper(field):
        searchGUI()
        # May use later, currently just destroying the window so 'Home' Button from 'adjustItem' function doesn't add another main menu
        #field.delete(0, tk.END)
    

        
    searchInventoryLabel = tk.Label(mainMenuWindow, text='Search', font=('calibre', 12, 'bold'))
    searchInventoryEntry = tk.Entry(mainMenuWindow, textvariable = searchVar, font=('calibre', 12))  
    searchInventoryEntry.focus()
    searchInventoryEntry.bind('<Return>', lambda e: searchHelper(searchInventoryEntry))     
    searchErrorLabel = tk.Label(mainMenuWindow, text='', font=('calibre', 12), fg='red')
    searchButton = tk.Button(mainMenuWindow, text = "Search", command = lambda: [searchHelper(searchInventoryEntry)])
    addItemButton = tk.Button(mainMenuWindow, text = "Add Item", command = lambda: [mainMenuWindow.destroy(), addItemGUI()])
    removeItemButton = tk.Button(mainMenuWindow, text = "Delete Item", command = removeItem)
    createBomButton = tk.Button(mainMenuWindow, text = "BOMs", command = lambda: [mainMenuWindow.destroy(), createBOMWindow()])
    barcodeGeneratorButton = tk.Button(mainMenuWindow, text = "Generate Barcode", command = lambda:[generateBarcode(barcodeEntry, checkDigitLabel)])
    barcodeEntry = tk.Entry(mainMenuWindow, font=('calibre', 12))
    checkDigitLabel = tk.Label(mainMenuWindow, text = '', font=('calibre', 12))

    # Row 1
    searchInventoryLabel.place(relx=.15, rely=.1, anchor='center')
    searchInventoryEntry.place(relx=.38, rely=.1, anchor='center')    
    searchChoiceBox.place(relx=.67, rely=.1, anchor='center')
    searchButton.place(relx=.85, rely=.1, anchor='center')
    searchErrorLabel.place(relx=.38, rely=.15, anchor='center')
    
    # Row 2
    addItemButton.place(relx=.5, rely=.2, anchor='center')
    
    # Row 3
    removeItemButton.place(relx=.5, rely=.3, anchor='center')
    
    # Row 4
    createBomButton.place(relx=.5, rely=.4, anchor='center')
     
    # Row 5
    barcodeGeneratorButton.place(relx=.5, rely=.5, anchor='center')
    
    # Row 6
    barcodeEntry.place(relx=.5, rely=.6, anchor='center')
    checkDigitLabel.place(relx=.7, rely=.6, anchor='center')
    

    mainMenuWindow.mainloop()

if __name__ == '__main__':
    DG.main()
    
    mainMenu()

    DG.close()

    
# Can currently add the same barcode multiple times, can NOT allow that to happen