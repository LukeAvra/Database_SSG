# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 08:32:28 2023

@author: Luke
"""
import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.setrecursionlimit(5000)
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import ttk
from datetime import datetime
import Database_Globals as DG
import Print_Label as PL
import psqlBackupScript as BU
import random
import bcrypt

def addItemGUI():
    newItemWindow = tk.Tk()
    newItemWindow.geometry("600x500+700+250")
    newItemWindow.title('New Item')
    cur = DG.conn.cursor()        
        
    def dataCheck(event):
        manIDCheck = manIDEntry.get()
        cur = DG.conn.cursor()
        sql = '''SELECT * FROM ''' + DG.invDatabase + '''
                  WHERE ManufacturerID = %s'''
        cur.execute(sql, [manIDCheck])
        records = cur.fetchall()
        if records:
            newItemWindow.destroy()
            adjustItemGUI(manIDCheck)
        return
    
    def pullBarcode(BarcodeEntry):
        bar = barcodeEntry.get() + checkDigitLabel.cget("text")
        BarcodeEntry.delete(0, tk.END)
        BarcodeEntry.insert(0, bar)
        #print(bar)
        return
    
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
        
        if(room.get() == ""):
            newRoom = None
        else:
            newRoom = room.get()
        
        if(rackEntry.get() == ""):
            newRack = None
        else:
            newRack = ord(rackEntry.get().upper())
        
        if(shelfEntry.get() == ""):
            newShelf = None
        else:
            newShelf = shelfEntry.get()
        
        if(shelfLocationEntry.get() == ""):
            newShelfLocation = None
        else:
            newShelfLocation = shelfLocationEntry.get()
            
        # Uncomment this when ready to use the Brother printer for all labels
        labelText = newManID.lower()
        if(roomChoiceBox.get() != ''):
            labelText = labelText + ' ' + roomChoiceBox.get()
        if(rackEntry.get() != ''):
                labelText = labelText + ' ' + rackEntry.get().upper()
        if(shelfEntry.get() != ''):
                labelText = labelText + '-' + shelfEntry.get()
        PL.createBarcodeImage(labelText, newBarcode)
        PL.printBarcode()
            
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
            tk.messagebox.showerror('Error', 'Manufacturer Number has already been found in our system')
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

    # variables for adding items
    manID = tk.StringVar()
    manName = tk.StringVar()
    SupplierPartNum = tk.StringVar()
    supplierName = tk.StringVar()
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
    DescriptionEntry = tk.Text(newItemWindow, font = ('calibre', 12), width = 20, height = 3)
    QuantityEntry = tk.Entry(newItemWindow, textvariable = Quantity, font=('calibre', 12))
    BarcodeEntry = tk.Entry(newItemWindow, textvariable = Barcode, font=('calibre', 12))
    
    choiceList = ['Inventory', 'Mezannine', 'Pallet Rack']
    
    roomChoiceBox = ttk.Combobox(
                        newItemWindow,
                        state='readonly',
                        values = choiceList,
                        textvariable=room
                        )
    roomChoiceBox.set('Inventory')
    
    rackEntry = tk.Entry(newItemWindow, textvariable = rack, font=('calibre', 12))
    shelfEntry = tk.Entry(newItemWindow, textvariable = shelf, font=('calibre', 12))
    shelfLocationEntry = tk.Entry(newItemWindow, textvariable = shelfLocation, font=('calibre', 12))
           
    manIDLabel.place(relx=.05, rely=.05, anchor='w')
    manIDEntry.place(relx=.6, rely=.05, anchor='center')
    
    manNameLabel.place(relx=.05, rely=.125, anchor='w')
    manNameEntry.place(relx=.6, rely=.125, anchor='center')
    
    SupplierPartNumLabel.place(relx=.05, rely=.2, anchor='w')
    SupplierPartNumEntry.place(relx=.6, rely=.2, anchor='center')
    
    SupplierNameLabel.place(relx=.05, rely=.275, anchor='w')
    SupplierNameEntry.place(relx=.6, rely=.275, anchor='center')
    
    DescriptionLabel.place(relx=.05, rely=.35, anchor='w')
    DescriptionEntry.place(relx=.6, rely=.375, anchor='center')
    
    QuantityLabel.place(relx=.05, rely=.475, anchor='w')
    QuantityEntry.place(relx=.6, rely=.475, anchor='center')
    
    BarcodeLabel.place(relx=.05, rely=.55, anchor='w')
    BarcodeEntry.place(relx=.6, rely=.55, anchor='center')
    
    roomLabel.place(relx=.05, rely=.625, anchor='w')
    roomChoiceBox.place(relx=.6, rely=.625, anchor='center')
    
    rackLabel.place(relx=.05, rely=.7, anchor='w')
    rackEntry.place(relx=.6, rely=.7, anchor='center')
    
    shelfLabel.place(relx=.05, rely=.775, anchor='w')
    shelfEntry.place(relx=.6, rely=.775, anchor='center')
    
    shelfLocationLabel.place(relx=.05, rely=.85, anchor='w')
    shelfLocationEntry.place(relx=.6, rely=.85, anchor='center')
    
    manIDEntry.focus_force()
    manIDEntry.bind("<FocusOut>", dataCheck)
    createButton = tk.Button(newItemWindow, text = 'Add Item', command = newItem)
    createButton.place(relx=.5, rely = .925, anchor='center')
    
    barcodeGeneratorButton = tk.Button(newItemWindow, text = "Generate Barcode", command = lambda:[generateBarcode(barcodeEntry, checkDigitLabel), pullBarcode(BarcodeEntry)])
    barcodeGeneratorButton.place(relx=.875, rely=.55, anchor='center')
    barcodeEntry = tk.Entry(newItemWindow, font=('calibre', 12))
    checkDigitLabel = tk.Label(newItemWindow, text = '', font=('calibre', 12))
    
    # Fill in the barcode entry automatically on window creation
    generateBarcode(barcodeEntry, checkDigitLabel)
    pullBarcode(BarcodeEntry)
    
    newItemWindow.mainloop()
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
    adjustItemWindow.geometry("600x400+700+250")
    adjustItemWindow.title('Adjust Item')
    adjustItemWindow.focus_force()
    
    def printCode():
        labelText = manIDEntry.get().lower()
        if(roomChoiceBox.get() != ''):
            labelText = labelText + ' ' + roomChoiceBox.get()
        if(rackEntry.get() != ''):
            labelText = labelText + ' ' + rackEntry.get().upper()
        if(shelfEntry.get() != ''):
            labelText = labelText + '-' + shelfEntry.get()
        PL.createBarcodeImage(labelText, BarcodeEntry.get())
        PL.printBarcode()
        return
    
    def adjustItem():
        adjustedManID = manIDEntry.get().lower()
        adjustedManName = manNameEntry.get().lower()
        adjustedSupplierPartNum = SupplierPartNumEntry.get()
        adjustedSupplierName = supplierNameEntry.get()
        adjustedDescription = DescriptionEntry.get('1.0', tk.END).strip()
        
        if(QuantityEntry.get() == ""):
            adjustedQuantity = None
        else:
            adjustedQuantity = QuantityEntry.get()
            
        adjustedBarcode = BarcodeEntry.get()
        if(len(adjustedBarcode) != 12):
            tk.messagebox.showerror("Error", "Barcodes must be 12 characters long")
            return
            
        adjustedroom = room.get()
        if(rackEntry.get() == ""):
            adjustedrack = None
        elif(len(rackEntry.get()) > 1):
            tk.messagebox.showerror("Error", "Please enter a single character rack identifier (A-Z)")
            return
        else:
            adjustedrack = ord(str(rackEntry.get()).upper())
            
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
            tk.messagebox.showerror('Error', 'Manufacturer Number has already been found in our system')
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
        tk.messagebox.showinfo("Success", 'Item Updated', parent=adjustItemWindow)
        adjustItemWindow.destroy()
        return

    manID = tk.StringVar()
    manName = tk.StringVar()
    supplierPartNum = tk.StringVar()
    supplierName = tk.StringVar()
    Quantity = tk.StringVar()
    Barcode = tk.StringVar()
    room = tk.StringVar()
    rack = tk.StringVar()
    shelf = tk.StringVar()
    shelfLocation = tk.StringVar()
    
    manIDLabel = tk.Label(adjustItemWindow, text = 'Manufacturer Part #: ', font=('calibre', 12))
    manNameLabel = tk.Label(adjustItemWindow, text = 'Manufacturer: ', font=('calibre', 12))
    SupplierPartNumLabel = tk.Label(adjustItemWindow, text = 'Supplier Part Number: ', font=('calibre', 12))
    supplierNameLabel = tk.Label(adjustItemWindow, text = 'Supplier: ', font=('calibre', 12))
    DescriptionLabel = tk.Label(adjustItemWindow, text = 'Description: ', font=('calibre', 12))
    QuantityLabel = tk.Label(adjustItemWindow, text = 'Quantity: ', font=('calibre', 12))
    BarcodeLabel = tk.Label(adjustItemWindow, text = 'Barcode: ', font=('calibre', 12))
    roomLabel = tk.Label(adjustItemWindow, text = 'Room: ', font=('calibre', 12))
    rackLabel = tk.Label(adjustItemWindow, text = 'Rack: ', font=('calibre', 12))
    shelfLabel = tk.Label(adjustItemWindow, text = 'Shelf: ', font=('calibre', 12))
    shelfLocationLabel = tk.Label(adjustItemWindow, text = 'Shelf Location: ', font=('calibre', 12))
    
    manIDEntry = tk.Entry(adjustItemWindow, textvariable = manID, font=('calibre', 12))
    manNameEntry = tk.Entry(adjustItemWindow, textvariable = manName, font=('calibre', 12))
    SupplierPartNumEntry = tk.Entry(adjustItemWindow, textvariable = supplierPartNum, font=('calibre', 12))
    supplierNameEntry = tk.Entry(adjustItemWindow, textvariable = supplierName, font=('calibre', 12))
    DescriptionEntry = tk.Text(adjustItemWindow, font = ('calibre', 12), width = 20, height = 3)
    QuantityEntry = tk.Entry(adjustItemWindow, textvariable = Quantity, font=('calibre', 12))
    BarcodeEntry = tk.Entry(adjustItemWindow, textvariable = Barcode, font=('calibre', 12))
    choiceList = ['Inventory', 'Mezannine', 'Pallet Rack']
    
    roomChoiceBox = ttk.Combobox(
                        adjustItemWindow,
                        state='readonly',
                        values = choiceList,
                        textvariable=room
                        )
    roomChoiceBox.set('Inventory')
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
    if(invRecords[0][4]):
        DescriptionEntry.insert('end', invRecords[0][4])
    if(invRecords[0][5]):
        QuantityEntry.insert(0, invRecords[0][5])
    if(invRecords[0][6]):
        BarcodeEntry.insert(0, invRecords[0][6])
    if(locRecords[0][0]):
        roomChoiceBox.set(locRecords[0][0])
    if(locRecords[0][1]):
        rackEntry.insert(0, chr(locRecords[0][1]))
    if(locRecords[0][2]):
        shelfEntry.insert(0, locRecords[0][2])
    if(locRecords[0][3]):
        shelfLocationEntry.insert(0, locRecords[0][3])

    manIDLabel.place(relx=.05, rely=.075, anchor='w')
    manIDEntry.place(relx=.55, rely=.075, anchor='center')
    
    manNameLabel.place(relx=.05, rely=.15, anchor='w')
    manNameEntry.place(relx=.55, rely=.15, anchor='center')
    
    SupplierPartNumLabel.place(relx=.05, rely=.225, anchor='w')
    SupplierPartNumEntry.place(relx=.55, rely=.225, anchor='center')
    
    supplierNameLabel.place(relx=.05, rely=.3, anchor='w')
    supplierNameEntry.place(relx=.55, rely=.3, anchor='center')
    
    DescriptionLabel.place(relx=.05, rely=.375, anchor='w')
    DescriptionEntry.place(relx=.55, rely=.4, anchor='center')
    
    QuantityLabel.place(relx=.05, rely=.475, anchor='w')
    QuantityEntry.place(relx=.55, rely=.475, anchor='center')
    
    BarcodeLabel.place(relx=.05, rely=.55, anchor='w')
    BarcodeEntry.place(relx=.55, rely=.55, anchor='center')
    
    roomLabel.place(relx=.05, rely=.625, anchor='w')
    roomChoiceBox.place(relx=.55, rely=.625, anchor='center')
    
    rackLabel.place(relx=.05, rely=.7, anchor='w')
    rackEntry.place(relx=.55, rely=.7, anchor='center')
    
    shelfLabel.place(relx=.05, rely=.775, anchor='w')
    shelfEntry.place(relx=.55, rely=.775, anchor='center')
    
    shelfLocationLabel.place(relx=.05, rely=.85, anchor='w')
    shelfLocationEntry.place(relx=.55, rely=.85, anchor='center')
    
    printButton = tk.Button(adjustItemWindow, text = "Print Label", command = printCode)
    printButton.place(relx= .7, rely= .925, anchor = 'center')
    
    adjustButton = tk.Button(adjustItemWindow, text = 'Adjust', command = adjustItem)
    adjustButton.place(relx= .5, rely= .925, anchor='center')

    adjustItemWindow.focus_force()
    adjustItemWindow.mainloop()
    return

def removeItem():
    removeItemWindow = tk.Tk()
    removeItemWindow.geometry("600x150")
    removeItemWindow.title("Remove Item")
    removeVar = tk.StringVar()
    cur = DG.conn.cursor()
    
    def itemRemoval(item_to_remove):
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
        return
            
    def removeCheckHelper(*args):
        manIDPartial = '%' + removeItemEntry.get().lower() + '%'
        sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE manufacturerid ILIKE %s'''
        cur.execute(sql, [manIDPartial])
        invRecords = cur.fetchall()
        if(invRecords):
            removeItemWindow.geometry("600x400")
            removeItemLabel.place(relx=.01, rely=.15)
            removeItemEntry.place(relx=.48, rely=.15, anchor='center')
            searchButton.place(relx=.7, rely=.15, anchor='center')

            def fillRemoveTree():
                for record in invRecords:
                    removeTree.insert("", 'end', values=(record[0], record[4], record[6], record[5]))     #manID, name, barcode, quantity))
                return
            
            def removeCheck():
                #Double check that item should actually be removed
                removeCheckWindow = tk.Tk()
                removeCheckWindow.geometry("400x200")
                removeCheckWindow.title("Are you sure?")
                removeCheckWindow.focus_force()
                
                item_to_remove = removeTree.item(removeTree.focus())['values'][0]
                removeText = "Are you sure you want to remove item: " + item_to_remove
                removeLabel = tk.Label(removeCheckWindow, text = removeText, font = ('calibre', 12))
                yesButton = tk.Button(removeCheckWindow, text = "Yes", command = lambda: [itemRemoval(item_to_remove), removeCheckWindow.destroy()])
                noButton = tk.Button(removeCheckWindow, text = "No", command = removeCheckWindow.destroy)
                removeItemEntry.unbind('<Return>')
                removeCheckWindow.bind('<Return>', lambda event:[itemRemoval(removeVar.get()), removeCheckWindow.destroy(), removeItemEntry.bind('<Return>', lambda e: removeCheck())])
                
                removeLabel.place(relx=.5, rely=.3, anchor='center')
                yesButton.place(relx=.2, rely=.6, anchor = 'center')
                noButton.place(relx=.8, rely=.6, anchor='center')   
                
                removeCheckWindow.mainloop()
                return
            
            removeTree = ttk.Treeview(removeItemWindow, selectmode = 'browse')
            removeTreeScrollbar = tk.Scrollbar(removeItemWindow, orient='vertical', command = removeTree.yview)
            
            removeTreeScrollbar.place(relx=.84, rely=.55, anchor = 'w')
            removeTree.place(relx=.1, rely=.55, anchor = 'w')
            returnButton.place(relx=.85, rely=.9, anchor='center')
            removeButton = tk.Button(removeItemWindow, text = 'Delete', command = removeCheck)
            removeButton.place(relx= .5, rely=.9, anchor='center')

            removeTree.configure(yscrollcommand = removeTreeScrollbar.set)
            removeTree["columns"] = ("1", "2", "3", "4")
            removeTree['show'] = 'headings' 
            removeTree.column("1", width = 100, anchor = 'w')
            removeTree.column("2", width = 200, anchor = 'w')
            removeTree.column("3", width = 100, anchor = 'w')
            removeTree.column("4", width = 60, anchor = 'w')
            removeTree.heading("1", text = "Manufacturer #")
            removeTree.heading("2", text = "Description")
            removeTree.heading("3", text = "Barcode")
            removeTree.heading("4", text = "Quantity")
            fillRemoveTree()
        return

    removeVar.trace_add('write', removeCheckHelper)
    removeItemLabel = tk.Label(removeItemWindow, text = "Manufacturer Number:", font=('calibre', 12, 'bold'))
    removeItemEntry = tk.Entry(removeItemWindow, textvariable = removeVar, font=('calibre', 12))
    
    searchButton = tk.Button(removeItemWindow, text = 'Search', command = removeCheckHelper)
    removeItemEntry.bind('<Return>', lambda e: removeCheckHelper())
    
    returnButton = tk.Button(removeItemWindow, text = 'Return', command = lambda: [removeItemWindow.destroy(), adminMenu()])
    
    removeItemLabel.place(relx=.01, rely=.4, anchor='w')
    removeItemEntry.place(relx=.48, rely=.4, anchor='center')
    searchButton.place(relx=.7, rely=.4, anchor='center')
    returnButton.place(relx=.85, rely=.85, anchor='center')
    
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
                tk.messagebox.showerror("Error", "Manufacturer Number not found")
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
            
        manIDLabel = tk.Label(createBomWindow, text = "Manufacturer Number:", font=('calibre', 12))
        manIDEntry = tk.Entry(createBomWindow, width = 30)
        quantityLabel = tk.Label(createBomWindow, text = "Quantity:", font=('calibre', 12))
        quantityEntry = tk.Entry(createBomWindow, width = 5)
        bomTree = ttk.Treeview(createBomWindow, selectmode = 'browse')
        completeBomButton = tk.Button(createBomWindow, text = "Finalize", command = finalize)
        addItemButton = tk.Button(createBomWindow, text = "Add Item", command = lambda:[addBomItem()])
        removeItemButton = tk.Button(createBomWindow, text = "Remove Item", command = lambda:[remBomItem()])
        bomScrollbar = tk.Scrollbar(createBomWindow, orient='vertical', command = bomTree.yview)
        returnButton = tk.Button(createBomWindow, text = 'Return', command = lambda:[createBomWindow.destroy(), createBOMGUI()])
        
        manIDEntry.focus_force()
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
        bomTree.heading("1", text = "Manufacturer Number")
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
    bomEntryLabel = tk.Label(bomWindow, text = "Type Manufacturer Numbers for \nBOM inventory check")
    nameList = []
    itemName = tk.StringVar()
    sql = '''SELECT Description FROM ''' + DG.invDatabase + ''' ORDER BY Description'''
    cur.execute(sql)
    records = cur.fetchall()
    for record in records:
        nameList.append(record[0])
    bomChoiceBox = ttk.Combobox(state='readonly', values = nameList, textvariable = itemName)
    bomEntryBox = tk.Entry(bomWindow, width = 25)
    createBomButton = tk.Button(bomWindow, text = "Create", command=createBom)
    checkInventoryButton = tk.Button(bomWindow, text="Check Inventory", command=checkInventoryHelper)
    returnButton = tk.Button(bomWindow, text = 'Return', command = lambda:[bomWindow.destroy(), adminMenu()])
    
    nameLabel.place(relx=.3, rely=.15, anchor = 'center')
    orLabel.place(relx=.5, rely=.25, anchor='center')
    bomEntryLabel.place(relx=.7, rely=.15, anchor='center')
    bomEntryBox.place(relx=.7, rely=.3, anchor='center')
    bomChoiceBox.place(relx=.3, rely=.3, anchor='center')
    createBomButton.place(relx=.3, rely=.6, anchor = 'center')
    checkInventoryButton.place(relx=.7, rely=.6, anchor='center')
    returnButton.place(relx=.85, rely=.85, anchor='center')
    bomEntryBox.focus_force()
    
    bomWindow.mainloop()
    return

def viewBuilds():
    viewBuildsWindow = tk.Tk()
    viewBuildsWindow.title("Builds/RMAs")
    viewBuildsWindow.geometry("300x300")
    viewBuildsWindow.focus_force()
    cur = DG.conn.cursor()
    searchBuild = tk.StringVar()
    searchLabel = tk.Label(viewBuildsWindow, text = "Search: ")
    searchEntry = tk.Entry(viewBuildsWindow, textvariable=searchBuild)
    buildListBox = tk.Listbox(viewBuildsWindow, width=30, height=8, selectmode = 'single')
    buildScrollbar = tk.Scrollbar(viewBuildsWindow)
    buildListBox.config(yscrollcommand=buildScrollbar.set)
    homeButton = tk.Button(viewBuildsWindow, text = "Home", command = lambda : [viewBuildsWindow.destroy(), mainMenu()])
    
    def buildSearch(*args):
        searchItem = '%' + searchBuild.get() + '%'
        buildListBox.delete(0, tk.END)
        sql = '''SELECT * FROM ''' + DG.buildDatabase + ''' WHERE build_name ILIKE %s'''
        cur.execute(sql, [searchItem])
        buildRecords = cur.fetchall()
        for i in range(len(buildRecords)):
            buildListBox.insert(i, buildRecords[i][0])
        return
    
    searchBuild.trace_add('write', buildSearch)
    
    def buildSelection(event):
        tableName = buildListBox.get(buildListBox.curselection())
        sql = '''SELECT * FROM ''' + tableName + ''' ORDER BY timeadded;'''
        cur.execute(sql)
        selectedBuildRecords = cur.fetchall()
        if(selectedBuildRecords):
            def fillBuildTree(rec):
                buildTree.insert("", 'end', values=(rec[0], rec[4], rec[5], rec[8])) 
                return
            def printHelper():
                sql = '''SELECT barcode FROM ''' + DG.buildDatabase + ''' WHERE build_name = %s;'''
                cur.execute(sql, [tableName])
                barRecords = cur.fetchall()
                barcode = barRecords[0][0]
                PL.createBarcodeImage(tableName.upper(), barcode)
                PL.printBarcode()
                return
            
            viewBuildsWindow.geometry("800x300")
            buildNameLabel = tk.Label(viewBuildsWindow, text = tableName, font=('calibre', 12, 'bold'))
            
            printCodeButton = tk.Button(viewBuildsWindow, text = "Print Barcode", command = printHelper)
            searchLabel.place(relx=.056, rely=.2, anchor = 'w')
            searchEntry.place(relx=.131, rely=.2, anchor='w')
            buildNameLabel.place(relx=.65, rely=.06, anchor='center')
            buildListBox.place(relx=.075, rely=.5, anchor='w')
            buildScrollbar.place(relx=.283, rely=.5, anchor='w')
            printCodeButton.place(relx=.8, rely = .92, anchor='center')
            homeButton.place(relx = .925, rely=.92, anchor = 'center')
    
            buildTree = ttk.Treeview(viewBuildsWindow, selectmode = 'browse')
            buildTreeScrollbar = tk.Scrollbar(viewBuildsWindow, orient='vertical', command = buildTree.yview)
            
            buildTree.place(relx=.65, rely=.475, anchor = 'center')
            buildTreeScrollbar.place(relx=.945, rely=.475, anchor = 'center')
            
            buildTree.configure(yscrollcommand = buildTreeScrollbar.set)
            buildTree["columns"] = ("1", "2", "3", "4")
            buildTree['show'] = 'headings' 
            buildTree.column("1", width = 100, anchor = 'w')
            buildTree.column("2", width = 200, anchor = 'w')
            buildTree.column("3", width = 60, anchor = 'w')
            buildTree.column("4", width = 130, anchor = 'w')
            buildTree.heading("1", text = "Manufacturer #")
            buildTree.heading("2", text = "Description")
            buildTree.heading("3", text = "Quantity")
            buildTree.heading("4", text = "Time added")
            for rec in selectedBuildRecords:    
                fillBuildTree(rec)
        return
    
    searchLabel.place(relx=.15, rely=.2, anchor = 'w')
    searchEntry.place(relx=.35, rely=.2, anchor='w')
    buildListBox.place(relx=.2, rely=.5, anchor='w')
    buildScrollbar.place(relx=.753, rely=.5, anchor='w')
    homeButton.place(relx = .7, rely=.85, anchor = 'w')
    
    sql = '''SELECT build_name FROM ''' + DG.buildDatabase + ''';'''
    cur.execute(sql)
    buildNameRecords = cur.fetchall()
    if(buildNameRecords):
        for i in range(len(buildNameRecords)):
            buildListBox.insert(i, buildNameRecords[i][0])
    buildListBox.bind('<<ListboxSelect>>', buildSelection)
    viewBuildsWindow.mainloop()
    return

def userMenu():
    userWindow = tk.Tk()
    userWindow.geometry("400x300")
    userWindow.title("Users")
    username = tk.StringVar()
    cur = DG.conn.cursor()
    
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
                sql = '''INSERT INTO ''' + DG.userDatabase + ''' (username, usercode) VALUES (%s, %s);
                        INSERT INTO ''' + DG.barDatabase + ''' (code) VALUES (%s);'''
                cur.execute(sql, [nameEntry.get().lower(), code, code])
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
        return
    
    # Helper function for double clicking items in User Listbox
    def viewUserHelper(event):
        viewUser()
        return
    
    def viewUser():
        if(not userListBox.curselection()):
            tk.messagebox.showerror("Error", 'Please select User')
        else:
            selectedUserWindow = tk.Tk()
            selectedUser = userListBox.get(userListBox.curselection()).lower()
            
            ## TO DO if RMA/Builds section doesn't work out
            ##
            # Search Transaction table for user
            # If transactions present, display Treeview with Transaction IDs and DateTimes
            # Selecting transaction opens up all items associated with transaction
            # Transaction ID can be user Entered "Check Out Reason"

            selectedUserWindow.geometry("300x150")
            selectedUserWindow.title("User Info")
            
            sql = '''SELECT usercode FROM ''' + DG.userDatabase + ''' WHERE username = %s;'''
            cur.execute(sql, [selectedUser])
            records = cur.fetchall()
            
            userLabel = tk.Label(selectedUserWindow, text = "User: ", font=('calibre', 12, 'bold'))
            selectedUserLabel = tk.Label(selectedUserWindow, text = '', font=('bold'))
            barcodeLabel = tk.Label(selectedUserWindow, text = "Barcode: ", font=('calibre', 12, 'bold'))
            selectedUserEntry = tk.Entry(selectedUserWindow)
            
            userLabel.place(relx=.1, rely=.3, anchor='w')
            selectedUserLabel.place(relx=.5, rely=.3, anchor='w')
            barcodeLabel.place(relx=.1, rely=.5, anchor='w')
            selectedUserEntry.place(relx=.5, rely=.5, anchor='w')
            
            selectedUserLabel.config(text = userListBox.get(userListBox.curselection()))
            selectedUserEntry.insert(0, records[0][0])
            selectedUserWindow.focus_force()
        return
    
    def deleteUser():
        userToDelete = userListBox.get(userListBox.curselection()).lower()
        sql = '''DROP TABLE IF EXISTS ''' + userToDelete + ''';'''
        cur.execute(sql)
        sql = '''DELETE FROM ''' + DG.userDatabase + ''' WHERE username = %s;'''
        cur.execute(sql, [userToDelete])
        return
    
    userListBox = tk.Listbox(userWindow)
    userScrollbar = tk.Scrollbar(userWindow)
    userListBox.config(yscrollcommand=userScrollbar.set)
    
    sql = '''SELECT username FROM ''' + DG.userDatabase + ''';'''
    cur.execute(sql)
    records = cur.fetchall()
    for record in records:
        userListBox.insert(tk.END, record[0].capitalize())
        
    viewUserButton = tk.Button(userWindow, text = "View User", command = viewUser)
    createUserButton = tk.Button(userWindow, text = "Create New User", command = createUser)
    deleteUserButton = tk.Button(userWindow, text = "Delete User", command = deleteUser)
    homeButton = tk.Button(userWindow, text = 'Home', command = lambda:[userWindow.destroy(), mainMenu()])
    userListBox.bind('<Double-1>', viewUserHelper)
    userListBox.place(relx=.5, rely=.3, anchor='center')
    userScrollbar.place(relx=.63, rely=.3, anchor='center')
    viewUserButton.place(relx=.5, rely=.65, anchor='center')
    createUserButton.place(relx=.5, rely=.75, anchor = 'center')
    deleteUserButton.place(relx=.5, rely=.85, anchor = 'center')
    homeButton.place(relx=.85, rely=.85, anchor = 'center')
    
    userWindow.focus_force()
      
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
            errorMessage = 'Less than ' + str(quantity) + ' "' + records[0][4] + '" available in database'
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
        manIDLabel = tk.Label(editItemWindow, text = 'Manufacturer Number:', font = ('calibre', 12))
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
        receiptScreen.geometry("400x200")

        def finalizeCheckout(buildBar):
            sql = '''SELECT * FROM ''' + DG.buildDatabase + ''' WHERE barcode = %s;'''
            cur.execute(sql, [buildBar])
            buildRecords = cur.fetchall()
            
            if(buildRecords):
                buildName = buildRecords[0][0]
                
                # Adjust when/if you want to add user to checkout
                username = None
                timeVar = datetime.now()
                currentTime = timeVar.strftime("%m-%d-%Y %H:%M:%S")

                for line in checkOutTree.get_children():
                    manID = checkOutTree.item(line).get('values')[0]
                    checkOutQuantity = checkOutTree.item(line).get('values')[3]
                    sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE ManufacturerID = %s;'''
                    cur.execute(sql, [str(manID)])
                    itemRecords = cur.fetchall()
                    
                    sql = '''INSERT INTO ''' + buildName + ''' (ManufacturerID, Manufacturer, SupplierPartNum, Supplier, Description, Quantity, Barcode, username, timeadded, BOM_ID)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                    cur.execute(sql, [itemRecords[0][0], itemRecords[0][1], itemRecords[0][2], itemRecords[0][3], itemRecords[0][4], checkOutQuantity, itemRecords[0][6], username, currentTime, itemRecords[0][7]])
                
                    quantity = itemRecords[0][5] - checkOutQuantity
                    sql = '''UPDATE ''' + DG.invDatabase + ''' SET quantity = %s WHERE manufacturerID = %s;'''
                    cur.execute(sql, [quantity, str(manID)])
                tk.messagebox.showinfo("Success", "Items checked out of inventory")
            else:
                tk.messagebox.showerror("Error", 'Build/RMA not found')
                buildBarEntry.focus_force()
                buildBarEntry.delete(0, tk.END)

            checkOutWindow.destroy()
            checkOut()
            return
        
        def finalizeCheckoutHelper():
            barcode = buildBarEntry.get()
            receiptScreen.destroy()
            finalizeCheckout(barcode)
            return
        
        def createNewBuild():
            receiptScreen.destroy()
            newBuildWindow = tk.Tk()
            newBuildWindow.title("New Build")
            newBuildWindow.geometry("400x200")
            buildType = tk.StringVar(newBuildWindow)
            buildNumber = tk.StringVar()
            buildLabel = tk.Label(newBuildWindow, text='RMA Number: ')
            
            def buildBoxChange(*args):
                if(buildChoiceBox.get() == 'RMA'):
                    buildLabel.config(text="RMA Number: ")
                else:
                    buildLabel.config(text="Name of Build: ")
                return
            
            def createBuild():
                def pullBarcode():
                    bar = barcodeEntry.get() + checkDigitLabel.cget("text")
                    return bar
                
                buildName = buildEntry.get()
                generateBarcode(barcodeEntry, checkDigitLabel)
                bar = pullBarcode()
                if(buildChoiceBox.get() == 'New Build'):
                    tableVar = 'Build_'
                else:
                    tableVar = 'RMA_'
                tableName = tableVar + buildName
                
                # Check to make sure table doesn't already exist
                sql = '''SELECT * FROM ''' + DG.buildDatabase + ''' WHERE build_name = %s;'''
                cur.execute(sql, [tableName])
                buildRecords = cur.fetchall()
                if(buildRecords):
                    tk.messagebox.showerror("Error", "Build already exists in database")
                    newBuildWindow.destroy()
                else:
                    sql = '''INSERT INTO ''' + DG.barDatabase + '''(code) VALUES (%s);'''
                    cur.execute(sql, [bar])
                    sql = '''INSERT INTO ''' + DG.buildDatabase + ''' (build_name, barcode) VALUES (%s, %s);'''
                    cur.execute(sql, [tableName.lower(), bar])
                    
                    sql = '''CREATE TABLE IF NOT EXISTS ''' + tableName + ''' (
                                ManufacturerID VARCHAR(100),
                                Manufacturer VARCHAR(100),
                                SupplierPartNum VARCHAR(100),
                                Supplier VARCHAR(100),
                                Description VARCHAR(100),
                                Quantity INT,
                                Barcode VARCHAR(100),
                                username VARCHAR(100),
                                timeadded VARCHAR(100),
                                BOM_ID SMALLINT);'''
                    cur.execute(sql)
                    newBuildWindow.destroy()
                    infoMessage = tableName + " Created succesfully"
                    tk.messagebox.showinfo("Success", infoMessage)
                    PL.createBarcodeImage(tableName.upper(), bar)
                    PL.printBarcode()
                    finalizeCheckout(bar)
                return
            
            buildType.trace_add('write', buildBoxChange)
            choiceList = ['RMA', 'New Build']
            buildChoiceBox = ttk.Combobox(
                                newBuildWindow,
                                state='readonly',
                                values = choiceList,
                                textvar = buildType
                                )
            buildChoiceBox.set('RMA')
            buildChoiceBox.place(relx=.5, rely=.4, anchor='center')

            buildEntry = tk.Entry(newBuildWindow, textvariable = buildNumber)
            buildEntry.focus_force()
            createButton = tk.Button(newBuildWindow, text = 'Create', command = createBuild)
            barcodeEntry = tk.Entry(newBuildWindow)
            checkDigitLabel = tk.Label(newBuildWindow, text='')
            barcodeLabel = tk.Label(newBuildWindow, text='')
            
            buildLabel.place(relx=.3, rely = .6, anchor = 'center')
            buildEntry.place(relx=.6, rely=.6, anchor = 'center')
            createButton.place(relx=.5, rely=.75, anchor='center')
            barcodeLabel.place(relx=.5, rely=.9, anchor='center')
            
            newBuildWindow.mainloop()
            return
        
        buildBarLabel = tk.Label(receiptScreen, text = "Build Barcode:", font = ('calibre', 12))
        buildBarEntry = tk.Entry(receiptScreen, width = 20)

        
        buildBarEntry.focus_force()
        finalizeOrderButton = tk.Button(receiptScreen, text = "Checkout Items", command = finalizeCheckoutHelper)
        
        buildListBox = tk.Listbox(receiptScreen)
        buildScrollbar = tk.Scrollbar(receiptScreen)
        buildListBox.configure(yscrollcommand=buildScrollbar.set)
        
        sql = '''SELECT build_name FROM ''' + DG.buildDatabase + ''';'''
        cur.execute(sql)
        records = cur.fetchall()

        orLabel = tk.Label(receiptScreen, text = "Or", font = ('calibre', 12))
        newBuildButton = tk.Button(receiptScreen, text = "Create New Build", command=createNewBuild)
        buildBarLabel.place(relx = .2, rely=.4, anchor='center')
        buildBarEntry.place(relx=.5, rely=.4, anchor = 'center')
        finalizeOrderButton.place(relx=.82, rely = .4, anchor='center')
        orLabel.place(relx=.5, rely=.6, anchor='center')
        newBuildButton.place(relx=.5, rely=.75, anchor='center')
        
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
    removeItemButton = tk.Button(checkOutWindow, text = 'Delete Item', command = removeItem)
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
    removeItemButton.place(relx=.9, rely=.45, anchor = 'center')
    completeOrderButton.place(relx=.5, rely=.85, anchor='center')
    homeButton.place(relx=.9, rely=.85, anchor = 'center')
    
    checkOutTree.configure(yscrollcommand = checkOutScrollbar.set)
    checkOutTree["columns"] = ("1", "2", "3", "4")
    checkOutTree['show'] = 'headings' 
    checkOutTree.column("1", width = 100, anchor = 'w')
    checkOutTree.column("2", width = 200, anchor = 'w')
    checkOutTree.column("3", width = 100, anchor = 'w')
    checkOutTree.column("4", width = 60, anchor = 'w')
    checkOutTree.heading("1", text = "Manufacturer #")
    checkOutTree.heading("2", text = "Description")
    checkOutTree.heading("3", text = "Barcode")
    checkOutTree.heading("4", text = "Quantity")
    checkOutWindow.mainloop()
    
    return

def inventoryBackup():
    tk.messagebox.showinfo("Alert", "Will create folders for year and month within selected directory.")
    saveFolder = filedialog.askdirectory()
    if(saveFolder):
        BU.createFile(saveFolder)
        messageDialog = "Database successfully backed up to:\n" + saveFolder
        tk.messagebox.showinfo("Success", messageDialog)
    return


def adminBuildMenu():
    cur = DG.conn.cursor()
    adminBuildMenuWindow = tk.Tk()
    adminBuildMenuWindow.geometry("400x200")
    adminBuildMenuWindow.title("Build Menu (Admin)")
    adminBuildMenuWindow.focus_force()
    
    def buildSelectionAdmin(*args):
        adminBuildMenu = tk.Tk()
        adminBuildMenu.geometry("600x350")
        buildName = buildListBox.get(buildListBox.curselection())
        adminBuildMenu.title(buildName)
        adminBuildMenu.focus_force()
        
        def fillBuildTree(rec):
            buildTree.insert("", 'end', values=(rec[0], rec[4], rec[5], rec[8])) 
            return
        
        def deleteBuild():
            print('Delete Build ' + buildName)
            return
        
        sql = '''SELECT * FROM ''' + buildName + ''' ORDER BY timeadded;'''
        cur.execute(sql)
        selectedBuildRecords = cur.fetchall()
        
        buildNameLabel = tk.Label(adminBuildMenu, text = buildName, font = ('calibre', 12, 'bold'))
        buildTree = ttk.Treeview(adminBuildMenu, selectmode = 'browse')
        buildTreeScrollbar = tk.Scrollbar(adminBuildMenu, orient='vertical', command = buildTree.yview)
        deleteBuildButton = tk.Button(adminBuildMenu, text='Delete Build', command = deleteBuild)
        
        buildNameLabel.place(relx=.5, rely=.07, anchor='center')
        buildTree.place(relx=.5, rely=.45, anchor = 'center')
        buildTreeScrollbar.place(relx=.89, rely=.45, anchor = 'center')
        deleteBuildButton.place(relx=.75, rely=.9, anchor='center')
        
        buildTree.configure(yscrollcommand = buildTreeScrollbar.set)
        buildTree["columns"] = ("1", "2", "3", "4")
        buildTree['show'] = 'headings' 
        buildTree.column("1", width = 100, anchor = 'w')
        buildTree.column("2", width = 200, anchor = 'w')
        buildTree.column("3", width = 60, anchor = 'w')
        buildTree.column("4", width = 130, anchor = 'w')
        buildTree.heading("1", text = "Manufacturer #")
        buildTree.heading("2", text = "Description")
        buildTree.heading("3", text = "Quantity")
        buildTree.heading("4", text = "Time added")
        for rec in selectedBuildRecords:    
            fillBuildTree(rec)
        
        return

    buildScrollbar = tk.Scrollbar(adminBuildMenuWindow)
    buildListBox = tk.Listbox(adminBuildMenuWindow, width=30, height=8, selectmode = 'single')
    buildListBox.config(yscrollcommand = buildScrollbar.set)
    sql = '''SELECT build_name FROM ''' + DG.buildDatabase + ''';'''
    cur.execute(sql)
    buildNameRecords = cur.fetchall()
    if(buildNameRecords):
        for i in range(len(buildNameRecords)):
            buildListBox.insert(i, buildNameRecords[i][0])
            
    buildListBox.place(relx=.5, rely=.4, anchor='center')
    buildScrollbar.place(relx=.73, rely=.4, anchor='center')
    buildListBox.bind('<Double-1>', buildSelectionAdmin)
    

def adminMenu():
    adminMenuWindow = tk.Tk()
    adminMenuWindow.title("Admin Menu")
    adminMenuWindow.geometry("600x400")
    adminMenuWindow.focus_force()
    
    backupButton = ttk.Button(adminMenuWindow, text = "Backup Inventory", command = inventoryBackup)
    removeButton = ttk.Button(adminMenuWindow, text = "Remove Item", command = lambda:[adminMenuWindow.destroy(), removeItem()])
    bomButton = ttk.Button(adminMenuWindow, text = "BOM Menu", command = lambda:[adminMenuWindow.destroy(), createBOMGUI()])
    buildButton = ttk.Button(adminMenuWindow, text = "Builds", command = lambda: [adminMenuWindow.destroy(), adminBuildMenu()])
    homeButton = ttk.Button(adminMenuWindow, text = "Home", command = lambda:[adminMenuWindow.destroy(), mainMenu()])
    
    backupButton.place(relx=.5, rely=.4, anchor='center')
    removeButton.place(relx=.5, rely=.5, anchor='center')
    bomButton.place(relx=.5, rely=.6, anchor='center')
    buildButton.place(relx=.5, rely=.7, anchor='center')
    homeButton.place(relx=.75, rely=.85, anchor='center')
    return

def adminLogin():
    adminLoginWindow = tk.Tk()
    adminLoginWindow.title("Admin Login")
    adminLoginWindow.geometry("400x200")
    userPass = tk.StringVar()
    
    def loginCheck():
        password = b'$2b$12$STTqL.4AVbfd9eY3YFrl8uSsBaYdL8mupGcdRQRGmE7AH0h0Ag9am'
        userPass = passEntry.get()
        passBytes = userPass.encode('utf-8')
        #passHash = bcrypt.hashpw(passBytes, bcrypt.gensalt())
        if bcrypt.checkpw(passBytes, password):    
            adminLoginWindow.destroy()
            adminMenu()
        else:
            tk.messagebox.showerror("Error", "Incorrect password entered")
        return
    
    adminLabel = tk.Label(adminLoginWindow, text = "Administrator", font = ('calibre', 12))
    passLabel = tk.Label(adminLoginWindow, text = "Password: ", font = ('calibre', 12))
    passEntry = tk.Entry(adminLoginWindow, show='*', textvariable = userPass)
    passEntry.focus_force()
    loginButton = tk.Button(adminLoginWindow, text = "Login", command = loginCheck)
    homeButton = tk.Button(adminLoginWindow, text = "Home", command = lambda: [adminLoginWindow.destroy(), mainMenu()])
    passEntry.bind("<Return>", lambda e : loginCheck())
    
    adminLabel.place(relx=.5, rely=.3, anchor = 'center')
    passLabel.place(relx=.3, rely=.5, anchor='center')
    passEntry.place(relx=.6, rely=.5, anchor='center')
    loginButton.place(relx=.5, rely=.75, anchor='center')
    homeButton.place(relx=.85, rely=.85, anchor='center')
    
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
    cur = DG.conn.cursor()
    global mainMenuWindow
    global searchVar
    global searchType
    mainMenuWindow = tk.Tk()
    mainMenuWindow.geometry("600x200+500+300")
    mainMenuWindow.title("Main Menu")
    ttk.Style().configure("TButton", background="#ccc")

    searchVar = tk.StringVar()
    searchType = tk.StringVar()
    mainMenuWindow.focus_force()
    
    # When SQL server is connected, use this instead of dummy list below
    choiceList = ['Barcode', 'Manufacturer Number', 'Item Name']
    
    searchChoiceBox = ttk.Combobox(
                        mainMenuWindow,
                        state='readonly',
                        values = choiceList,
                        textvariable=searchType
                        )
    searchChoiceBox.set('Barcode')
    
    def searchAdjustment(*args):
        searchItem = '%' + searchVar.get() + '%'
        if(searchType.get() == 'Manufacturer Number'):
            sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE manufacturerid ILIKE %s order by manufacturerid;'''
            recNum = 0
        elif(searchType.get() == 'Item Name'):
            sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE Description ILIKE %s order by Description;'''
            recNum = 4
        else:
            print('searchType: ' + searchType.get())
            return
        cur.execute(sql, [searchItem])
        records = cur.fetchall()
        if(records):
            for i in range(len(records)):
                args[0].insert(i, records[i][recNum])
            
            def listBoxSelection(*listBoxArgs):
                itemIndex = args[0].curselection()[0]
                #mainMenuWindow.destroy()
                adjustItemGUI(records[itemIndex][0])
                return
            selectButton = tk.Button(mainMenuWindow, text = 'Select Item', command = listBoxSelection)
            selectButton.place(relx=.9, rely=.4, anchor='center')
            args[0].bind("<Double-Button-1>", listBoxSelection)
        return

    def searchHelper(*args):
        if(searchType.get() != 'Barcode'):
            mainMenuWindow.geometry("600x500")
            invListbox = tk.Listbox(mainMenuWindow, width=60, height=15, selectmode = 'single')
            invScrollbar = tk.Scrollbar(mainMenuWindow)
            
            invListbox.place(relx=.5, rely=.4, anchor='center')
            invScrollbar.place(relx=.79, rely=.4, anchor='center')
            invListbox.configure(yscrollcommand=invScrollbar.set)
            # Row 2
            addItemButton.place(relx=.5, rely=.7, anchor='center')
            
            # Row 3
            buildsButton.place(relx=.5, rely=.775, anchor = 'center')
            
            # Row 4
            checkOutButton.place(relx=.5, rely=.85, anchor='center')
            
            adminButton.place(relx=.85, rely=.9, anchor = 'center')
            
            searchAdjustment(invListbox)
        return
    
    def adminMenuHelper():
        mainMenuWindow.destroy()
        adminLogin()
        return
    
    def barcodeSearchHelper():
        if(searchType.get() == 'Barcode'):
            barcodeSearch()
        return
    
    def barcodeSearch():
        if(searchType.get() == 'Barcode'):
            bar = searchVar.get()
            sql = '''SELECT * FROM ''' + DG.barDatabase + ''' WHERE code = %s'''
            cur.execute(sql, [bar])
            records = cur.fetchall()
            if(not records):
                tk.messagebox.showerror("Error", 'Item not found')
                searchInventoryEntry.delete(0, tk.END)
            else:
                sql = '''SELECT ManufacturerID FROM ''' + DG.invDatabase + ''' WHERE Barcode = %s'''
                cur.execute(sql, [records[0][0]])
                records = cur.fetchall()
                #mainMenuWindow.destroy()
                searchInventoryEntry.delete(0, tk.END)
                adjustItemGUI(records[0][0])
                
        else:
            print("Made it to barcodeSearch but searchType was not Barcode")
        return
    

    searchVar.trace_add('write', searchHelper)
    searchInventoryLabel = tk.Label(mainMenuWindow, text='Search', font=('calibre', 12, 'bold'))
    searchInventoryEntry = tk.Entry(mainMenuWindow, textvariable = searchVar, font=('calibre', 12))  
    #
    # THIS GETS CALLED NO MATTER WHAT IF THE USER HITS ENTER ON A SEARCH
    # CREATE HELPER FUNCTION TO REDIRECT IF IT'S NOT A BARCODE
    #
    searchInventoryEntry.bind('<Return>', lambda e: barcodeSearchHelper())     
    #searchErrorLabel = tk.Label(mainMenuWindow, text='', font=('calibre', 12), fg='red')
    searchButton = ttk.Button(mainMenuWindow, text = "Search", command = lambda: [barcodeSearch()])
    addItemButton = ttk.Button(mainMenuWindow, text = "Add Item", command = lambda: [addItemGUI()])
    #removeItemButton = ttk.Button(mainMenuWindow, text = "Delete Item", command = lambda: [mainMenuWindow.destroy(), removeItem()])
    #createBomButton = ttk.Button(mainMenuWindow, text = "BOMs", command = lambda: [mainMenuWindow.destroy(), createBOMGUI()])
    buildsButton = ttk.Button(mainMenuWindow, text="Builds/RMAs", command = lambda: [mainMenuWindow.destroy(), viewBuilds()])
    checkOutButton = ttk.Button(mainMenuWindow, text = 'Check Out', command = lambda:[mainMenuWindow.destroy(), checkOut()])
    #userButton = ttk.Button(mainMenuWindow, text="Users", command = lambda: [mainMenuWindow.destroy(), userMenu()])
    #barcodeGeneratorButton = ttk.Button(mainMenuWindow, text = "Generate Barcode", command = lambda:[generateBarcode(barcodeEntry, checkDigitLabel)])
    #barcodeEntry = tk.Entry(mainMenuWindow, font=('calibre', 12))
    #checkDigitLabel = tk.Label(mainMenuWindow, text = '', font=('calibre', 12))
    adminButton = ttk.Button(mainMenuWindow, text = 'Admin', command = adminMenuHelper)

    # Row 1
    searchInventoryLabel.place(relx=.15, rely=.1, anchor='center')
    searchInventoryEntry.place(relx=.38, rely=.1, anchor='center')    
    searchChoiceBox.place(relx=.67, rely=.1, anchor='center')
    searchButton.place(relx=.88, rely=.1, anchor='center')
    #searchErrorLabel.place(relx=.38, rely=.15, anchor='center')
    
    # Row 2
    addItemButton.place(relx=.5, rely=.3, anchor='center')
    
    # Row 3
    buildsButton.place(relx=.5, rely=.5, anchor = 'center')
    
    # Row 4
    checkOutButton.place(relx=.5, rely=.7, anchor='center')
    
    adminButton.place(relx=.85, rely=.9, anchor = 'center')
    searchInventoryEntry.focus_force()
    mainMenuWindow.mainloop()
    return
    
def main():
    DG.main()
    mainMenu()
    DG.close()

if __name__ == '__main__':
    main()