# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 08:32:28 2023

@author: Luke
"""
import os
import sys
print(os.path.dirname(__file__))
sys.path.append('C:\\Users\\Luke\\Documents\\Python Scripts\\Database_SSG\\Database - Python')
import tkinter as tk
import ttk
import Database_Globals as DG
import random

def searchGUI(field):
    cur = DG.conn.cursor()
    if(searchType.get() == 'Barcode'):
        bar = searchVar.get()
        sql = '''SELECT * FROM ''' + DG.barDatabase + ''' WHERE code = %s'''
        cur.execute(sql, [bar])
        records = cur.fetchall()
        if(not records):
            tk.messagebox.showerror("Error", 'Item not found')
            field.delete(0, tk.END)
        else:
            sql = '''SELECT ManufacturerID FROM ''' + DG.invDatabase + ''' WHERE Barcode = %s'''
            cur.execute(sql, [records[0][0]])
            records = cur.fetchall()
            mainMenuWindow.destroy()
            adjustItemGUI(records[0][0])
        return
        
    # Currently pulling full inventory and location records but just calling adjust item with the manufacturer ID
    elif(searchType.get() == 'Manufacturer ID'):
        invRecords, locRecords = DG.searchID(searchVar.get().lower())
        if(invRecords == None or locRecords == None):
            tk.messagebox.showerror('Search Error', "Item not found in inventory")
            field.delete(0, tk.END)
            return
        else:
            mainMenuWindow.destroy()
            adjustItemGUI(invRecords[0][0])            
    elif(searchType.get() == 'Item Name'):
        records = DG.searchByName(searchVar.get())
        if(records):
            def adjustItemHelper():
                selectedItem = invListbox.get(invListbox.curselection())
                sql = '''SELECT ManufacturerID FROM ''' + DG.invDatabase + ''' WHERE Description=%s;'''
                cur.execute(sql, [selectedItem])
                ID_for_adjustment = cur.fetchall()
                searchWindow.destroy()
                adjustItemGUI(ID_for_adjustment[0][0])
                return
            mainMenuWindow.destroy()
            searchWindow = tk.Tk()
            searchWindow.title("Search Results")
            searchWindow.geometry("400x250")
            
            invLabel = tk.Label(searchWindow, text='Similar items found\nSelect item to adjust or click new item')
            invListbox = tk.Listbox(searchWindow, width=40, height=5, selectmode = 'single')
            invScrollbar = tk.Scrollbar(searchWindow)
            selectedItem = invListbox.curselection()
            adjustItemButton = tk.Button(searchWindow, text='Adjust Item', command = adjustItemHelper)
            homeButton = tk.Button(searchWindow, text = 'Home', command = lambda:[searchWindow.destroy(), mainMenu()])
            
            invLabel.place(relx=.5, rely=.15, anchor='center')
            invListbox.place(relx=.5, rely=.45, anchor='center')
            invScrollbar.place(relx=.79, rely=.45, anchor='center')
            adjustItemButton.place(relx=.5, rely=.75, anchor='center')
            homeButton.place(relx=.5, rely=.9, anchor='center')
            
            invListbox.config(yscrollcommand = invScrollbar.set)
            invScrollbar.config(command = invListbox.yview)
            
            for i in range(len(records)):
                invListbox.insert(i, records[i][0])
                
            searchWindow.mainloop()
        else:
            tk.messagebox.showerror("Error", "Nothing found with that name")
            field.delete(0, tk.END)
            
    else:
        print("I have no idea how you managed to do that")
        print(searchType.get())
        field.delete(0, tk.END)
    return
    
    if(searchVar.get() == ""):
        mainMenu()      
    return

def addItemGUI():
    global addItemWindow
    addItemWindow = tk.Tk()
    addItemWindow.geometry("600x150")
    addItemWindow.title("Add Item")
    
    def newItemGUI():
        newItemWindow = tk.Tk()
        newItemWindow.geometry("600x600")
        newItemWindow.title('New Item')
        cur = DG.conn.cursor()
        
        # If Else statements are to convert empty string to something that can be stored in SMALLINT
        # Could also be used to send warning when user tries to establish something without a data field
        def newItem():
            if(manIDEntry.get() == ""):
                newManID = None
            else:
                newManID = manIDEntry.get().lower()
                
            if(manNameEntry.get() == ""):
                newManName = None
            else:
                newManName = manNameEntry.get().lower()
                
            if(SupplierPartNumEntry.get() == ""):
                newSupplierPartNum = None
            else:
                newSupplierPartNum = SupplierPartNumEntry.get()
            
            if(SupplierNameEntry.get() == ""):
                newSupplierName = None
            else:
                newSupplierName = SupplierNameEntry.get().lower()
            
            #newName = NameEntry.get()
            
            newDescription = DescriptionEntry.get('1.0', tk.END).strip()
            
            if(QuantityEntry.get() == ""):
                newQuantity = None
            else:
                newQuantity = QuantityEntry.get()
                
            newBarcode = BarcodeEntry.get()
            if(len(newBarcode) != 12):
                tk.messagebox.showerror('Error', 'Please Enter a valid 12 digit barcode')
                return

            newBomID = None
            
            if(roomEntry.get() == ""):
                newRoom = None
            else:
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
            sql = '''SELECT * FROM ''' + DG.barDatabase + ''' WHERE code = %s'''
            cur.execute(sql, [newBarcode])
            barRecords = cur.fetchall()
            sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE Barcode = %s'''
            cur.execute(sql, [newBarcode])
            invBarRecords = cur.fetchall()
            sql = '''SELECT * FROM ''' + DG.locDatabase + ''' WHERE Barcode = %s'''
            cur.execute(sql, [newBarcode])
            locBarRecords = cur.fetchall()
            if(barRecords or locBarRecords or invBarRecords):
                tk.messagebox.showerror('Error', 'Barcode has already been found in our system')
                return
            
            # Check if Manufacturer ID is already in system
            sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE ManufacturerID = %s'''
            cur.execute(sql, [newManID])
            manIDRecords = cur.fetchall()
            if(manIDRecords):
                tk.messagebox.showerror('Error', 'Manufacturer ID has already been found in our system')
                return
            
            
            sql='''INSERT INTO ''' + DG.invDatabase + ''' (ManufacturerID, Manufacturer, SupplierPartNum, Supplier, Description, Quantity, Barcode, BOM_ID)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                 END'''
            cur.execute(sql, [newManID, newManName, newSupplierPartNum, newSupplierName, newDescription, newQuantity, newBarcode, newBomID])
            
            sql = '''INSERT INTO ''' + DG.locDatabase + ''' (Room, Rack, Shelf, Shelf_Location, Barcode)
                        VALUES (%s, %s, %s, %s, %s);
                    END'''
            cur.execute(sql, [newRoom, newRack, newShelf, newShelfLocation, newBarcode])
            
            sql = '''INSERT INTO ''' + DG.barDatabase + ''' (code) VALUES (%s); END'''
            cur.execute(sql, [newBarcode])        
            
            print('Item should have been added')
            newItemWindow.destroy()
            addItemGUI()

        # variables for adding items
        manID = tk.StringVar()
        manName = tk.StringVar()
        SupplierPartNum = tk.StringVar()
        supplierName = tk.StringVar()
        #Name = tk.StringVar()
        Quantity = tk.StringVar()
        Barcode = tk.StringVar()
        room = tk.StringVar()
        rack = tk.StringVar()
        shelf = tk.StringVar()
        shelfLocation = tk.StringVar()
        
        # Labels 
        manIDLabel = tk.Label(newItemWindow, text = 'Manufacturer Number: ', font=('calibre', 12))
        manNameLabel = tk.Label(newItemWindow, text = 'Manufacturer: ', font=('calibre', 12))
        SupplierPartNumLabel = tk.Label(newItemWindow, text = 'Supplier Part Number: ', font=('calibre', 12))
        SupplierNameLabel = tk.Label(newItemWindow, text = 'Supplier Name: ', font=('calibre', 12))
        
        
        #NameLabel = tk.Label(newItemWindow, text = 'Name: ', font=('calibre', 12))
        DescriptionLabel = tk.Label(newItemWindow, text = 'Description: (100 Chars max)', font=('calibre', 12))
        QuantityLabel = tk.Label(newItemWindow, text = 'Quantity: ', font=('calibre', 12))
        BarcodeLabel = tk.Label(newItemWindow, text = 'Barcode: ', font=('calibre', 12))
        roomLabel = tk.Label(newItemWindow, text = 'Room: ', font=('calibre', 12))
        rackLabel = tk.Label(newItemWindow, text = 'Rack: ', font=('calibre', 12))
        shelfLabel = tk.Label(newItemWindow, text = 'Shelf: ', font=('calibre', 12))
        shelfLocationLabel = tk.Label(newItemWindow, text = 'Shelf Location: ', font=('calibre', 12))
        
        # Entry Fields
        manIDEntry = tk.Entry(newItemWindow, textvariable = manID, font=('calibre', 12))
        manNameEntry = tk.Entry(newItemWindow, textvariable = manName, font=('calibre', 12))
        SupplierPartNumEntry = tk.Entry(newItemWindow, textvariable = SupplierPartNum, font=('calibre', 12))
        SupplierNameEntry = tk.Entry(newItemWindow, textvariable = supplierName, font=('calibre', 12))
        
        #NameEntry = tk.Entry(newItemWindow, textvariable = Name, font=('calibre', 12))    
        DescriptionEntry = tk.Text(newItemWindow, font = ('calibre', 12), width = 20, height = 3)
        QuantityEntry = tk.Entry(newItemWindow, textvariable = Quantity, font=('calibre', 12))
        BarcodeEntry = tk.Entry(newItemWindow, textvariable = Barcode, font=('calibre', 12))
        roomEntry = tk.Entry(newItemWindow, textvariable = room, font=('calibre', 12))
        rackEntry = tk.Entry(newItemWindow, textvariable = rack, font=('calibre', 12))
        shelfEntry = tk.Entry(newItemWindow, textvariable = shelf, font=('calibre', 12))
        shelfLocationEntry = tk.Entry(newItemWindow, textvariable = shelfLocation, font=('calibre', 12))
               
        manIDLabel.place(relx=.05, rely=.1, anchor='w')
        manIDEntry.place(relx=.6, rely=.1, anchor='center')
        
        manNameLabel.place(relx=.05, rely=.15, anchor='w')
        manNameEntry.place(relx=.6, rely=.15, anchor='center')
        
        SupplierPartNumLabel.place(relx=.05, rely=.2, anchor='w')
        SupplierPartNumEntry.place(relx=.6, rely=.2, anchor='center')
        
        SupplierNameLabel.place(relx=.05, rely=.25, anchor='w')
        SupplierNameEntry.place(relx=.6, rely=.25, anchor='center')
        
        #NameLabel.place(relx=.05, rely=.2, anchor='w')
        #NameEntry.place(relx=.55, rely=.2, anchor='center')
        
        DescriptionLabel.place(relx=.05, rely=.325, anchor='w')
        DescriptionEntry.place(relx=.6, rely=.35, anchor='center')
        
        QuantityLabel.place(relx=.05, rely=.45, anchor='w')
        QuantityEntry.place(relx=.6, rely=.45, anchor='center')
        
        BarcodeLabel.place(relx=.05, rely=.5, anchor='w')
        BarcodeEntry.place(relx=.6, rely=.5, anchor='center')
        
        roomLabel.place(relx=.05, rely=.55, anchor='w')
        roomEntry.place(relx=.6, rely=.55, anchor='center')
        
        rackLabel.place(relx=.05, rely=.6, anchor='w')
        rackEntry.place(relx=.6, rely=.6, anchor='center')
        
        shelfLabel.place(relx=.05, rely=.65, anchor='w')
        shelfEntry.place(relx=.6, rely=.65, anchor='center')
        
        shelfLocationLabel.place(relx=.05, rely=.7, anchor='w')
        shelfLocationEntry.place(relx=.6, rely=.7, anchor='center')
        
        if(item_to_add_manID.get() != ""):
            manIDEntry.insert(0, item_to_add_manID.get().lower())
            manNameEntry.focus_force()
        else:
            manIDEntry.focus_force()
        
        createButton = tk.Button(newItemWindow, text = 'Add', command = newItem)
        createButton.place(relx=.5, rely = .775, anchor='center')
        
        returnButton = tk.Button(newItemWindow, text = 'Home', command = lambda: [newItemWindow.destroy(), mainMenu()])
        returnButton.place(relx=.85, rely=.85, anchor='center')
        
        barcodeGeneratorButton = tk.Button(newItemWindow, text = "Generate Barcode", command = lambda:[generateBarcode(barcodeEntry, checkDigitLabel)])
        barcodeGeneratorButton.place(relx=.5, rely=.92, anchor='center')
        barcodeEntry = tk.Entry(newItemWindow, font=('calibre', 12))
        barcodeEntry.place(relx=.5, rely=.85, anchor = 'center')
        checkDigitLabel = tk.Label(newItemWindow, text = '', font=('calibre', 12))
        checkDigitLabel.place(relx=.7, rely=.85, anchor = 'center')
        
        newItemWindow.mainloop()
        return
    
    def dataCheck():
        cur = DG.conn.cursor()
        sql = '''SELECT * FROM ''' + DG.invDatabase + '''
                 WHERE ManufacturerID = %s'''
        cur.execute(sql, [item_to_add_manID.get().lower()])
        records = cur.fetchall()
        if records:
            addItemWindow.destroy()
            adjustItemGUI(item_to_add_manID.get().lower())
        else:
            addItemWindow.destroy()
            newItemGUI()
            return
        return
    
    global item_to_add_manID
    item_to_add_manID = tk.StringVar()
    
    addItemManufacturerLabel = tk.Label(addItemWindow, text = 'Manufacturer ID:', font=('calibre', 12, 'bold'))
    addItemManufacturerEntry = tk.Entry(addItemWindow, textvariable = item_to_add_manID, font=('calibre', 12))
    addItemManufacturerButton = tk.Button(addItemWindow, text = 'Add Item', command = dataCheck)
    returnButton = tk.Button(addItemWindow, text = 'Home', command = lambda: [addItemWindow.destroy(), mainMenu()])
    addItemManufacturerEntry.bind('<Return>', lambda e: dataCheck())
    addItemManufacturerEntry.focus_force()

    addItemManufacturerLabel.place(relx=.116, rely=.4, anchor='center')
    addItemManufacturerEntry.place(relx=.4, rely=.4, anchor='center')
    addItemManufacturerButton.place(relx=.7, rely=.4, anchor='center')
    returnButton.place(relx=.85, rely=.85, anchor = 'center')
    
    addItemWindow.mainloop() 
    return    

def adjustItemGUI(item_for_adjustment):
    cur = DG.conn.cursor()
    sql = '''SELECT Barcode FROM ''' + DG.invDatabase + '''
            WHERE ManufacturerID = %s'''
    cur.execute(sql, [item_for_adjustment])
    records = cur.fetchall()
    barcode_for_adjustment = records[0][0]
    invRecords, locRecords = DG.searchID(item_for_adjustment)
    
    adjustItemWindow = tk.Tk()
    adjustItemWindow.geometry("600x400")
    adjustItemWindow.title('Adjust Item')
    
    def adjustItem():
        adjustedManID = manIDEntry.get().lower()
        adjustedManName = manNameEntry.get().lower()
        adjustedSupplierPartNum = SupplierPartNumEntry.get()
        adjustedSupplierName = supplierNameEntry.get()
        #adjustedName = NameEntry.get()
        adjustedDescription = DescriptionEntry.get('1.0', tk.END).strip()
        
        if(QuantityEntry.get() == ""):
            adjustedQuantity = None
        else:
            adjustedQuantity = QuantityEntry.get()
            
        adjustedBarcode = BarcodeEntry.get()
        if(len(adjustedBarcode) != 12):
            tk.messagebox.showerror("Error", "Barcodes must be 12 characters long")
            return
        
        # Removing BOM entry from adjust and add items
        
# =============================================================================
#         if(bomIDEntry.get() == ""):
#             adjustedbomID = None
#         else:
#             adjustedbomID = bomIDEntry.get()
# =============================================================================
            
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
            
        # Check if Barcode is already in system
        # does extraneous checks on Inventory, Locations and Barcodes. Adding items doesn't have to be blazing fast
        #
        # This is directly copied from the newItem function, may be edge cases where this is too strict
        # I'm just going to wait until someone complains or I notice an issue before adjusting it though
        #
        sql = '''SELECT * FROM ''' + DG.barDatabase + ''' WHERE code = %s'''
        cur.execute(sql, [adjustedBarcode])
        barRecords = cur.fetchall()
        sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE Barcode = %s'''
        cur.execute(sql, [adjustedBarcode])
        invBarRecords = cur.fetchall()
        sql = '''SELECT * FROM ''' + DG.locDatabase + ''' WHERE Barcode = %s'''
        cur.execute(sql, [adjustedBarcode]) 
        locBarRecords = cur.fetchall()
        if(barRecords and barRecords[0][0] != invRecords[0][6]):
            if(locBarRecords or invBarRecords):
                tk.messagebox.showerror('Error', 'Barcode has already been found in our system')
                return
        
        # Check if Manufacturer ID is already in system
        sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE ManufacturerID = %s'''
        cur.execute(sql, [adjustedManID])
        manIDRecords = cur.fetchall()
        
        # Check for records of Manufacturer ID with discrepancy of reusing the same ID
        if(manIDRecords and manIDRecords[0][0] != invRecords[0][0]):
            tk.messagebox.showerror('Error', 'Manufacturer ID has already been found in our system')
            return
        
        sql = '''UPDATE ''' + DG.invDatabase + '''
                 SET ManufacturerID = %s,
                     Manufacturer = %s,
                     SupplierPartNum = %s, 
                     Supplier = %s, 
                     Description = %s, 
                     Quantity = %s, 
                     Barcode = %s
                 WHERE Barcode = %s;
                 END'''
        cur.execute(sql, [adjustedManID, adjustedManName, adjustedSupplierPartNum, adjustedSupplierName, adjustedDescription, adjustedQuantity, adjustedBarcode, barcode_for_adjustment])
        
        sql = '''UPDATE ''' + DG.locDatabase + '''
                 SET Room = %s,
                     Rack = %s,
                     Shelf = %s,
                     Shelf_Location = %s,
                     Barcode = %s
                 WHERE Barcode = %s;
                 END'''
        cur.execute(sql, [adjustedroom, adjustedrack, adjustedshelf, adjustedshelfLocation, adjustedBarcode, barcode_for_adjustment])
        
        sql = '''SELECT * FROM ''' + DG.barDatabase + ''' WHERE code = %s'''
        cur.execute(sql, [barcode_for_adjustment])
        records = cur.fetchall()
        if(records):
            sql='''UPDATE ''' + DG.barDatabase + '''
                    SET code = %s
                    WHERE code = %s;
                    END'''
            cur.execute(sql, [adjustedBarcode, barcode_for_adjustment])
        else:
            sql = '''INSERT INTO ''' + DG.barDatabase + ''' (code) VALUES (%s)'''
            cur.execute(sql, [adjustedBarcode])
        
        
        # Careful here, there's no check for this, it just shows up if nothing crashed the program thus far.
        # Maybe establish a try/catch for the above three SQL statements? If no failures, display the box
        tk.messagebox.showinfo("Success", 'Item Updated')
        adjustItemWindow.destroy()
        mainMenu()
    
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
    manName = tk.StringVar()
    supplierPartNum = tk.StringVar()
    supplierName = tk.StringVar()
    #Name = tk.StringVar()
    Quantity = tk.StringVar()
    Barcode = tk.StringVar()
    #bomID = tk.StringVar()
    room = tk.StringVar()
    rack = tk.StringVar()
    shelf = tk.StringVar()
    shelfLocation = tk.StringVar()
    
    manIDLabel = tk.Label(adjustItemWindow, text = 'Manufacturer Part #: ', font=('calibre', 12))
    manNameLabel = tk.Label(adjustItemWindow, text = 'Manufacturer: ', font=('calibre', 12))
    SupplierPartNumLabel = tk.Label(adjustItemWindow, text = 'Supplier Part Number: ', font=('calibre', 12))
    supplierNameLabel = tk.Label(adjustItemWindow, text = 'Supplier: ', font=('calibre', 12))
    #NameLabel = tk.Label(adjustItemWindow, text = 'Name: ', font=('calibre', 12))
    DescriptionLabel = tk.Label(adjustItemWindow, text = 'Description: ', font=('calibre', 12))
    QuantityLabel = tk.Label(adjustItemWindow, text = 'Quantity: ', font=('calibre', 12))
    BarcodeLabel = tk.Label(adjustItemWindow, text = 'Barcode: ', font=('calibre', 12))
    #bomIDLabel = tk.Label(adjustItemWindow, text = 'BOM ID: ', font=('calibre', 12))
    roomLabel = tk.Label(adjustItemWindow, text = 'Room: ', font=('calibre', 12))
    rackLabel = tk.Label(adjustItemWindow, text = 'Rack: ', font=('calibre', 12))
    shelfLabel = tk.Label(adjustItemWindow, text = 'Shelf: ', font=('calibre', 12))
    shelfLocationLabel = tk.Label(adjustItemWindow, text = 'Shelf Location: ', font=('calibre', 12))
    
    manIDEntry = tk.Entry(adjustItemWindow, textvariable = manID, font=('calibre', 12))
    manNameEntry = tk.Entry(adjustItemWindow, textvariable = manName, font=('calibre', 12))
    SupplierPartNumEntry = tk.Entry(adjustItemWindow, textvariable = supplierPartNum, font=('calibre', 12))
    supplierNameEntry = tk.Entry(adjustItemWindow, textvariable = supplierName, font=('calibre', 12))
    #NameEntry = tk.Entry(adjustItemWindow, textvariable = Name, font=('calibre', 12))
    DescriptionEntry = tk.Text(adjustItemWindow, font = ('calibre', 12), width = 20, height = 3)
    QuantityEntry = tk.Entry(adjustItemWindow, textvariable = Quantity, font=('calibre', 12))
    BarcodeEntry = tk.Entry(adjustItemWindow, textvariable = Barcode, font=('calibre', 12))
    #bomIDEntry = tk.Entry(adjustItemWindow, textvariable = bomID, font=('calibre', 12))
    roomEntry = tk.Entry(adjustItemWindow, textvariable = room, font=('calibre', 12))
    rackEntry = tk.Entry(adjustItemWindow, textvariable = rack, font=('calibre', 12))
    shelfEntry = tk.Entry(adjustItemWindow, textvariable = shelf, font=('calibre', 12))
    shelfLocationEntry = tk.Entry(adjustItemWindow, textvariable = shelfLocation, font=('calibre', 12))

    if(invRecords[0][0]):
        manIDEntry.insert(0, invRecords[0][0])
    if(invRecords[0][1]):
        manNameEntry.insert(0, invRecords[0][1])
    if(invRecords[0][2]):
        SupplierPartNumEntry.insert(0, invRecords[0][2])
    if(invRecords[0][3]):
        supplierNameEntry.insert(0, invRecords[0][3])
# =============================================================================
#     if(invRecords[0][4]):
#         NameEntry.insert(0,invRecords[0][4])
# =============================================================================
    if(invRecords[0][4]):
        DescriptionEntry.insert('end', invRecords[0][4])
    if(invRecords[0][5]):
        QuantityEntry.insert(0, invRecords[0][5])
    if(invRecords[0][6]):
        BarcodeEntry.insert(0, invRecords[0][6])
# =============================================================================
#     if(invRecords[0][6] != None):
#         bomIDEntry.insert(0, invRecords[0][6])
# =============================================================================
    if(locRecords[0][0]):
        roomEntry.insert(0, locRecords[0][0])
    if(locRecords[0][1]):
        rackEntry.insert(0, locRecords[0][1])
    if(locRecords[0][2]):
        shelfEntry.insert(0, locRecords[0][2])
    if(locRecords[0][3]):
        shelfLocationEntry.insert(0, locRecords[0][3])

    manIDLabel.place(relx=.05, rely=.1, anchor='w')
    manIDEntry.place(relx=.55, rely=.1, anchor='center')
    
    manNameLabel.place(relx=.05, rely=.15, anchor='w')
    manNameEntry.place(relx=.55, rely=.15, anchor='center')
    
    SupplierPartNumLabel.place(relx=.05, rely=.2, anchor='w')
    SupplierPartNumEntry.place(relx=.55, rely=.2, anchor='center')
    
    supplierNameLabel.place(relx=.05, rely=.25, anchor='w')
    supplierNameEntry.place(relx=.55, rely=.25, anchor='center')
    
# =============================================================================
#     NameLabel.place(relx=.05, rely=.2, anchor='w')
#     NameEntry.place(relx=.55, rely=.2, anchor='center')
# =============================================================================
    
    DescriptionLabel.place(relx=.05, rely=.325, anchor='w')
    DescriptionEntry.place(relx=.55, rely=.35, anchor='center')
    
    QuantityLabel.place(relx=.05, rely=.45, anchor='w')
    QuantityEntry.place(relx=.55, rely=.45, anchor='center')
    
    BarcodeLabel.place(relx=.05, rely=.5, anchor='w')
    BarcodeEntry.place(relx=.55, rely=.5, anchor='center')
    
# =============================================================================
#     bomIDLabel.place(relx=.05, rely=.5, anchor='w')
#     bomIDEntry.place(relx=.55, rely=.5, anchor='center')
# =============================================================================
    
    roomLabel.place(relx=.05, rely=.55, anchor='w')
    roomEntry.place(relx=.55, rely=.55, anchor='center')
    
    rackLabel.place(relx=.05, rely=.6, anchor='w')
    rackEntry.place(relx=.55, rely=.6, anchor='center')
    
    shelfLabel.place(relx=.05, rely=.65, anchor='w')
    shelfEntry.place(relx=.55, rely=.65, anchor='center')
    
    shelfLocationLabel.place(relx=.05, rely=.7, anchor='w')
    shelfLocationEntry.place(relx=.55, rely=.7, anchor='center')
    
    adjustButton = tk.Button(adjustItemWindow, text = 'Adjust', command = adjustItem)
    adjustButton.place(relx=.5, rely = .85, anchor='center')
    
    returnButton = tk.Button(adjustItemWindow, text = 'Home', command = lambda: [adjustItemWindow.destroy(), mainMenu()])
    returnButton.place(relx=.85, rely=.9, anchor='center')

    adjustItemWindow.mainloop()
    return

def removeItem():
    mainMenuWindow.destroy()
    removeItemWindow = tk.Tk()
    removeItemWindow.geometry("600x150")
    removeItemWindow.title("Remove Item")
    removeVar = tk.StringVar()
    
    def itemRemoval(item_to_remove):
        cur = DG.conn.cursor()
        sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE ManufacturerID = %s'''
        cur.execute(sql, [item_to_remove])
        records = cur.fetchall()
        if(records):
            sql = '''DELETE FROM ''' + DG.invDatabase + ''' WHERE ManufacturerID = %s'''
            cur.execute(sql, [item_to_remove])
            sql = '''DELETE FROM ''' + DG.locDatabase + ''' WHERE Barcode = %s'''
            cur.execute(sql, [records[0][6]])
            sql = '''DELETE FROM ''' + DG.barDatabase + ''' WHERE code = %s'''
            cur.execute(sql, [records[0][6]])
            
            message = "Item:", item_to_remove, 'deleted'
            tk.messagebox.showinfo("Success", message)
            removeItemEntry.delete(0, tk.END)
        else:
            tk.messagebox.showerror('Error', 'Item not found in inventory')
                
    def removeCheck():
        #Double check that item should actually be removed
        removeCheckWindow = tk.Tk()
        removeCheckWindow.geometry("400x200")
        removeCheckWindow.title("Are you sure?")
        removeCheckWindow.focus_force()
        
        removeText = "Are you sure you want to remove item: " + removeVar.get().lower()
        removeLabel = tk.Label(removeCheckWindow, text = removeText, font = ('calibre', 12))
        yesButton = tk.Button(removeCheckWindow, text = "Yes", command = lambda: [itemRemoval(removeVar.get().lower()), removeCheckWindow.destroy()])
        noButton = tk.Button(removeCheckWindow, text = "No", command = removeCheckWindow.destroy)
        removeItemEntry.unbind('<Return>')
        removeCheckWindow.bind('<Return>', lambda event:[itemRemoval(removeVar.get()), removeCheckWindow.destroy(), removeItemEntry.bind('<Return>', lambda e: removeCheck())])
        
        removeLabel.place(relx=.5, rely=.3, anchor='center')
        yesButton.place(relx=.2, rely=.6, anchor = 'center')
        noButton.place(relx=.8, rely=.6, anchor='center')   
        
        removeCheckWindow.mainloop()
        return
    
    removeItemLabel = tk.Label(removeItemWindow, text = "Manufacturer ID:", font=('calibre', 12))
    removeItemEntry = tk.Entry(removeItemWindow, textvariable = removeVar, font=('calibre', 12))
    
    removeItemButton = tk.Button(removeItemWindow, text = 'Remove', command = removeCheck)
    removeItemEntry.bind('<Return>', lambda e: removeCheck())
    
    homeButton = tk.Button(removeItemWindow, text = 'Home', command = lambda: [removeItemWindow.destroy(), mainMenu()])
    
    removeItemLabel.place(relx=.15, rely=.4, anchor='center')
    removeItemEntry.place(relx=.4, rely=.4, anchor='center')
    removeItemButton.place(relx=.7, rely=.4, anchor='center')
    homeButton.place(relx=.85, rely=.85, anchor='center')
    
    removeItemEntry.focus_force()
    removeItemWindow.mainloop()
    
    return

def createBOMGUI():
    bomWindow = tk.Tk()
    bomWindow.geometry("600x200")
    bomWindow.title("Bill of Materials")
    cur = DG.conn.cursor()
    
    def createBOMID():
        bomID = random.randrange(0, 10000)
        sql = '''SELECT * FROM ''' + DG.bomDatabase + ''' WHERE bom_id = %s'''
        cur.execute(sql, [bomID])
        records = cur.fetchall()
        if(records):
            createBOMID()
        else:
            return(bomID)
    
    def createBom():
        if(not itemName.get()):
            tk.messagebox.showerror("Error", 'Please select an item')
            return
        bomWindow.destroy()
        createBomWindow = tk.Tk()
        createBomWindow.title("Create BOM")
        createBomWindow.geometry("600x400")
        

        def addBomItem():
            inv, loc = DG.searchID(manIDEntry.get().lower())
            sql = '''SELECT manufacturerid FROM ''' + DG.invDatabase + ''' WHERE bom_id = %s'''
            cur.execute(sql, [bomID])
            selfID = cur.fetchall()
            if(selfID):
                selfID = selfID[0][0]
            try:
                quant = int(quantityEntry.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Quantity must be an integer value")
                quantityEntry.delete(0, tk.END)
                quantityEntry.focus_force()
                return
            if(not inv):
                tk.messagebox.showerror("Error", "Manufacturer ID not found")
            elif(quant < 1):
                tk.messagebox.showerror("Error", "Please enter a quantity greater than zero")
            elif(manIDEntry.get().lower() == selfID):
                tk.messagebox.showerror("Error", "Cannot add item to it's own BOM")
            else:
                bomTree.insert("", 'end', values=(manIDEntry.get().lower(), quant))
            manIDEntry.delete(0, tk.END)
            quantityEntry.delete(0, tk.END)
            manIDEntry.focus_force()
            return
        
        def remBomItem():
            selected = bomTree.selection()[0]
            bomTree.delete(selected)
            return
        
        def finalize():
            # CREATING BOM TABLE
            tableName = "bom_" + str(bomID)
            sql = '''CREATE TABLE IF NOT EXISTS ''' + tableName + '''(
                        ManufacturerID VARCHAR(100),
                        QuantityNeeded SMALLINT
                    );'''
            cur.execute(sql)
            
            if(edit):
                sql = '''DELETE FROM ''' + tableName + ''';'''
                cur.execute(sql)
            else:
                # INSERTING BOM_ID# and BOM_NAME INTO BOM TABLE OF TABLES
                sql = '''INSERT INTO ''' + DG.bomDatabase + ''' (bom_id, bom_name) VALUES (%s, %s);'''
                cur.execute(sql, [bomID, itemName.get()])
                sql = '''UPDATE ''' + DG.invDatabase + ''' SET bom_id = %s WHERE name = %s'''
                cur.execute(sql, [bomID, itemName.get()])
            # INSERTING ALL MANUFACTURER IDS AND QUANTITIES
            for line in bomTree.get_children():
                sql = '''INSERT INTO ''' + tableName + '''(ManufacturerID, QuantityNeeded) VALUES (%s, %s);'''
                cur.execute(sql, [bomTree.item(line).get('values')[0], bomTree.item(line).get('values')[1]])
                
            
            
            # Show success box before transfer back
            tk.messagebox.showinfo("Success", 'Bill of Materials saved')
            createBomWindow.destroy()
            mainMenu()
            
                
            return
        
        
        manIDLabel = tk.Label(createBomWindow, text = "Manufacturer ID:", font=('calibre', 12))
        manIDEntry = tk.Entry(createBomWindow, width = 30)
        quantityLabel = tk.Label(createBomWindow, text = "Quantity:", font=('calibre', 12))
        quantityEntry = tk.Entry(createBomWindow, width = 5)
        bomTree = ttk.Treeview(createBomWindow, selectmode = 'browse')
        completeBomButton = tk.Button(createBomWindow, text = "Finalize", command = finalize)
        addItemButton = tk.Button(createBomWindow, text = "Add Item", command = lambda:[addBomItem()])
        removeItemButton = tk.Button(createBomWindow, text = "Remove Item", command = lambda:[remBomItem()])
        bomScrollbar = tk.Scrollbar(createBomWindow, orient='vertical', command = bomTree.yview)
        returnButton = tk.Button(createBomWindow, text = 'Return', command = lambda:[createBomWindow.destroy(), createBOMGUI()])
        
        manIDEntry.focus()
        manIDEntry.bind('<Return>', lambda e: addBomItem())
        quantityEntry.bind('<Return>', lambda e: addBomItem())
        
        manIDLabel.place(relx=.15, rely=.1, anchor='center')
        manIDEntry.place(relx=.4, rely=.1, anchor = 'center')
        quantityLabel.place(relx=.56, rely=.1, anchor='center')
        quantityEntry.place(relx=.66, rely=.1, anchor = 'center')
        addItemButton.place(relx=.8, rely=.1, anchor = 'center')
        removeItemButton.place(relx=.35, rely=.8, anchor = 'center')
        bomTree.place(relx=.5, rely=.45, anchor = 'center')
        bomScrollbar.place(relx=.65, rely=.45, anchor = 'center')
        completeBomButton.place(relx=.65, rely=.8, anchor = 'center')
        returnButton.place(relx = .5, rely=.9, anchor='center')
        
        bomTree.configure(yscrollcommand = bomScrollbar.set)
        bomTree["columns"] = ("1", "2")
        bomTree['show'] = 'headings' 
        bomTree.column("1", width = 100, anchor = 'w')
        bomTree.column("2", width = 100, anchor = 'w')
        bomTree.heading("1", text = "Manufacturer ID")
        bomTree.heading("2", text = "Quantity")
            
            
        # USE FOR EDITING BOM
        # FILLS TREE WITH INFORMATION ALREADY IN DATABASE
            
        sql = '''SELECT * FROM ''' + DG.bomDatabase + ''' WHERE bom_name = %s'''
        cur.execute(sql, [itemName.get()])
        records = cur.fetchall()
        edit = 0
        if(records):
            edit = 1
            bomID = records[0][0]
            tableName = "bom_" + str(bomID)
            sql = '''SELECT * FROM ''' + tableName + ''';'''
            cur.execute(sql)
            records = cur.fetchall()
            if(records):
                for record in records:
                    bomTree.insert("", 'end', values=(record[0], record[1]))
        else:
            bomID = createBOMID()

        createBomWindow.mainloop()
        return
    
    # useList and nonUseList are what is and isn't used in the inventory to make a particular bom
    def checkInventoryHelper():
        useList, nonUseList = set([]), set([])
        bomString = bomEntryBox.get()
        bomList = [i.strip() for i in bomString.split(",")]
        for bom in bomList:
            sql = '''SELECT bom_id FROM ''' + DG.bomDatabase + ''' WHERE bom_name = %s;'''
            cur.execute(sql, [bom])
            records = cur.fetchall()
            if(records):
                bomIDNum = records[0][0]
                checkInventory(bomIDNum, useList, nonUseList)
                sql = '''SELECT * FROM ''' + DG.invDatabase + ''';'''
                cur.execute(sql)
                records = cur.fetchall()

            else:
                tk.messagebox.showerror("Error", 'No BOM on record to check inventory')
        for record in records:
            if(record[0] not in useList):
                nonUseList.add(record[0])
# =============================================================================
#         nonUseList = set(nonUseList)
#         useList = set(useList)
# =============================================================================
        print("Items Used: ", useList)
        print("Items Unused: ", nonUseList)
        return
    
    def checkInventory(bom, useList, nonUseList):
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
                    sql = '''SELECT bom_id from ''' + DG.invDatabase + ''' WHERE ManufacturerID = %s'''
                    cur.execute(sql, [record[0]])
                    bomRecords = cur.fetchall()
                    
                    # Check to see if item has it's own BOM, if so recursively call checkInventory()
                    if(bomRecords[0][0] != None):
                        print(bomRecords[0][0])
                        useList.add(record[0])
                        checkInventory(bomRecords[0][0], useList, nonUseList)

                    else:
                        sql = '''SELECT Quantity from ''' + DG.invDatabase + '''
                                WHERE ManufacturerID = %s;'''
                        cur.execute(sql, [record[0]])
                        quantity = cur.fetchall()
                        print("Manufacurer ID: ", record[0], "\nQuantity: ", quantity[0][0])
                        
                        sql = '''SELECT QuantityNeeded from BOM_%s WHERE ManufacturerID = %s'''
                        cur.execute(sql, [bom, record[0]])
                        bomQuantity = cur.fetchall()
                        print("Required: ", bomQuantity[0][0])
                        useList.add(record[0])
                    
        else:
            errorMessage = 'No BOM found for BOM #' + str(bom) 
            tk.messagebox.showerror('Error', errorMessage)
        
        
    nameLabel = tk.Label(bomWindow, text = "Select item to create/edit BOM")
    orLabel = tk.Label(bomWindow, text = "or", font = ('calibre', 12))
    bomEntryLabel = tk.Label(bomWindow, text = "Type manufacturer IDs for \nBOM inventory check")
    nameList = []
    itemName = tk.StringVar()
    sql = '''SELECT name FROM ''' + DG.invDatabase + ''' ORDER BY name'''
    cur.execute(sql)
    records = cur.fetchall()
    for record in records:
        nameList.append(record[0])
    bomChoiceBox = ttk.Combobox(state='readonly', values = nameList, textvariable = itemName)
    bomEntryBox = tk.Entry(bomWindow, width = 25)
    createBomButton = tk.Button(bomWindow, text = "Create", command=createBom)
    checkInventoryButton = tk.Button(bomWindow, text="Check Inventory", command=checkInventoryHelper)
    returnButton = tk.Button(bomWindow, text = 'Home', command = lambda:[bomWindow.destroy(), mainMenu()])
    
    nameLabel.place(relx=.3, rely=.15, anchor = 'center')
    orLabel.place(relx=.5, rely=.25, anchor='center')
    bomEntryLabel.place(relx=.7, rely=.15, anchor='center')
    bomEntryBox.place(relx=.7, rely=.3, anchor='center')
    bomChoiceBox.place(relx=.3, rely=.3, anchor='center')
    createBomButton.place(relx=.3, rely=.6, anchor = 'center')
    checkInventoryButton.place(relx=.7, rely=.6, anchor='center')
    returnButton.place(relx=.85, rely=.85, anchor='center')
    
    bomWindow.mainloop()
    
    return

def userMenu():
    userWindow = tk.Tk()
    userWindow.geometry("300x200")
    userWindow.title("Users")
    username = tk.StringVar()
    
    def createUser():
        createUserWindow = tk.Tk()
        createUserWindow.geometry("500x200")
        createUserWindow.title("Create User")
        cur = DG.conn.cursor()            

        def finalizeUserCreation():
            if(nameEntry.get() == ""):
                tk.messagebox.showerror("Error", "Please enter a username")
                createUserWindow.destroy()
                return
            sql = '''SELECT * FROM ''' + DG.userDatabase + ''' WHERE username = %s UNION 
                    SELECT * FROM ''' + DG.userDatabase + ''' WHERE usercode = %s;'''
            cur.execute(sql, [nameEntry.get().lower(), code])
            records = cur.fetchall()
            if(records):
                for record in records:
                    print("Barcode: ", record[0], "Username: ",  record[1])
                tk.messagebox.showerror("Duplicate User", "Please enter a unique Username")
            else:
                sql = '''INSERT INTO ''' + DG.userDatabase + ''' (username, usercode) VALUES (%s, %s);'''
                cur.execute(sql, [nameEntry.get().lower(), code])
                createUserWindow.destroy()
                tk.messagebox.showinfo('Success', 'User Created')
            return

        
        nameLabel = tk.Label(createUserWindow, text = "User Name:", font = ('calibre', 12))
        nameEntry = tk.Entry(createUserWindow, textvariable = username, font = ('calibre', 12))
        createButton = tk.Button(createUserWindow, text = "Create", command = lambda:[finalizeUserCreation()])
        nameEntry.bind('<Return>',  lambda e: finalizeUserCreation())
        
        barcodeEntry = tk.Entry(createUserWindow, font=('calibre', 12))
        checkDigitLabel = tk.Label(createUserWindow, text = '', font=('calibre', 12))
        barcodeLabel = tk.Label(createUserWindow, text = 'Barcode', font = ('calibre', 12))
        backButton = tk.Button(createUserWindow, text = 'Back', command = createUserWindow.destroy)
        
        
        nameLabel.place(relx= .2, rely= .4, anchor = 'center')
        nameEntry.place(relx= .5, rely= .4, anchor = 'center')
        
        barcodeLabel.place(relx=.2, rely=.6, anchor='center')
        barcodeEntry.place(relx= .5, rely= .6, anchor = 'center')
        checkDigitLabel.place(relx= .7, rely= .6, anchor = 'center')
        
        createButton.place(relx= .75, rely= .8, anchor = 'center')
        backButton.place(relx = .25, rely = .8, anchor = 'center')
        code = generateBarcode(barcodeEntry, checkDigitLabel)
        
        createUserWindow.mainloop()
        
    
    createUserButton = tk.Button(userWindow, text = "Create User", command = createUser)
    homeButton = tk.Button(userWindow, text = 'Home', command = lambda:[userWindow.destroy(), mainMenu()])
    
    createUserButton.place(relx=.5, rely=.5, anchor = 'center')
    homeButton.place(relx=.85, rely=.85, anchor = 'center')
      
    userWindow.mainloop()
    return










def checkOut():
    checkOutWindow = tk.Tk()
    checkOutWindow.title("Check Out")
    checkOutWindow.geometry("800x400")
    cur = DG.conn.cursor()
    
    def quantityCheck(bar, quantity):
        sql = '''SELECT quantity FROM ''' + DG.invDatabase + ''' WHERE barcode = %s'''
        cur.execute(sql, [bar])
        records = cur.fetchall()
        for record in records:
            if(int(quantity) > record[0]):
                return False
            else:
                return True
        return
      
    def addItem():
        sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE barcode = %s;'''
        cur.execute(sql, [barEntry.get()])
        records = cur.fetchall()
        
        # Check if records of inventory item with entered barcode exists
        if(not records):
            tk.messagebox.showerror("Error", "Item not currently in system")
            return
        
        # Check previously added items for duplicates
        for line in checkOutTree.get_children():
            #print("Tree:", checkOutTree.item(line).get('values')[2], type(checkOutTree.item(line).get('values')[2]), "Barcode:", barEntry.get(), type(barEntry.get()))
            if(str(checkOutTree.item(line).get('values')[2]) == barEntry.get()):
                errorMessage = 'Item: "' + str(checkOutTree.item(line).get('values')[1]) + '" already in list'
                tk.messagebox.showerror("Error", errorMessage)
                barEntry.delete(0,tk.END)
                barEntry.focus_force()
                return
            
        # If user didn't enter a quantity, just assign quantity of 1
        if(itemQuantityEntry.get() == ""):
            quantity = 1
        else:
            quantity = itemQuantityEntry.get()
        
        # Check to make sure that quantity is available in database
        if(not quantityCheck(barEntry.get(), quantity)):
# =============================================================================
#             errorMessage = 'Quantity of Item: "' + str(checkOutTree.item(line).get('values')[1]) + '" not available in database'
# =============================================================================
            errorMessage = 'Less than ' + quantity + ' "' + records[0][4] + '" available in database'
            tk.messagebox.showerror("Error", errorMessage)
            itemQuantityEntry.delete(0, tk.END)
            itemQuantityEntry.focus_force()
            return
            
        # Insertion of values into Treeview tree
        checkOutTree.insert("", 'end', values=(records[0][0], records[0][4], barEntry.get(), quantity))     #manID, name, barcode, quantity))
        barEntry.delete(0, tk.END)
        itemQuantityEntry.delete(0, tk.END)
        barEntry.focus_force()
        return
    
    def removeItem():
        selected = checkOutTree.selection()[0]
        checkOutTree.delete(selected)
        return
    
    def editItem():
        
        selected = checkOutTree.item(checkOutTree.focus())
        if(selected['values'] == ''):
            tk.messagebox.showerror('Error', 'Please select an item to edit')
            return
        editItemWindow = tk.Tk()
        editItemWindow.title("Edit Item")
        editItemWindow.geometry("400x200")
        
        def finalizeEdit():
            if(quantityCheck(str(selected['values'][2]), quantityEntry.get())):
                checkOutTree.set(checkOutTree.focus(), column = '4', value = quantityEntry.get())
            else:
                errorMessage = 'Less than ' + quantityEntry.get() + ' "' + selected['values'][1] + '" available in database'
                tk.messagebox.showerror("Error", errorMessage)
            return
        
        returnButton = tk.Button(editItemWindow, text = 'Return', command = editItemWindow.destroy)
        finalizeButton = tk.Button(editItemWindow, text = 'Finalize', command = lambda:[finalizeEdit(), editItemWindow.destroy()])
        manIDLabel = tk.Label(editItemWindow, text = 'Manufacturer ID:', font = ('calibre', 12))
        manIDLabel_fill = tk.Label(editItemWindow, text = '')
        nameLabel = tk.Label(editItemWindow, text = 'Description:', font = ('calibre', 12))
        nameLabel_fill = tk.Label(editItemWindow, text = '')
        barcodeLabel = tk.Label(editItemWindow, text = 'Barcode:', font = ('calibre', 12))
        barcodeLabel_fill = tk.Label(editItemWindow, text = '')
        quantityLabel = tk.Label(editItemWindow, text = 'Quantity', font = ('calibre', 12))
        quantityEntry = tk.Entry(editItemWindow, width = 5)
        
        manIDLabel.place(relx=.15, rely=.3, anchor='w')
        manIDLabel_fill.place(relx=.5, rely=.3, anchor='w')
        nameLabel.place(relx=.15, rely=.4, anchor='w')
        nameLabel_fill.place(relx=.5, rely=.4, anchor='w')
        barcodeLabel.place(relx=.15, rely=.5, anchor='w')
        barcodeLabel_fill.place(relx=.5, rely=.5, anchor='w')
        quantityLabel.place(relx=.15, rely=.6, anchor = 'w')
        quantityEntry.place(relx=.5, rely=.6, anchor = 'w')
        returnButton.place(relx=.85, rely=.85, anchor = 'center')
        finalizeButton.place(relx=.65, rely=.85, anchor='center')

        manIDLabel_fill.config(text = selected['values'][0])
        nameLabel_fill.config(text = selected['values'][1])
        barcodeLabel_fill.config(text = selected['values'][2])
        quantityEntry.delete(0,tk.END)
        quantityEntry.insert(0,selected['values'][3])
        
        editItemWindow.mainloop()
        return
    
    def completeOrderGUI():
        receiptScreen = tk.Tk() 
        receiptScreen.title("Check Out Finalization")
        receiptScreen.geometry("600x400")
        
        userBarLabel = tk.Label(receiptScreen, text = "User Barcode:", font = ('calibre', 12))
        userBarEntry = tk.Entry(receiptScreen, width = 20)
        #userBarEntry.bind('<Return>', lambda e: )
        
        userBarLabel.place(relx = .2, rely=.5, anchor='center')
        userBarEntry.place(relx=.5, rely=.5, anchor = 'center')
        
        for line in checkOutTree.get_children():
            print(checkOutTree.item(line).get('values')[0], checkOutTree.item(line).get('values')[1], checkOutTree.item(line).get('values')[2], checkOutTree.item(line).get('values')[3])
        
        receiptScreen.mainloop()
        return
    
    barEntryLabel = tk.Label(checkOutWindow, text = 'Barcode:', font = ('calibre', 12))
    quantityLabel = tk.Label(checkOutWindow, text = 'Quantity:', font = ('calibre', 12))
    barEntry = tk.Entry(checkOutWindow, width = 30)
    itemQuantityEntry = tk.Entry(checkOutWindow, width = 5)
    checkOutTree = ttk.Treeview(checkOutWindow, selectmode = 'browse')
    checkOutScrollbar = tk.Scrollbar(checkOutWindow, orient='vertical', command = checkOutTree.yview)
    addItemButton = tk.Button(checkOutWindow, text = 'Add Item', command = addItem)
    editItemButton = tk.Button(checkOutWindow, text = "Edit Item", command = editItem)
    removeItemButton = tk.Button(checkOutWindow, text = 'Remove Item', command = removeItem)
    completeOrderButton = tk.Button(checkOutWindow, text = 'Complete Order', command = completeOrderGUI)
    homeButton = tk.Button(checkOutWindow, text = "Home", command = lambda:[checkOutWindow.destroy(), mainMenu()])
    barEntry.focus_force()
    barEntry.bind('<Return>', lambda e: itemQuantityEntry.focus_force())
    itemQuantityEntry.bind('<Return>', lambda e: addItem())
    
    barEntryLabel.place(relx=.25, rely=.1, anchor = 'center')
    barEntry.place(relx=.42, rely=.1, anchor='center')
    quantityLabel.place(relx=.62, rely=.1, anchor='center')
    itemQuantityEntry.place(relx=.7, rely=.1, anchor = 'center')
    checkOutScrollbar.place(relx=.775, rely=.45, anchor = 'center')
    checkOutTree.place(relx=.5, rely=.45, anchor = 'center')
    addItemButton.place(relx=.8, rely=.1, anchor = 'center')
    editItemButton.place(relx=.9, rely=.3, anchor = 'center')
    removeItemButton.place(relx=.9, rely=.5, anchor = 'center')
    completeOrderButton.place(relx=.65, rely=.85, anchor='center')
    homeButton.place(relx=.85, rely=.85, anchor = 'center')
    
    checkOutTree.configure(yscrollcommand = checkOutScrollbar.set)
    checkOutTree["columns"] = ("1", "2", "3", "4")
    checkOutTree['show'] = 'headings' 
    checkOutTree.column("1", width = 100, anchor = 'w')
    checkOutTree.column("2", width = 200, anchor = 'w')
    checkOutTree.column("3", width = 100, anchor = 'w')
    checkOutTree.column("4", width = 60, anchor = 'w')
    checkOutTree.heading("1", text = "Manufacturer ID")
    checkOutTree.heading("2", text = "Description")
    checkOutTree.heading("3", text = "Barcode")
    checkOutTree.heading("4", text = "Quantity")
    
    checkOutWindow.mainloop()
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
    sql = '''SELECT * FROM ''' + DG.barDatabase + ''' WHERE code=%s'''
    cur.execute(sql, [sqlCheck])
    records = cur.fetchone()
    if records:
        generateBarcode(barcodeEntry, checkDigitLabel)
        return
    else:
        barcodeEntry.delete(0, tk.END)    
        barcodeEntry.insert(0, barcodeString)
        checkDigitLabel.configure(text=str(checkDigit))
    return sqlCheck

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
        searchGUI(field)
        
        #searchInventoryEntry.delete(0, tk.END)
        # May use later, currently just destroying the window so 'Home' Button from 'adjustItem' function doesn't add another main menu
        #field.delete(0, tk.END)
    

        
    searchInventoryLabel = tk.Label(mainMenuWindow, text='Search', font=('calibre', 12, 'bold'))
    searchInventoryEntry = tk.Entry(mainMenuWindow, textvariable = searchVar, font=('calibre', 12))  
    searchInventoryEntry.focus_force()
    searchInventoryEntry.bind('<Return>', lambda e: searchHelper(searchInventoryEntry))     
    searchErrorLabel = tk.Label(mainMenuWindow, text='', font=('calibre', 12), fg='red')
    searchButton = tk.Button(mainMenuWindow, text = "Search", command = lambda: [searchHelper(searchInventoryEntry)])
    addItemButton = tk.Button(mainMenuWindow, text = "Add Item", command = lambda: [mainMenuWindow.destroy(), addItemGUI()])
    removeItemButton = tk.Button(mainMenuWindow, text = "Delete Item", command = removeItem)
    createBomButton = tk.Button(mainMenuWindow, text = "BOMs", command = lambda: [mainMenuWindow.destroy(), createBOMGUI()])
    checkOutButton = tk.Button(mainMenuWindow, text = 'Check Out', command = lambda:[mainMenuWindow.destroy(), checkOut()])
    userButton = tk.Button(mainMenuWindow, text="Users", command = lambda: [mainMenuWindow.destroy(), userMenu()])
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
    userButton.place(relx=.5, rely=.5, anchor='center')
    
    # Row 6
    checkOutButton.place(relx=.5, rely=.6, anchor='center')
     
    # Row 7
    barcodeGeneratorButton.place(relx=.5, rely=.7, anchor='center')
    
    # Row 8
    barcodeEntry.place(relx=.5, rely=.8, anchor='center')
    checkDigitLabel.place(relx=.7, rely=.8, anchor='center')
    

    mainMenuWindow.mainloop()
    
def testingDatabase():
    manid = 'test5'
    cur = DG.conn.cursor()
    sql = '''SELECT * FROM ssg_inventory WHERE manufacturerid = %s;'''
    cur.execute(sql, [manid])
    records = cur.fetchall()
    for record in records:
        print(record[0], record[1], record[2], record[3], record[4], type(record[4]), record[5])
    return
    
def main():
    DG.main()
    testingDatabase()
    mainMenu()
    DG.close()

if __name__ == '__main__':
    main()