# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 08:32:28 2023

@author: Luke
"""
# Hi Corey
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
    subWindow_x = str(mainMenuWindow.winfo_x() + 100)
    subWindow_y = str(mainMenuWindow.winfo_y() + 50)
    windowPosition = subWindow_x + "+" + subWindow_y
    newItemWindow.geometry("600x600" + "+" + windowPosition)
    newItemWindow.title('New Item')
    cur = DG.conn.cursor()        
 
    def dataCheck(event):
        manID_To_Check = manIDEntry.get()
        sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE ManufacturerID = %s'''
        cur.execute(sql, [manID_To_Check])
        manIDInvRecords = cur.fetchall()
        if(manIDInvRecords):
            for rec in manIDInvRecords:
                if(rec[8] == kitChoiceBox.get()):
                    tk.messagebox.showinfo('Alert', 'Identical Man. # and Kit has already been found in our system\nPlease double check information and adjust quantity on next page', parent = newItemWindow)
                    subWindow_x = str(newItemWindow.winfo_x() + 100)
                    subWindow_y = str(newItemWindow.winfo_y() + 50)
                    subWindowLoc = subWindow_x + "+" + subWindow_y
                    newItemWindow.destroy()
                    adjustItemGUI(rec[6], subWindowLoc)
                    return
            for rec in manIDInvRecords:
                tk.messagebox.showinfo("Alert", "Manufacturer Number Records Found\nPlease make sure to enter new kit, quantity and location", parent = newItemWindow)
                if(rec[8] == '0'):
                    #print("Rec[0]: ", rec[0], "Rec[1]: ", rec[1], "Rec[2]: ", rec[2], "Rec[3]: ", rec[3], "Rec[4]: ", rec[4])
                    if(rec[0]):
                        manIDEntry.delete(0, tk.END)
                        manIDEntry.insert(0, rec[0])
                    if(rec[1]):
                        manNameEntry.delete(0, tk.END)
                        manNameEntry.insert(0, rec[1])
                    if(rec[2]):
                        supplierPartNumEntry.delete(0, tk.END)
                        supplierPartNumEntry.insert(0, rec[2])
                    if(rec[3]):
                        supplierNameEntry.delete(0, tk.END)
                        supplierNameEntry.insert(0, rec[3])
                    if(rec[4]):
                        descriptionEntry.delete("1.0", tk.END)
                        descriptionEntry.insert("1.0", rec[4])
                    return
            # If nothing was found that is NOT within a kit, then just pull from first available record
            #print("manIDInvRecords[0][0]: ", manIDInvRecords[0][0], "manIDInvRecords[0][1]: ", manIDInvRecords[0][1], "manIDInvRecords[0][2]: ", manIDInvRecords[0][2], "manIDInvRecords[0][3]: ", manIDInvRecords[0][3], "manIDInvRecords[0][4]: ", manIDInvRecords[0][4])
            if(manIDInvRecords[0][0]):
                manIDEntry.delete(0, tk.END)
                manIDEntry.insert(0, manIDInvRecords[0][0])
            if(manIDInvRecords[0][1]):
                manNameEntry.delete(0, tk.END)
                manNameEntry.insert(0, manIDInvRecords[0][1])
            if(manIDInvRecords[0][2]):
                supplierPartNumEntry.delete(0, tk.END)
                supplierPartNumEntry.insert(0, manIDInvRecords[0][2])
            if(manIDInvRecords[0][3]):
                supplierNameEntry.delete(0, tk.END)
                supplierNameEntry.insert(0, manIDInvRecords[0][3])
            if(manIDInvRecords[0][4]):
                descriptionEntry.delete("1.0", tk.END)
                descriptionEntry.insert("1.0", manIDInvRecords[0][4])
        return
    
    def pullBarcode():
        generatedBarcode = DG.createBarcode()
        barcodeEntry.delete(0, tk.END)
        barcodeEntry.insert(0, generatedBarcode)
        return
    
    # If Else statements are to convert empty string to something that can be stored in SMALLINT
    # Could also be used to send warning when user tries to establish something without a data field
    def newItem():
        if(kitChoiceBox.get() == "None"):
            kitChoice = '0'
        else:
            kitChoice = kitChoiceBox.get()
        
        if(manIDEntry.get() == ""):
            newManID = None
        else:
            newManID = manIDEntry.get().lower()
            
        if(manNameEntry.get() == ""):
            newManName = None
        else:
            newManName = manNameEntry.get().lower()
            
        if(supplierPartNumEntry.get() == ""):
            newSupplierPartNum = None
        else:
            newSupplierPartNum = supplierPartNumEntry.get()
        
        if(supplierNameEntry.get() == ""):
            newSupplierName = None
        else:
            newSupplierName = supplierNameEntry.get().lower()
        
        newDescription = descriptionEntry.get('1.0', tk.END).strip()
        
        if(quantityEntry.get() == ""):
            newQuantity = 0
        else:
            newQuantity = quantityEntry.get()
            
        newBarcode = barcodeEntry.get()
        if(len(newBarcode) != 12):
            tk.messagebox.showerror('Error', 'Please Enter a valid 12 digit barcode')
            return

        newBomID = None
        
        if(roomChoiceBox.get() == ""):
            newRoom = None
        else:
            newRoom = roomChoiceBox.get()
        
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
            
        # Check if Barcode is already in system, do extraneous checks
        # This error should never run do to other safeties in place but it's critical that no items be added with duplicate barcodes
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
 
        # Check if ManufacturerID/Kit pair is already in system
        # Used in conjunction with DataCheck() above which helps with filling in information that was previously established
        sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE ManufacturerID = %s'''
        cur.execute(sql, [newManID])
        manIDRecords = cur.fetchall()
        if(manIDRecords):
            for manRecord in manIDRecords:
                barcode = manRecord[6]
                kit = manRecord[8]
                if(kit == kitChoice):  
                    tk.messagebox.showinfo('Alert', 'Identical Man. # and Kit has already been found in our system\nPlease double check information and adjust quantity on next page', parent = newItemWindow)
                    subWindow_x = str(newItemWindow.winfo_x() + 100)
                    subWindow_y = str(newItemWindow.winfo_y() + 50)
                    subWindowLoc = subWindow_x + "+" + subWindow_y
                    newItemWindow.destroy()
                    adjustItemGUI(barcode, subWindowLoc)
                    return

        # Label creation and calling of the Label printer
        labelText = newManID.lower()
        if(roomChoiceBox.get() != ''):
            labelText = labelText + ' ' + roomChoiceBox.get()
        if(rackEntry.get() != ''):
                labelText = labelText + ' ' + rackEntry.get().upper()
        if(shelfEntry.get() != ''):
                labelText = labelText + '-' + shelfEntry.get()
        PL.createBarcodeImage(labelText, newBarcode)
        PL.printBarcode()

        sql='''INSERT INTO ''' + DG.invDatabase + ''' (ManufacturerID, Manufacturer, SupplierPartNum, Supplier, Description, Quantity, Barcode, BOM_ID, kit)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
             END'''
        cur.execute(sql, [newManID, newManName, newSupplierPartNum, newSupplierName, newDescription, newQuantity, newBarcode, newBomID, kitChoice])
        
        sql = '''INSERT INTO ''' + DG.locDatabase + ''' (Room, Rack, Shelf, Shelf_Location, Barcode)
                    VALUES (%s, %s, %s, %s, %s);
                END'''
        cur.execute(sql, [newRoom, newRack, newShelf, newShelfLocation, newBarcode])
        
        sql = '''INSERT INTO ''' + DG.barDatabase + ''' (code) VALUES (%s); END'''
        cur.execute(sql, [newBarcode])

        if(kitChoice != '0'):
            sql = '''INSERT INTO ''' + kitChoice + ''' (manufacturerid, manufacturer, supplierpartnum, supplier, description, quantity, barcode, username, timeadded, bom_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); END'''
            cur.execute(sql, [newManID, newManName, newSupplierPartNum, newSupplierName, newDescription, newQuantity, newBarcode, None, None, newBomID])
        
        print('Item has been added')
        newItemWindow.destroy()
        return

    # variables for adding items
    manID = tk.StringVar()
    manName = tk.StringVar()
    SupplierPartNum = tk.StringVar()
    supplierName = tk.StringVar()
    Quantity = tk.StringVar()
    Barcode = tk.StringVar()
    room = tk.StringVar()
    kit = tk.StringVar()
    rack = tk.StringVar()
    shelf = tk.StringVar()
    shelfLocation = tk.StringVar()
    
    # Labels 
    kitLabel = tk.Label(newItemWindow, text='Kit', font=('calibre', 12))
    manIDLabel = tk.Label(newItemWindow, text = 'Manufacturer Number: ', font=('calibre', 12))
    manNameLabel = tk.Label(newItemWindow, text = 'Manufacturer: ', font=('calibre', 12))
    supplierPartNumLabel = tk.Label(newItemWindow, text = 'Supplier Part Number: ', font=('calibre', 12))
    supplierNameLabel = tk.Label(newItemWindow, text = 'Supplier Name: ', font=('calibre', 12))
    descriptionLabel = tk.Label(newItemWindow, text = 'Description: (100 Chars max)', font=('calibre', 12))
    quantityLabel = tk.Label(newItemWindow, text = 'Quantity: ', font=('calibre', 12))
    barcodeLabel = tk.Label(newItemWindow, text = 'Barcode: ', font=('calibre', 12))
    roomLabel = tk.Label(newItemWindow, text = 'Room: ', font=('calibre', 12))
    rackLabel = tk.Label(newItemWindow, text = 'Rack: ', font=('calibre', 12))
    shelfLabel = tk.Label(newItemWindow, text = 'Shelf: ', font=('calibre', 12))
    shelfLocationLabel = tk.Label(newItemWindow, text = 'Shelf Location: ', font=('calibre', 12))
    
    # Entry Fields
    kitList = ['None']
    sql = '''SELECT name FROM ''' + DG.kitDatabase + ''';'''
    cur.execute(sql)
    kits = cur.fetchall()
    for kit in kits:
        kitList.append(kit[0])
    
    kitChoiceBox = ttk.Combobox(
                        newItemWindow,
                        state='readonly',
                        values = kitList,
                        textvariable=kit
                        )
    kitChoiceBox.set('None')
    manIDEntry = tk.Entry(newItemWindow, textvariable = manID, font=('calibre', 12))
    manNameEntry = tk.Entry(newItemWindow, textvariable = manName, font=('calibre', 12))
    supplierPartNumEntry = tk.Entry(newItemWindow, textvariable = SupplierPartNum, font=('calibre', 12))
    supplierNameEntry = tk.Entry(newItemWindow, textvariable = supplierName, font=('calibre', 12)) 
    descriptionEntry = tk.Text(newItemWindow, font = ('calibre', 12), width = 20, height = 3)
    quantityEntry = tk.Entry(newItemWindow, textvariable = Quantity, font=('calibre', 12))
    barcodeEntry = tk.Entry(newItemWindow, textvariable = Barcode, font=('calibre', 12))
    
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
           
    kitLabel.place(relx=.05, rely=.05, anchor='w')
    kitChoiceBox.place(relx=.6, rely=.05, anchor='center')
    
    manIDLabel.place(relx=.05, rely=.13, anchor='w')
    manIDEntry.place(relx=.6, rely=.13, anchor='center')
    
    manNameLabel.place(relx=.05, rely=.2, anchor='w')
    manNameEntry.place(relx=.6, rely=.2, anchor='center')
    
    supplierPartNumLabel.place(relx=.05, rely=.27, anchor='w')
    supplierPartNumEntry.place(relx=.6, rely=.27, anchor='center')
    
    supplierNameLabel.place(relx=.05, rely=.34, anchor='w')
    supplierNameEntry.place(relx=.6, rely=.34, anchor='center')
    
    descriptionLabel.place(relx=.05, rely=.41, anchor='w')
    descriptionEntry.place(relx=.6, rely=.435, anchor='center')
    
    quantityLabel.place(relx=.05, rely=.505, anchor='w')
    quantityEntry.place(relx=.6, rely=.505, anchor='center')
    
    barcodeLabel.place(relx=.05, rely=.575, anchor='w')
    barcodeEntry.place(relx=.6, rely=.575, anchor='center')
    
    roomLabel.place(relx=.05, rely=.645, anchor='w')
    roomChoiceBox.place(relx=.6, rely=.645, anchor='center')
    
    rackLabel.place(relx=.05, rely=.715, anchor='w')
    rackEntry.place(relx=.6, rely=.715, anchor='center')
    
    shelfLabel.place(relx=.05, rely=.785, anchor='w')
    shelfEntry.place(relx=.6, rely=.785, anchor='center')
    
    shelfLocationLabel.place(relx=.05, rely=.855, anchor='w')
    shelfLocationEntry.place(relx=.6, rely=.855, anchor='center')
    
    manIDEntry.focus_force()
    
    # Check if item is in inventory, if it is, update information
    # If item with identical manID and Kit, take user to adjustItem Page for said item
    manIDEntry.bind("<FocusOut>", dataCheck)
    
    createButton = tk.Button(newItemWindow, text = 'Add Item', command = newItem)
    createButton.place(relx=.5, rely = .925, anchor='center')
    
    barcodeGeneratorButton = tk.Button(newItemWindow, text = "Generate Barcode", command = pullBarcode)
    barcodeGeneratorButton.place(relx=.875, rely=.575, anchor='center')
    #barcodeEntry = tk.Entry(newItemWindow, font=('calibre', 12))
    #checkDigitLabel = tk.Label(newItemWindow, text = '', font=('calibre', 12))
    
    # Fill in the barcode entry automatically on window creation
    #generateBarcode(barcodeEntry, checkDigitLabel)
    #pullBarcode(BarcodeEntry)
    generatedBarcode = DG.createBarcode()
    barcodeEntry.delete(0, tk.END)
    barcodeEntry.insert(0, generatedBarcode)
    
    newItemWindow.mainloop()
    return

def adjustItemGUI(barcode_for_adjustment, location):
    cur = DG.conn.cursor()
    # Check to see if all manufacturerIDs need to be updated
    barcode_for_adjustment = str(barcode_for_adjustment)
    invRecords, locRecords = DG.searchID(barcode_for_adjustment)
    
    adjustItemWindow = tk.Tk()
    adjustItemWindow.geometry("600x600+" + location)
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
            
        adjustedroom = roomChoiceBox.get()
        # This will probably need to be adjusted to allow for doubled letters
        # Just parse the string and maybe add them together? Shouldn't cause an issue
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
        
        sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE Barcode = %s'''
        cur.execute(sql, [str(barcode_for_adjustment)])
        invRecords_for_manIDCheck = cur.fetchall()
        if(invRecords_for_manIDCheck[0][0] != manIDEntry.get().lower() or invRecords_for_manIDCheck[0][1] != manNameEntry.get().lower() or invRecords_for_manIDCheck[0][2] != SupplierPartNumEntry.get() or invRecords_for_manIDCheck[0][3] != supplierNameEntry.get() or invRecords_for_manIDCheck[0][4] != DescriptionEntry.get('1.0', tk.END).strip()):
            tk.messagebox.showinfo("Alert", "Adjusted Descriptions, Manufacturer and Supplier information are changed for all items sharing a Manufacturer Number")
            sql = '''UPDATE ''' + DG.invDatabase + ''' 
                    SET ManufacturerID = %s,
                        Manufacturer = %s,
                        SupplierPartNum = %s, 
                        Supplier = %s, 
                        Description = %s
                    WHERE Manufacturerid = %s;
                    END'''
            cur.execute(sql, [adjustedManID, adjustedManName, adjustedSupplierPartNum, adjustedSupplierName, adjustedDescription, invRecords[0][0]])
            
            for database in ['ssg_kits', 'ssg_builds', 'ssg_rmas']:
                sql = '''SELECT name FROM ''' + database + ''';'''
                cur.execute(sql)
                buildListRecords = cur.fetchall()
                for buildName in buildListRecords:
                    sql = '''UPDATE ''' + buildName[0] + ''' 
                            SET ManufacturerID = %s,
                                Manufacturer = %s,
                                SupplierPartNum = %s, 
                                Supplier = %s, 
                                Description = %s
                            WHERE Manufacturerid = %s;
                            END'''
                    cur.execute(sql, [adjustedManID, adjustedManName, adjustedSupplierPartNum, adjustedSupplierName, adjustedDescription, invRecords[0][0]])
        
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
    
    kitLabel = tk.Label(adjustItemWindow, text = "Kit/Build/RMA", font=('calibre', 12))
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
    
    if(invRecords[0][8] == '0'):
        kitName = 'No Kit/RMA/Build'
    else:
        kitName = invRecords[0][8]
    kitNameLabel = tk.Label(adjustItemWindow, text = kitName, font=('calibre', 12))
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
    if(invRecords[0][5] or invRecords[0][5] == 0):
        QuantityEntry.insert(0, invRecords[0][5])
    if(invRecords[0][6]):
        BarcodeEntry.insert(0, invRecords[0][6])
    if(locRecords[0][0]):
        roomChoiceBox.set(locRecords[0][0])
    if(locRecords[0][1]):
        rackEntry.insert(0, chr(locRecords[0][1]))
    if(locRecords[0][2] != None):
        shelfEntry.insert(0, locRecords[0][2])
    if(locRecords[0][3]):
        shelfLocationEntry.insert(0, locRecords[0][3])
        
    kitLabel.place(relx=.05, rely=.05, anchor='w')
    kitNameLabel.place(relx=.55, rely=.05, anchor='center')
    
    manIDLabel.place(relx=.05, rely=.12, anchor='w')
    manIDEntry.place(relx=.55, rely=.12, anchor='center')
    
    manNameLabel.place(relx=.05, rely=.19, anchor='w')
    manNameEntry.place(relx=.55, rely=.19, anchor='center')
    
    SupplierPartNumLabel.place(relx=.05, rely=.26, anchor='w')
    SupplierPartNumEntry.place(relx=.55, rely=.26, anchor='center')
    
    supplierNameLabel.place(relx=.05, rely=.33, anchor='w')
    supplierNameEntry.place(relx=.55, rely=.33, anchor='center')
    
    DescriptionLabel.place(relx=.05, rely=.4, anchor='w')
    DescriptionEntry.place(relx=.55, rely=.425, anchor='center')
    
    QuantityLabel.place(relx=.05, rely=.52, anchor='w')
    QuantityEntry.place(relx=.55, rely=.52, anchor='center')
    
    BarcodeLabel.place(relx=.05, rely=.59, anchor='w')
    BarcodeEntry.place(relx=.55, rely=.59, anchor='center')
    
    roomLabel.place(relx=.05, rely=.66, anchor='w')
    roomChoiceBox.place(relx=.55, rely=.66, anchor='center')
    
    rackLabel.place(relx=.05, rely=.73, anchor='w')
    rackEntry.place(relx=.55, rely=.73, anchor='center')
    
    shelfLabel.place(relx=.05, rely=.8, anchor='w')
    shelfEntry.place(relx=.55, rely=.8, anchor='center')
    
    shelfLocationLabel.place(relx=.05, rely=.87, anchor='w')
    shelfLocationEntry.place(relx=.55, rely=.87, anchor='center')
    
    printButton = tk.Button(adjustItemWindow, text = "Print Label", command = printCode)
    printButton.place(relx= .7, rely= .94, anchor = 'center')
    
    adjustButton = tk.Button(adjustItemWindow, text = 'Adjust', command = adjustItem)
    adjustButton.place(relx= .5, rely= .94, anchor='center')

    #manIDEntry.bind("<FocusOut>", checkAdjustments)
    adjustItemWindow.focus_force()
    adjustItemWindow.mainloop()
    return

def viewBuilds(location, callLocation):
    tableName = None
    viewBuildsWindow = tk.Tk()
    viewBuildsWindow.title("Kits/Builds/RMAs")
    viewBuildsWindow.geometry("300x300+" + location)
    viewBuildsWindow.focus_force()
    #kitType = tk.StringVar()
    cur = DG.conn.cursor()

    # I don't know how healthy this is, I'm using the error response of calling a function on an empty window to check whether it's open
    # May cause issues down the line
    # Right now it seems to work, so it stays
    def returnHelper():
        viewBuildsWindow.destroy()
        if(callLocation == None):
            try:
                if(mainMenuWindow.winfo_exists()):
                    mainMenuWindow.focus_force()
            except:
                mainMenu()
        elif(callLocation == 'Admin'):
            try:
                Admin("200+200")
            except:
                print("Issue returning to Admin Menu")
                mainMenu()
        return
    
    def wipeTree():
        for item in buildTree.get_children():
            buildTree.delete(item)
        return
    
    def populateBuildListBox():
        buildListBox.delete(0, tk.END)
        buildsList = []
        if(callLocation != 'Admin'):
            sql = '''SELECT name FROM ''' + DG.kitDatabase + ''' UNION
                    SELECT name FROM ''' + DG.rmaDatabase + ''' WHERE userview = 1 UNION
                    SELECT name FROM ''' + DG.buildDatabase + ''' WHERE userview = 1;'''
        else:
            sql = '''SELECT name FROM ''' + DG.kitDatabase + ''' UNION
                    SELECT name FROM ''' + DG.rmaDatabase + ''' UNION
                    SELECT name FROM ''' + DG.buildDatabase + ''';'''
        cur.execute(sql)
        buildNameRecords = cur.fetchall()
        if(buildNameRecords):
            for build in buildNameRecords:
                buildsList.append(build[0])
            buildsList.sort()
            for i in range(len(buildsList)):
                buildListBox.insert(i, buildsList[i])
        return
    
    def editBuild():
        try:
            tableNameEditBuild = buildListBox.get(buildListBox.curselection())
        except:
            #print(buildNameLabel.cget("text"))
            tableNameEditBuild = buildNameLabel.cget("text")
        if(tableNameEditBuild[:4] == 'rma_'):
            database = DG.rmaDatabase
        if(tableNameEditBuild[:6] == 'build_'):
            database = DG.buildDatabase
        if(tableNameEditBuild[:4] == 'kit_'):
            database = DG.kitDatabase
        sql = '''SELECT barcode FROM ''' + database + ''' WHERE name = %s;'''
        cur.execute(sql, [tableNameEditBuild])
        records = cur.fetchall()
        if records:
            barcode = records[0][0]
            subWindowLoc = childWindowLocation(viewBuildsWindow)
            viewBuildsWindow.destroy()
            callLocation = None
            checkOut(barcode, subWindowLoc, callLocation)
        return
    
    def buildSearch(*args):
        barcodeCheck = searchBuild.get()
        sql = '''SELECT * FROM ''' + DG.kitDatabase + ''' WHERE barcode = %s UNION
                SELECT * FROM ''' + DG.rmaDatabase + ''' WHERE barcode = %s UNION
                SELECT * FROM ''' + DG.buildDatabase + ''' WHERE barcode = %s;'''
        cur.execute(sql, [barcodeCheck, barcodeCheck, barcodeCheck])
        barcodeRecords = cur.fetchall()
        if(len(barcodeRecords) > 1):
            tk.messagebox.showerror("Error", "Multiple builds found with identical barcodes")
            return
        elif(barcodeRecords):
            buildListBox.delete(0, tk.END)
            buildListBox.insert(0, barcodeRecords[0][0])
        else:
            buildsList = []
            searchItem = '%' + searchBuild.get() + '%'
            buildListBox.delete(0, tk.END)
            sql = '''SELECT * FROM ''' + DG.kitDatabase + ''' WHERE name ILIKE %s UNION
                    SELECT * FROM ''' + DG.rmaDatabase + ''' WHERE name ILIKE %s UNION
                    SELECT * FROM ''' + DG.buildDatabase + ''' WHERE name ILIKE %s;'''
            cur.execute(sql, [searchItem, searchItem, searchItem])
            buildRecords = cur.fetchall()
            if(buildRecords):
                for build in buildRecords:
                    buildsList.append(build[0])
                buildsList.sort()
                for i in range(len(buildsList)):
                    buildListBox.insert(i, buildsList[i])
        return
    
    def deleteBuild():
        try:
            tableName = buildListBox.get(buildListBox.curselection())
        except:
            tk.messagebox.showerror("Error", "Must select item to delete", parent = viewBuildsWindow)
            return
        
        if(tableName[:4] == 'rma_'):
            database = DG.rmaDatabase
        elif(tableName[:6] == 'build_'):
            database = DG.buildDatabase
        elif(tableName[:4] == 'kit_'):
            database = DG.kitDatabase
        else:
            tk.messagebox.showerror("Error", "Issue processing information involved with specified build")
            return
        if(tableName[:4] == 'kit_'):
            sql = '''SELECT manufacturerid, barcode, quantity FROM ''' + tableName + ''';'''
            cur.execute(sql)
            fullBuildRecords = cur.fetchall()
            for record in fullBuildRecords:
                itemManID = record[0]
                itemBarcode = record[1]
                itemQuantity = record[2]
                found = False
                
                sql = '''SELECT quantity, barcode, kit FROM ''' + DG.invDatabase + ''' WHERE manufacturerid = %s;'''
                cur.execute(sql, [itemManID])
                manIDRecords = cur.fetchall()
                for manIDRecord in manIDRecords:
                    if(manIDRecord[2] == '0'):
                        invRecordQuantity = manIDRecord[0]
                        invRecordBarcode = manIDRecord[1]
                        newInventoryQuantity = itemQuantity + invRecordQuantity
                        sql = '''UPDATE ''' + DG.invDatabase + ''' SET quantity = %s WHERE barcode = %s;'''
                        cur.execute(sql, [newInventoryQuantity, invRecordBarcode])
                        found = True
                
                if(found == False):
                    # TODO 
                    # What should be done if an item is added directly to a kit but is not already in inventory and then the kit is deleted?
                    # Could do the whole locationList and addLocation page again
                    #
                    print("Figure it out")
                
                sql = '''DELETE FROM ''' + DG.invDatabase + ''' WHERE barcode = %s;'''
                cur.execute(sql, [itemBarcode])
                sql = '''DELETE FROM ''' + DG.locDatabase + ''' WHERE barcode = %s;'''
                cur.execute(sql, [itemBarcode])
                sql = '''DELETE FROM ''' + DG.barDatabase + ''' WHERE code = %s;'''
                cur.execute(sql, [itemBarcode])
        
        sql = '''SELECT barcode FROM ''' + database + ''' WHERE name = %s;'''
        cur.execute(sql, [tableName])
        barcode = cur.fetchall()
        
        sql = '''DELETE FROM ''' + database + ''' WHERE name = %s;'''
        cur.execute(sql, [tableName])
        sql = '''DELETE FROM ''' + DG.barDatabase + ''' WHERE code = %s; 
                DROP TABLE ''' + tableName + ''';'''
        cur.execute(sql, [barcode[0][0]])
        populateBuildListBox()
        wipeTree()
        buildNameLabel.config(text = '')
        tk.messagebox.showinfo("Success", "Build Deleted", parent = viewBuildsWindow)
        return
    
    def deleteBuildCheck():
        subWindow_x = str(viewBuildsWindow.winfo_x() + 100)
        subWindow_y = str(viewBuildsWindow.winfo_y() + 50)
        subWindowLoc = subWindow_x + "+" + subWindow_y
        deleteBuildCheckWindow = tk.Tk()
        deleteBuildCheckWindow.geometry("350x200+" + subWindowLoc)
        deleteBuildCheckWindow.title("Delete Build Check")
        deleteBuildCheckWindow.focus_force()
        try:
            tableName = buildListBox.get(buildListBox.curselection())
        except:
            tk.messagebox.showerror("Error", "Must select item to delete", parent = deleteBuildCheckWindow)
            return
        if(tableName[:4] == 'kit_'):
            deleteCheckString = 'All items in build will be returned to main inventory locations\nContinue?'
        else:
            deleteCheckString = 'Are you sure you want to delete this RMA/Build?\nAll items within will be removed'
        deleteCheckLabel = tk.Label(deleteBuildCheckWindow, text = deleteCheckString)
        yesButton = tk.Button(deleteBuildCheckWindow, text = 'Yes', command=lambda:[deleteBuildCheckWindow.destroy(), deleteBuild()])
        noButton = tk.Button(deleteBuildCheckWindow, text='No', command=lambda:[deleteBuildCheckWindow.destroy()])
        
        deleteCheckLabel.place(relx=.5, rely=.4, anchor='center')
        yesButton.place(relx=.65, rely=.7, anchor='center')
        noButton.place(relx=.35, rely=.7, anchor='center')
        
        return
    
    def newBuildHelper():
        subWindowLoc = childWindowLocation(viewBuildsWindow)
        bar = DG.createBarcode()
        createNewBuild(bar, subWindowLoc)
        return
    
    
    
    
    
    def completeBuild():
        currentBuild = buildNameLabel.cget("text")
        doubleCheck = tk.messagebox.askquestion("Caution", 'Build/RMA will be removed and only accessible from Admin screen\nAre you sure you want to continue?', parent = viewBuildsWindow)
        if(doubleCheck == 'yes'):
            if(currentBuild[:3] == 'rma'):
                database = DG.rmaDatabase
            elif(currentBuild[:5] == 'build'):
                database = DG.buildDatabase
            else:
                tk.messagebox.showerror("Error", "Couldn't get build type")
                return
            sql = '''UPDATE ''' + database + ''' SET userview = 0 WHERE name = %s;'''
            cur.execute(sql, [currentBuild])
            location = childWindowLocation(viewBuildsWindow)
            viewBuildsWindow.destroy()
            viewBuilds(location, None)
        return
    
    
    
    
    
    def buildSelection(event):
        try:
            tableName = buildListBox.get(buildListBox.curselection())
        except:
            return
        sql = '''SELECT * FROM ''' + tableName + ''' ORDER BY timeadded;'''
        cur.execute(sql)
        selectedBuildRecords = cur.fetchall()
        wipeTree()
    
        def fillBuildTree(rec):
            buildTree.insert("", 'end', values=(rec[0], rec[4], rec[5], rec[6], rec[8])) 
            return
        
        def getBuildType(currentBuild):
            if(currentBuild[:3] == 'kit'):
                buildType = 'Kit'
            elif(currentBuild[:3] == 'rma'):
                buildType = 'RMA'
            elif(currentBuild[:5] == 'build'):
                buildType = 'Build'
            else:
                buildType = None
            return buildType
        
        def printHelper():
            tableName = buildNameLabel.cget("text")
            if(tableName[:4] == "rma_"):
                database = DG.rmaDatabase
            elif(tableName[:6] == "build_"):
                database = DG.buildDatabase
            elif(tableName[:4] == "kit_"):
                database = DG.kitDatabase
            sql = '''SELECT barcode FROM ''' + database + ''' WHERE name = %s;'''
            cur.execute(sql, [tableName])
            barRecords = cur.fetchall()
            barcode = barRecords[0][0]
            PL.createBarcodeImage(tableName.upper(), barcode)
            PL.printBarcode()
            return
        
        def adjustBuildItemHelper(*args):
            selectedItemValueList = buildTree.item(buildTree.focus())['values']
            print(selectedItemValueList)
            currentBuild = buildNameLabel.cget("text")
            manID = str(selectedItemValueList[0])
            description = str(selectedItemValueList[1])
            if len(description) > 28:
                description = description[:28] + "..."
            kitQuantity = selectedItemValueList[2]
            barcode = str(selectedItemValueList[3])
            
            if len(barcode) < 12:
                for i in range(12-len(barcode)):
                    barcode = "0" + barcode
            print(barcode)
            subWindow_x = str(viewBuildsWindow.winfo_x() + 100)
            subWindow_y = str(viewBuildsWindow.winfo_y() + 50)
            subWindowLoc = subWindow_x + "+" + subWindow_y
            adjustBuildGUI = tk.Tk()
            adjustBuildGUI.geometry("500x300+" + subWindowLoc)
        
            # if(currentBuild[:3] == 'kit'):
            #     buildType = 'Kit'
            # elif(currentBuild[:3] == 'rma'):
            #     buildType = 'RMA'
            # elif(currentBuild[:5] == 'build'):
            #     buildType = 'Build'
            # else:
            buildType = getBuildType(currentBuild)
            if(buildType == None):
                tk.messagebox.showerror("Error", "Couldn't get build type", parent = adjustBuildGUI)
                adjustBuildGUI.destroy()
                return
            
            buildTypeWName = buildType + ': ' + currentBuild
            adjustBuildGUI.title("Adjust " + buildTypeWName)
            
            def submitBuildChanges():
                
                return
            
            def deleteBuildItem():
                
                return
            
            # sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE barcode = %s;'''
            # cur.execute(sql, [barcode])
            # invRecords = cur.fetchall()
            # #print(invRecords)
            # if(buildType == 'Kit'):
            #     for rec in invRecords:
            #         print(rec[8], " --- Current Build: ", currentBuild)
            #         if(rec[8] == currentBuild):
            #             currentItemBarcode = rec[6]
            # else:
            #     for rec in invRecords:
            #         print(rec[8])
            #         if(rec[8] == '0'):
            #             currentItemBarcode = rec[6]
            
            
            currentNameLabel = tk.Label(adjustBuildGUI, text = currentBuild, font=('calibre', 14, 'bold'))
            manIDLabel = tk.Label(adjustBuildGUI, text = "Man. #:", font=('calibre', 12, 'bold'))
            manIDPulledLabel = tk.Label(adjustBuildGUI, text = "", font=('calibre', 12))
            descriptionLabel = tk.Label(adjustBuildGUI, text = "Description:", font=('calibre', 12, 'bold'))
            descriptionPulledLabel = tk.Label(adjustBuildGUI, text = "", font=('calibre', 12))
            
            barcodeLabel = tk.Label(adjustBuildGUI, text = "Barcode:", font=('calibre', 12, 'bold'))
            barcodePulledLabel = tk.Label(adjustBuildGUI, text = "", font=('calibre', 12))
            quantityLabel = tk.Label(adjustBuildGUI, text = "Quantity:", font=('calibre', 12, 'bold'))
            quantityEntry = tk.Entry(adjustBuildGUI, width=10)
            submitButton = tk.Button(adjustBuildGUI, text='Submit', command=submitBuildChanges)
            deleteButton = tk.Button(adjustBuildGUI, text='Delete Item', command=deleteBuildItem)
            
            currentNameLabel.place(relx=.5, rely=.1, anchor='center')
            manIDLabel.place(relx=.35, rely=.3, anchor='e')
            manIDPulledLabel.place(relx=.4, rely=.3, anchor='w')
            descriptionLabel.place(relx=.35, rely=.45, anchor='e')
            descriptionPulledLabel.place(relx=.4, rely=.45, anchor='w')
            barcodeLabel.place(relx=.35, rely=.6, anchor='e')
            barcodePulledLabel.place(relx=.4, rely=.6, anchor='w')
            quantityLabel.place(relx=.35, rely=.75, anchor='e')
            quantityEntry.place(relx=.4, rely=.75, anchor='w')
            submitButton.place(relx=.35, rely=.9, anchor='center')
            deleteButton.place(relx=.65, rely=.9, anchor='center')
            
            manIDPulledLabel.configure(text=manID)
            barcodePulledLabel.configure(text=barcode)
            descriptionPulledLabel.configure(text=description)
            quantityEntry.insert(0, kitQuantity)
            quantityEntry.focus_force()
            
            return
        
        viewBuildsWindow.geometry("1000x300") 
        buildNameLabel.config(text = buildListBox.get(buildListBox.curselection()))
        
        printCodeButton = tk.Button(viewBuildsWindow, text = "Print Barcode", command = printHelper)
        searchLabel.place(relx=.045, rely=.2, anchor = 'w')
        searchEntry.place(relx=.105, rely=.2, anchor='w')
        buildNameLabel.place(relx=.65, rely=.06, anchor='center')
        buildListBox.place(relx=.06, rely=.5, anchor='w')
        buildScrollbar.place(in_=buildListBox, relheight = 1.0, relx=.92, rely=.5, anchor='w')
        newBuildButton.place(relx=.152, rely=.78, anchor='w')
        editBuildButton.place(relx=.38, rely=.92, anchor='center')
        printCodeButton.place(relx=.8, rely = .92, anchor='center')
        homeButton.place(relx = .925, rely=.92, anchor = 'center')
        
        if(callLocation == 'Admin'):
            deleteBuildButton.place(relx=.075, rely=.78, anchor='center')
            refreshButton.place(relx=.188, rely=.85, anchor='center')
        else:
            refreshButton.place(relx=.06, rely=.78, anchor='center')
        
        finishBuildButton.place_forget()
        buildType = getBuildType(tableName)
        if(buildType == 'Build' or buildType == 'RMA'):
            finishBuildButton.place(relx=.655, rely=.92, anchor='center')
        
        
        buildTree.place(relx=.65, rely=.475, anchor = 'center')
        buildTreeScrollbar.place(in_=buildTree, relheight = .9, relx=.98, rely=.5, anchor = 'center')
        
        for rec in selectedBuildRecords:    
            fillBuildTree(rec)

        buildTree.bind('<Double-1>', adjustBuildItemHelper)

        return
    
    searchBuild = tk.StringVar(viewBuildsWindow)
    searchLabel = tk.Label(viewBuildsWindow, text = "Search: ")
    searchEntry = tk.Entry(viewBuildsWindow, textvariable=searchBuild)
    buildListBox = tk.Listbox(viewBuildsWindow, width=30, height=8, selectmode = 'single')
    buildScrollbar = tk.Scrollbar(viewBuildsWindow, command=buildListBox.yview)
    buildListBox.config(yscrollcommand=buildScrollbar.set)
    buildNameLabel = tk.Label(viewBuildsWindow, text = '', font=('calibre', 12, 'bold'))
    deleteBuildButton = tk.Button(viewBuildsWindow, text='Delete Kit', command=deleteBuildCheck)
    finishBuildButton = tk.Button(viewBuildsWindow, text='Complete Build', command=completeBuild)
    editBuildButton = tk.Button(viewBuildsWindow, text='Add Items', command= lambda: [editBuild()])
    refreshButton = tk.Button(viewBuildsWindow, text='Refresh List', command=populateBuildListBox)
    newBuildButton = tk.Button(viewBuildsWindow, text = 'New Kit/Build/RMA', command=newBuildHelper)
    homeButton = tk.Button(viewBuildsWindow, text = "Home", command=returnHelper)
    
    buildTree = ttk.Treeview(viewBuildsWindow, selectmode = 'browse')
    buildTreeScrollbar = tk.Scrollbar(viewBuildsWindow, orient='vertical', command=buildTree.yview)
    buildTree.configure(yscrollcommand = buildTreeScrollbar.set)
    buildTree["columns"] = ("1", "2", "3", "4", "5")
    buildTree['show'] = 'headings' 
    buildTree.column("1", width = 100, anchor = 'w')
    buildTree.column("2", width = 200, anchor = 'w')
    buildTree.column("3", width = 60, anchor = 'w')
    buildTree.column("4", width = 100, anchor = 'w')
    buildTree.column("4", width = 130, anchor = 'w')
    buildTree.heading("1", text = "Manufacturer #")
    buildTree.heading("2", text = "Description")
    buildTree.heading("3", text = "Quantity")
    buildTree.heading("4", text = "Barcode")
    buildTree.heading("5", text = "Time added")
    
    searchBuild.trace_add('write', buildSearch)

    searchLabel.place(relx=.15, rely=.2, anchor = 'w')
    searchEntry.place(relx=.35, rely=.2, anchor='w')
    buildListBox.place(relx=.2, rely=.5, anchor='w')
    buildScrollbar.place(in_=buildListBox, relheight = 1.0, relx=.92, rely=.5, anchor='w')
    newBuildButton.place(relx=.697, rely=.78, anchor='center')
    homeButton.place(relx=.8, rely=.92, anchor = 'w')
    
    if(callLocation == 'Admin'):
        deleteBuildButton.place(relx=.2, rely=.78, anchor='center')
        refreshButton.place(relx=.5, rely=.85, anchor='center')    
    else:
        refreshButton.place(relx=.2, rely=.78, anchor='center')
    
    populateBuildListBox()
    
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

def createNewBuild(bar, location):
    cur = DG.conn.cursor()
    newBuildWindow = tk.Tk()
    newBuildWindow.title("New Build")
    newBuildWindow.geometry("400x200+" + location)
    
    buildType = tk.StringVar(newBuildWindow)
    buildNumber = tk.StringVar()
    buildLabel = tk.Label(newBuildWindow, text='RMA Number: ')
    
    def buildBoxChange(*args):
        if(buildChoiceBox.get() == 'RMA'):
            buildLabel.config(text="RMA Number: ")
        elif(buildChoiceBox.get() == 'Build'):
            buildLabel.config(text='Build Name: ')
        else:
            buildLabel.config(text="Name of Kit: ")
        return
    
    def createBuild():
        if(buildEntry.get()):
            buildName = str(buildEntry.get())
            buildName = buildName.replace("-", "_")
        else:
            tk.messagebox.showerror("Error", "Please enter a build label")
            return
        
        if(buildChoiceBox.get() == 'Kit'):
            tableVar = 'Kit_'
        elif(buildChoiceBox.get() == 'Build'):
            tableVar = 'Build_'
        else:
            tableVar = 'RMA_'
        tableName = tableVar + buildName
        
        # Check to make sure table doesn't already exist
        sql = '''SELECT * FROM ''' + DG.kitDatabase + ''' WHERE name = %s 
                UNION SELECT * FROM ''' + DG.rmaDatabase + ''' WHERE name = %s 
                UNION SELECT * FROM ''' + DG.buildDatabase + ''' WHERE name = %s;'''
        cur.execute(sql, [tableName.lower(), tableName.lower(), tableName.lower()])
        buildRecords = cur.fetchall()
        if(buildRecords):
            tk.messagebox.showerror("Error", "Build already exists in database", parent = newBuildWindow)
        else:
            if(tableVar == 'Kit_'):
                sql = '''INSERT INTO ''' + DG.kitDatabase + ''' (name, barcode, userview) VALUES (%s, %s, %s);'''
                cur.execute(sql, [tableName.lower(), bar, 1])
            elif(tableVar == 'RMA_'):
                sql = '''INSERT INTO ''' + DG.rmaDatabase + ''' (name, barcode, userview) VALUES (%s, %s, %s);'''
                cur.execute(sql, [tableName.lower(), bar, 1])
            elif(tableVar == 'Build_'):
                sql = '''INSERT INTO ''' + DG.buildDatabase + ''' (name, barcode, userview) VALUES (%s, %s, %s);'''
                cur.execute(sql, [tableName.lower(), bar, 1])
                
            sql = '''INSERT INTO ''' + DG.barDatabase + '''(code) VALUES (%s);'''
            cur.execute(sql, [bar])
                        
            sql = '''CREATE TABLE IF NOT EXISTS ''' + tableName + ''' (
                        ManufacturerID VARCHAR(100),
                        Manufacturer VARCHAR(100),
                        SupplierPartNum VARCHAR(100),
                        Supplier VARCHAR(100),
                        Description VARCHAR(1000),
                        Quantity INT,
                        Barcode VARCHAR(100),
                        username VARCHAR(100),
                        timeadded VARCHAR(100),
                        BOM_ID SMALLINT);'''
            cur.execute(sql)
            infoMessage = tableName + " Created succesfully"
            tk.messagebox.showinfo("Success", infoMessage, parent=newBuildWindow)
            PL.createBarcodeImage(tableName.upper(), bar)
            PL.printBarcode() 
        return

    
    def createBuildHelper():
        createBuild()
        newBuildWindow.destroy()
        return
  
    
  
    buildType.trace_add('write', buildBoxChange)
    choiceList = ['RMA', 'Kit', 'Build']
    buildChoiceBox = ttk.Combobox(
                        newBuildWindow,
                        state='readonly',
                        values = choiceList,
                        textvar = buildType
                        )
    buildChoiceBox.set('RMA')
    buildChoiceBox.place(relx=.5, rely=.3, anchor='center')

    buildEntry = tk.Entry(newBuildWindow, textvariable = buildNumber)
    buildEntry.focus_force()
    #buildEntry.bind('<Return>', createBuildHelper)
    createButton = tk.Button(newBuildWindow, text = 'Create', command = createBuildHelper)
    barcodeLabel = tk.Label(newBuildWindow, text='')
    buildEntry.bind('<Return>', lambda e: createBuildHelper())
    
    buildLabel.place(relx=.3, rely = .5, anchor = 'center')
    buildEntry.place(relx=.6, rely=.5, anchor = 'center')
    createButton.place(relx=.5, rely=.7, anchor='center')
    barcodeLabel.place(relx=.5, rely=.9, anchor='center')
    
    newBuildWindow.mainloop()
    return

def checkOut(buildBarcode, location, callLocation):
    checkOutWindow = tk.Tk()
    checkOutWindow.title("Check Out")
    checkOutWindow.geometry("800x400+" + location)
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
            tk.messagebox.showerror("Error", "Item not currently in system", parent = checkOutWindow)
            return
        
        if(buildBarcode != None):
            sql = '''SELECT name FROM ''' + DG.kitDatabase + ''' WHERE barcode = %s;'''
            cur.execute(sql, [buildBarcode])
            buildRecords = cur.fetchall()
            if(buildRecords):
                sql = '''SELECT * FROM ''' + buildRecords[0][0] + ''' WHERE barcode = %s;'''
                cur.execute(sql, [barEntry.get()])
                itemAlreadyInBuildRecords = cur.fetchall()
                if(itemAlreadyInBuildRecords):
                    tk.messagebox.showerror("Error", "Trying to pull and add identical item to build", parent = checkOutWindow)
                    barEntry.delete(0, tk.END)
                    itemQuantityEntry.delete(0, tk.END)
                    barEntry.focus()
                    return
        # if(records[0][8] != '0'):
        #     tk.messagebox.showerror("Error", "Adding items from one kit to another is not permitted", parent = checkOutWindow)
        #     barEntry.delete(0,tk.END)
        #     barEntry.focus_force()
        #     return
        
        # Check previously added items for duplicates
        for line in checkOutTree.get_children():
            barcode = str(checkOutTree.item(line).get('values')[2])
            if(len(barcode) < 12):
                zeroCount = 12 - len(barcode)
                for i in range(zeroCount):
                    barcode = "0" + barcode
            if(barcode == barEntry.get()):
                errorMessage = 'Item: "' + str(checkOutTree.item(line).get('values')[1]) + '" already in list'
                tk.messagebox.showerror("Error", errorMessage, parent = checkOutWindow)
                itemQuantityEntry.delete(0, tk.END)
                barEntry.delete(0,tk.END)
                barEntry.focus_force()
                return
            
        # If user didn't enter a quantity, just assign quantity of 1
        if(itemQuantityEntry.get() == ""):
            quantity = 1
        else:
            # This hasn't been checked but I don't see why adding .strip() would affect anything negatively
            quantity = itemQuantityEntry.get().strip()
        
        # Check to make sure that quantity is available in database
        if(not quantityCheck(barEntry.get(), quantity)):
            errorMessage = 'Less than ' + str(quantity) + ' "' + records[0][4] + '" available in database'
            tk.messagebox.showerror("Error", errorMessage, parent = checkOutWindow)
            barEntry.delete(0, tk.END)
            itemQuantityEntry.delete(0, tk.END)
            barEntry.focus_force()
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
    
    def editItem(*args):
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
                tk.messagebox.showerror("Error", errorMessage, parent = checkOutWindow)
            return
        
        returnButton = tk.Button(editItemWindow, text = 'Return', command = editItemWindow.destroy)
        finalizeButton = tk.Button(editItemWindow, text = 'Finalize', command = lambda:[finalizeEdit(), editItemWindow.destroy()])
        manIDLabel = tk.Label(editItemWindow, text = 'Manufacturer #:', font = ('calibre', 12))
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
        
        quantityEntry.bind('<Return>', lambda e: [finalizeEdit(), editItemWindow.destroy()])
        editItemWindow.mainloop()
        return
    
    def completeOrderGUI(location):
        receiptScreen = tk.Tk() 
        receiptScreen.title("Check Out Finalization")
        receiptScreen.geometry("400x200+" + location)

        def finalizeCheckout(buildBar):
            sql = '''SELECT * FROM ''' + DG.rmaDatabase + ''' WHERE barcode = %s UNION
                    SELECT * FROM ''' + DG.kitDatabase + ''' WHERE barcode = %s UNION 
                    SELECT * FROM ''' + DG.buildDatabase + ''' WHERE barcode = %s;'''
            cur.execute(sql, [buildBar, buildBar, buildBar])
            buildRecords = cur.fetchall()
            if(buildRecords):
                buildName = buildRecords[0][0]
                kitList = []
                sql = '''SELECT * FROM ''' + buildName + ''';'''
                cur.execute(sql)
                currentBuildRecords = cur.fetchall()
                if(currentBuildRecords):
                    for currentItem in currentBuildRecords:
                        kitList.append(currentItem[0])
                        
                # Adjust when/if you want to add user to checkout
                username = None
                timeVar = datetime.now()
                currentTime = timeVar.strftime("%m-%d-%Y %H:%M:%S")
                # THIS NEEDS TO BE FINISHED
                if(buildName[:4] == "kit_"):
                    #barEntry = tk.Entry()
                    #checkDigitLabel = tk.Label()
                    newLocationsList = []
                    quantityUpdateCheck = False
                                
                    for line in checkOutTree.get_children():
                        if(line):
                            manID = checkOutTree.item(line).get('values')[0]
                            itemCode = str(checkOutTree.item(line).get('values')[2])
                            if(len(itemCode) < 12):
                                zeroCount = 12 - len(itemCode)
                                for i in range(zeroCount):
                                    itemCode = "0" + itemCode
                            checkOutQuantity = checkOutTree.item(line).get('values')[3]
                            
                            sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE barcode = %s;'''
                            cur.execute(sql, [str(itemCode)])
                            itemRecords = cur.fetchall()
                            # In case of Confusion:
                                # itemCode == itemRecords[0][6]
                                # manID == itemRecords[0][0]
                            
                            ## kitList is a list of the manufacturerid's present in the build
                            # kitList = []
                            # sql = '''SELECT * FROM ''' + buildName + ''';'''
                            # cur.execute(sql)
                            # currentBuildRecords = cur.fetchall()
                            
                            # May want to add in a safety here in case somehow the build records are not present
                            
                            # for currentItem in currentBuildRecords:
                            #     kitList.append(currentItem[0])
                            if(manID in kitList):
                                # This statement and the one pulling the barcode below can probably be combined
                                sql = '''SELECT quantity FROM ''' + buildName + ''' WHERE manufacturerid = %s;'''
                                cur.execute(sql, [manID])
                                kitQuantityRecords = cur.fetchall()
                                
                                # kitQuantityRecords is the full records of quantity in the kit (should only contain one item)
                                # checkOutQuantity is the quantity in the checkOutTree associated with the manID
                                newBuildQuantity = kitQuantityRecords[0][0] + checkOutQuantity
                                #print('New: ' + str(newBuildQuantity), 'Old: ' + str(kitQuantityRecords[0][0]), 'CheckOut: ' + str(checkOutQuantity))
                                sql = '''UPDATE ''' + buildName + ''' SET quantity = %s WHERE manufacturerid = %s;'''
                                cur.execute(sql, [newBuildQuantity, manID])
                                
                                sql = '''SELECT barcode FROM ''' + buildName + ''' WHERE manufacturerid = %s;'''
                                cur.execute(sql, [manID])
                                kitItemBarcodeRecords = cur.fetchall()
                                kitItemBarcode = kitItemBarcodeRecords[0][0]
                                
                                sql = '''UPDATE ''' + DG.invDatabase + ''' SET quantity = %s WHERE barcode = %s;'''
                                cur.execute(sql, [newBuildQuantity, kitItemBarcode])
                                
                                quantityUpdateCheck = True
                                
                            # This whole chunk runs if the item is NOT already found in the kit   
                            else:
                                newItemBarcode = DG.createBarcode()
                                sql = '''INSERT INTO ''' + DG.barDatabase + ''' (code) VALUES (%s); END'''
                                cur.execute(sql, [newItemBarcode])
                                
                                sql = '''INSERT INTO ''' + buildName + ''' (ManufacturerID, Manufacturer, SupplierPartNum, Supplier, Description, Quantity, Barcode, username, timeadded, BOM_ID)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                                cur.execute(sql, [itemRecords[0][0], itemRecords[0][1], itemRecords[0][2], itemRecords[0][3], itemRecords[0][4], checkOutQuantity, newItemBarcode, username, None, itemRecords[0][7]])
                                
                                sql = '''INSERT INTO ''' + DG.invDatabase + ''' (ManufacturerID, Manufacturer, SupplierPartNum, Supplier, Description, Quantity, Barcode, bom_id, kit)
                                        SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s'''
                                cur.execute(sql, [itemRecords[0][0], itemRecords[0][1], itemRecords[0][2], itemRecords[0][3], itemRecords[0][4], checkOutQuantity, newItemBarcode, itemRecords[0][7], buildName])             
                                
                                sql = '''INSERT INTO ''' + DG.locDatabase + ''' (Room, Rack, Shelf, Shelf_Location, Barcode) VALUES (%s, %s, %s, %s, %s);'''
                                cur.execute(sql, [None, None, None, None, newItemBarcode])
                                
                                newLocationsList.append([itemRecords[0][0], newItemBarcode, checkOutQuantity, None])
                            
                            if(itemRecords):
                                quantity = itemRecords[0][5] - checkOutQuantity                                
                                sql = '''UPDATE ''' + DG.invDatabase + ''' SET quantity = %s WHERE barcode = %s;'''
                                cur.execute(sql, [quantity, str(itemCode)])
                                
                                sql = '''SELECT kit FROM ''' + DG.invDatabase + ''' WHERE barcode = %s;'''
                                cur.execute(sql, [itemCode])
                                kitRecords = cur.fetchall()
                                #quantity = kitRecords[0][0]
                                kit = kitRecords[0][0]
                                #print(kit, quantity, itemCode)
                                if(kit != '0'):
                                    sql = '''UPDATE ''' + kit + ''' SET quantity = %s WHERE barcode = %s;'''
                                    cur.execute(sql, [quantity, str(itemCode)])
                                
                    if(quantityUpdateCheck):
                        tk.messagebox.showinfo("Success", "Quantites of items previously in kit updated", parent = checkOutWindow) 
                            
                    if (len(newLocationsList) > 0):         
                        def editLocation(*args):
                            #cur = DG.conn.cursor()     
                            #loc is the location within newLocationsTree, it's only used to pull the selectedItemList
                            try:
                                loc = newLocationsTree.selection()[0]
                            except:
                                if(len(newLocationsTree.get_children()) > 1):
                                    tk.messagebox.showerror("Error", "Select item to edit location", parent = newLocationsWindow)
                                    return
                                else:
                                    loc = newLocationsTree.get_children()[0]
                            selectedItemList = newLocationsTree.item(loc)['values']
                            barcode = str(selectedItemList[1])
                            manID = str(selectedItemList[0])

                            subWindowLoc = childWindowLocation(newLocationsWindow)
                            specifiedRoom = tk.StringVar()
                            
                            def submitLocation():
                                newItemRoom = roomComboBox.get()
                                newItemRack = ord(rackEntry.get().upper())
                                newItemShelf = shelfEntry.get()
                                
                                sql = '''UPDATE ''' + DG.locDatabase + ''' 
                                        SET room = %s, 
                                        rack = %s, 
                                        shelf = %s 
                                        WHERE barcode = %s; END'''
                                cur.execute(sql, [newItemRoom, newItemRack, newItemShelf, barcode])
                                
                                sql = '''SELECT * FROM ssg_locations WHERE barcode = %s;'''
                                cur.execute(sql, [barcode])
                                locationRecords = cur.fetchall()
                                currentLocation = locationRecords[0][0] + " " + chr(locationRecords[0][1]) + '-' + str(locationRecords[0][2])
                                
                                labelText = str(selectedItemList[0]).lower()
                                labelText = labelText + " " + currentLocation
                                # locationRecords[0][4] is the barcode
                                PL.createBarcodeImage(labelText, locationRecords[0][4])
                                PL.printBarcode()
                                
                                newLocationsTree.item(loc, values = (selectedItemList[0], selectedItemList[1], selectedItemList[2], currentLocation))
                                adjustLocationWindow.destroy()
                                return
                                                        
                            adjustLocationWindow = tk.Tk()
                            adjustLocationWindow.geometry("300x300+" + subWindowLoc)
                            adjustLocationWindow.title("Adjust Location")
                            
                            itemName = manID + "\n" + buildName
                            itemNameLabel = tk.Label(adjustLocationWindow, text = itemName, font = ('calibre', 12))
                            roomLabel = tk.Label(adjustLocationWindow, text = 'Room:')
                            rackLabel  = tk.Label(adjustLocationWindow, text = 'Rack:')
                            shelfLabel = tk.Label(adjustLocationWindow, text = 'Rack:')
                            
                            roomList = []
                            sql = '''SELECT DISTINCT room FROM ''' + DG.locDatabase + ''';''';
                            cur.execute(sql)
                            roomRecords = cur.fetchall()
                            for room in roomRecords:
                                if(room[0] != ""):
                                    roomList.append(room[0])
                            roomComboBox = ttk.Combobox(adjustLocationWindow, state='readonly', values = roomList, textvariable = specifiedRoom)
                            roomComboBox.set('Inventory')
                            rackEntry = tk.Entry(adjustLocationWindow)
                            shelfEntry = tk.Entry(adjustLocationWindow)
                            enterLocationButton = tk.Button(adjustLocationWindow, text='Submit', command=submitLocation)
                            rackEntry.bind('<Return>', lambda e: shelfEntry.focus_force())
                            shelfEntry.bind('<Return>', lambda e: submitLocation())
                            rackEntry.focus_force()
                            
                            itemNameLabel.place(relx=.5, rely=.15, anchor='center')
                            roomLabel.place(relx=.25, rely=.3, anchor='center')
                            rackLabel.place(relx=.25, rely=.5, anchor='center')
                            shelfLabel.place(relx=.25, rely=.7, anchor='center')
                            enterLocationButton.place(relx=.5, rely=.85, anchor='center')
                            
                            roomComboBox.place(relx=.6, rely=.3, anchor='center')
                            rackEntry.place(relx=.6, rely=.5, anchor='center')
                            shelfEntry.place(relx=.6, rely=.7, anchor='center')
                            
                            adjustLocationWindow.mainloop()
                            return

                        def submissionCheck():
                            emptyLocationsList = []
                            for line in newLocationsTree.get_children():
                                if((str(newLocationsTree.item(line).get('values')[3])) == 'None'):
                                    emptyLocationsList.append(newLocationsTree.item(line).get('values'))
                            if(emptyLocationsList):
                                #print(emptyLocationsList)
                                tk.messagebox.showerror("ERROR", "Please add a location to all items", parent = newLocationsWindow)
                            else:
                                tk.messagebox.showinfo("Success", "Items added into inventory in their new locations", parent = newLocationsWindow)
                                newLocationsWindow.destroy()
                                checkOutWindow.destroy()
                            #return

                        def exitHandler():
                            if(tk.messagebox.askokcancel("Are you sure?", "Items will be added in without locations", parent = newLocationsWindow)):
                                newLocationsWindow.destroy()
                                checkOutWindow.destroy()
                            return
    
                        subWindowLoc = childWindowLocation(checkOutWindow)
                        newLocationsWindow = tk.Tk()
                        newLocationsWindow.title("New Locations")
                        newLocationsWindow.geometry("500x350+" + subWindowLoc)
                        
                        newLocationsTree = ttk.Treeview(newLocationsWindow, selectmode='browse', height = 10)
                        newLocationsScrollbar = tk.Scrollbar(newLocationsWindow, orient='vertical', command = newLocationsTree.yview)
                        completeButton = tk.Button(newLocationsWindow, text='Finish', command=submissionCheck)
                        editItemButton = tk.Button(newLocationsWindow, text='Edit Item', command=editLocation)
                        
                        newLocationsTree.configure(yscrollcommand = newLocationsScrollbar.set)
                        newLocationsTree["columns"] = ("1", "2", "3", "4")
                        newLocationsTree['show'] = 'headings' 
                        newLocationsTree.column("1", width = 100, anchor = 'w')
                        newLocationsTree.column("2", width = 100, anchor = 'w')
                        newLocationsTree.column("3", width = 60, anchor = 'center')
                        newLocationsTree.column("4", width = 100, anchor = 'center')
                        newLocationsTree.heading("1", text = "Manufacturer #")
                        newLocationsTree.heading("2", text = "Barcode")
                        newLocationsTree.heading("3", text = "Quantity")
                        newLocationsTree.heading("4", text = "Location")
                        newLocationsTree.bind('<Double-1>', editLocation)
                        newLocationsTreeStyle = ttk.Style()
                        newLocationsTreeStyle.configure('Treeview.Heading', foreground='black')
                        
                        for location in newLocationsList:
                            newLocationsTree.insert("", 'end', values=(location[0], location[1], location[2], location[3],))
                        
                        newLocationsTree.place(relx=.5, rely=.4, anchor='center')
                        newLocationsScrollbar.place(relx=.84, rely=.4, anchor='center')
                        editItemButton.place(relx=.5, rely=.8, anchor='center')
                        completeButton.place(relx=.5, rely=.9, anchor='center')
                        newLocationsWindow.focus_force()
                        newLocationsWindow.protocol("WM_DELETE_WINDOW", exitHandler)
                        newLocationsWindow.mainloop()      
                        # return
                    else:
                        checkOutWindow.destroy()
                        
                if(buildName[:4] == "rma_" or buildName[:6] == "build_"):
                    #print(buildName)
                    for line in checkOutTree.get_children(): 
                        if(line):
                            manID = checkOutTree.item(line).get('values')[0]
                            
                            # Pulling barcode here will cause issues with leading zeros
                            itemCode = str(checkOutTree.item(line).get('values')[2])
                            if(len(itemCode) < 12):
                                zeroCount = 12 - len(itemCode)
                                for i in range(zeroCount):
                                    itemCode = "0" + itemCode
                            checkOutQuantity = checkOutTree.item(line).get('values')[3]
                            sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE barcode = %s;'''
                            cur.execute(sql, [str(itemCode)])
                            itemRecords = cur.fetchall()
                            sql = '''INSERT INTO ''' + buildName + ''' (ManufacturerID, Manufacturer, SupplierPartNum, Supplier, Description, Quantity, Barcode, username, timeadded, BOM_ID)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                            cur.execute(sql, [itemRecords[0][0], itemRecords[0][1], itemRecords[0][2], itemRecords[0][3], itemRecords[0][4], checkOutQuantity, itemRecords[0][6], username, currentTime, itemRecords[0][7]])
                
                            newInvQuantity = itemRecords[0][5] - checkOutQuantity
                            sql = '''UPDATE ''' + DG.invDatabase + ''' SET quantity = %s WHERE barcode = %s;'''
                            cur.execute(sql, [newInvQuantity, str(itemCode)])
                            
                            if(itemRecords[0][8] != '0'):
                                currentBuildName = itemRecords[0][8]
                                
                                # sql = '''SELECT quantity from ''' + buildName + ''' WHERE barcode = %s;'''
                                # cur.execute(sql, [str(itemCode)])
                                # buildQuantityRecords = cur.fetchall()
                                # buildQuantity_prior = buildQuantityRecords[0][0]
                                # newBuildQuantity = buildQuantity_prior - checkOutQuantity
                                
                                # sql = '''UPDATE ''' + currentBuildName + ''' SET quantity = %s WHERE barcode = %s;'''
                                # cur.execute(sql, [newBuildQuantity, str(itemCode)])
                                sql = '''SELECT quantity from ''' + DG.invDatabase + ''' WHERE barcode = %s;'''
                                cur.execute(sql, [str(itemCode)])
                                currentItemUpdatedInvQuantityRecords = cur.fetchall()
                                sql = '''UPDATE ''' + currentBuildName + ''' SET quantity = %s WHERE barcode = %s;'''
                                cur.execute(sql, [currentItemUpdatedInvQuantityRecords[0][0] , str(itemCode)])
  
                    tk.messagebox.showinfo("Success", "Items checked out of inventory", parent = checkOutWindow)
                    checkOutWindow.destroy()

            else:
                tk.messagebox.showerror("Error", 'Build/RMA not found')
                buildBarEntry.focus_force()
                buildBarEntry.delete(0, tk.END)

            return
        
        
        def finalizeCheckoutHelper():
            barcode = buildBarEntry.get()
            # subWindow_x = str(receiptScreen.winfo_x() + 100)
            # subWindow_y = str(receiptScreen.winfo_y() + 50)
            # subWindowLoc = subWindow_x + "+" + subWindow_y
            receiptScreen.destroy()
            finalizeCheckout(barcode)
            return
        
        def newBuildHelper():
            subWindow_x = str(receiptScreen.winfo_x() + 100)
            subWindow_y = str(receiptScreen.winfo_y() + 50)
            subWindowLoc = subWindow_x + "+" + subWindow_y
            #receiptScreen.destroy()
            #bar = createNewBuild(checkOutWindow, subWindowLoc)
            bar = DG.createBarcode()
            #checkOutWindow.destroy()
            createNewBuild(bar, subWindowLoc)
            #finalizeCheckout(bar)
            return
        
        buildBarLabel = tk.Label(receiptScreen, text = "Build Barcode:", font = ('calibre', 12))
        buildBarEntry = tk.Entry(receiptScreen, width = 20)

        buildBarEntry.focus_force()
        finalizeOrderButton = tk.Button(receiptScreen, text = "Checkout Items", command = finalizeCheckoutHelper)
        
        orLabel = tk.Label(receiptScreen, text = "Or", font = ('calibre', 12))
        newBuildButton = tk.Button(receiptScreen, text = "Create New Build", command=newBuildHelper)
        buildBarLabel.place(relx = .2, rely=.4, anchor='center')
        buildBarEntry.place(relx=.5, rely=.4, anchor = 'center')
        finalizeOrderButton.place(relx=.82, rely = .4, anchor='center')
        orLabel.place(relx=.5, rely=.6, anchor='center')
        newBuildButton.place(relx=.5, rely=.75, anchor='center')
        
        if buildBarcode:
            buildBarEntry.insert(0, buildBarcode)
            finalizeCheckoutHelper()
        
        receiptScreen.mainloop()
        return
    
    def completeOrderHelper():
        count = 0
        subWindowLoc = childWindowLocation(checkOutWindow)
        for line in checkOutTree.get_children():
            count += 1
        # if(count == 0):
        #     tk.messagebox.showerror('Error', 'Please enter the items you wis)h to check out')
        completeOrderGUI(subWindowLoc)
        return
    
    def returnHelper():
        try:
            if(mainMenuWindow.winfo_exists()):
                checkOutWindow.destroy()
                mainMenuWindow.focus_force()
        except:
            checkOutWindow.destroy()
            mainMenu()
        return
    
    
    #barEntryCombobox =
    barEntryLabel = tk.Label(checkOutWindow, text = 'Barcode:', font = ('calibre', 12))
    quantityLabel = tk.Label(checkOutWindow, text = 'Quantity:', font = ('calibre', 12))
    barEntry = tk.Entry(checkOutWindow, width = 30)
    itemQuantityEntry = tk.Entry(checkOutWindow, width = 5)
    checkOutTree = ttk.Treeview(checkOutWindow, selectmode = 'browse')
    checkOutScrollbar = tk.Scrollbar(checkOutWindow, orient='vertical', command = checkOutTree.yview)
    addItemButton = tk.Button(checkOutWindow, text = 'Add Item', command = addItem)
    editItemButton = tk.Button(checkOutWindow, text = "Edit Item", command = editItem)
    removeItemButton = tk.Button(checkOutWindow, text = 'Delete Item', command = removeItem)
    completeOrderButton = tk.Button(checkOutWindow, text = 'Complete Order', command = completeOrderHelper)
    homeButton = tk.Button(checkOutWindow, text = "Home", command = returnHelper)
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
    
    checkOutTree.bind('<Double-1>', editItem)
    checkOutWindow.mainloop()
    
    return

def adminLogin(location):
    adminLoginWindow = tk.Tk()
    adminLoginWindow.title("Admin Login")
    adminLoginWindow.geometry("400x200+" + location)
    userPass = tk.StringVar()
    
    def loginCheck():
        password = b'$2b$12$STTqL.4AVbfd9eY3YFrl8uSsBaYdL8mupGcdRQRGmE7AH0h0Ag9am'
        userPass = passEntry.get()
        passBytes = userPass.encode('utf-8')
        #passHash = bcrypt.hashpw(passBytes, bcrypt.gensalt())
        if bcrypt.checkpw(passBytes, password): 
            subWindowLoc = childWindowLocation(adminLoginWindow)
            adminLoginWindow.destroy()
            Admin(subWindowLoc)
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
    
    adminLoginWindow.mainloop()
    return

def Admin(location):
    adminMenuWindow = tk.Tk()
    adminMenuWindow.title("Admin Menu")
    adminMenuWindow.geometry("600x400+" + location)
    adminMenuWindow.focus_force()
    
    
    # TODO
    # Double check that all of this is calling the typical build menu and then remove if unecessary 
    
    #Function definitions for Admin Menu Items
    # def adminBuildMenu():
    #     cur = DG.conn.cursor()
    #     adminBuildMenuWindow = tk.Tk()
    #     adminBuildMenuWindow.geometry("400x200")
    #     adminBuildMenuWindow.title("Build Menu (Admin)")
    #     adminBuildMenuWindow.focus_force()
        
    #     def buildSelectionAdmin(*args):
    #         adminBuildMenu = tk.Tk()
    #         #print("X: ", adminBuildMenuWindow.winfo_x(), "Y: ", adminBuildMenuWindow.winfo_y())
    #         subWindow_x = str(adminBuildMenuWindow.winfo_x() + 100)
    #         subWindow_y = str(adminBuildMenuWindow.winfo_y() + 50)
    #         windowPosition = subWindow_x + "+" + subWindow_y
    #         adminBuildMenu.geometry("600x350" + "+" + windowPosition)
    #         buildName = buildListBox.get(buildListBox.curselection())
    #         adminBuildMenu.title(buildName)
    #         adminBuildMenu.focus_force()
            
    #         def fillBuildTree(rec):
    #             buildTree.insert("", 'end', values=(rec[0], rec[4], rec[5], rec[8])) 
    #             return
            
    #         #copy code from DELETE BUILD in main user menu
    #         def deleteBuild():
    #             print('Delete Build ' + buildName)
    #             return
            
    #         sql = '''SELECT * FROM ''' + buildName + ''' ORDER BY timeadded;'''
    #         cur.execute(sql)
    #         selectedBuildRecords = cur.fetchall()
            
    #         buildNameLabel = tk.Label(adminBuildMenu, text = buildName, font = ('calibre', 12, 'bold'))
    #         buildTree = ttk.Treeview(adminBuildMenu, selectmode = 'browse')
    #         buildTreeScrollbar = tk.Scrollbar(adminBuildMenu, orient='vertical', command = buildTree.yview)
    #         deleteBuildButton = tk.Button(adminBuildMenu, text='Delete Build', command = deleteBuild)
            
    #         buildNameLabel.place(relx=.5, rely=.07, anchor='center')
    #         buildTree.place(relx=.5, rely=.45, anchor = 'center')
    #         buildTreeScrollbar.place(relx=.89, rely=.45, anchor = 'center')
    #         deleteBuildButton.place(relx=.75, rely=.9, anchor='center')
            
    #         buildTree.configure(yscrollcommand = buildTreeScrollbar.set)
    #         buildTree["columns"] = ("1", "2", "3", "4")
    #         buildTree['show'] = 'headings' 
    #         buildTree.column("1", width = 100, anchor = 'w')
    #         buildTree.column("2", width = 200, anchor = 'w')
    #         buildTree.column("3", width = 60, anchor = 'w')
    #         buildTree.column("4", width = 130, anchor = 'w')
    #         buildTree.heading("1", text = "Manufacturer #")
    #         buildTree.heading("2", text = "Description")
    #         buildTree.heading("3", text = "Quantity")
    #         buildTree.heading("4", text = "Time added")
    #         for rec in selectedBuildRecords:    
    #             fillBuildTree(rec)
            
    #         adminBuildMenu.mainloop()
    #         return

    #     buildListBox = tk.Listbox(adminBuildMenuWindow, width=30, height=8, selectmode = 'single')
    #     buildScrollbar = tk.Scrollbar(adminBuildMenuWindow)
    #     returnButton = tk.Button(adminBuildMenuWindow, text = "Return", command = lambda:[adminBuildMenuWindow.destroy(), adminMenu()])

    #     sql = '''SELECT name FROM ''' + DG.rmaDatabase + ''' UNION SELECT name FROM ''' + DG.kitDatabase + ''' UNION SELECT name FROM ''' + DG.buildDatabase + ''';'''
    #     cur.execute(sql)
    #     buildNameRecords = cur.fetchall()
        
    #     buildListBox.place(relx=.5, rely=.4, anchor='center')
    #     buildScrollbar.place(relx=.7, rely=.4, anchor='center')
    #     buildListBox.config(yscrollcommand = buildScrollbar.set)
    #     buildListBox.bind('<Double-1>', buildSelectionAdmin)
        
    #     if(buildNameRecords):
    #         buildsList = []
    #         for name in buildNameRecords:
    #             buildsList.append(name[0])
    #         buildsList.sort()
    #         for i in range(len(buildsList)):
    #             buildListBox.insert(i, buildsList[i])
        
    #     returnButton.place(relx=.8, rely=.85, anchor = 'center')
    #     adminBuildMenuWindow.mainloop()
    #     return
        
    def adminBuildHelper():
        subWindowLoc = childWindowLocation(adminMenuWindow)
        adminMenuWindow.destroy()
        viewBuilds(subWindowLoc, 'Admin')
        return
    
    def createBOMGUI():
        bomWindow = tk.Tk()
        bomWindow.geometry("600x200")
        bomWindow.title("Bill of Materials")
        cur = DG.conn.cursor()
        
        def createBOMID():
            #Smallint can hold 32767, I'm assuming this is all we will need for the forseeable future
            bomID = random.randrange(0, 32750)
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
            
        def returnHelper():
            subWindowLoc = childWindowLocation(bomWindow)
            bomWindow.destroy()
            Admin(subWindowLoc)
            return
            
        nameLabel = tk.Label(bomWindow, text = "Select item to create/edit BOM")
        orLabel = tk.Label(bomWindow, text = "or", font = ('calibre', 12))
        bomEntryLabel = tk.Label(bomWindow, text = "Type Manufacturer Numbers for \nBOM inventory check")
        nameList = []
        itemName = tk.StringVar()
        sql = '''SELECT DISTINCT manufacturerid FROM ''' + DG.invDatabase + ''' ORDER BY manufacturerid'''
        cur.execute(sql)
        records = cur.fetchall()
        for record in records:
            nameList.append(record[0])
            
        #
        #This combobox needs to be placed in the bomwindow? I think? Don't have time to check right now
        bomChoiceBox = ttk.Combobox(state='readonly', values = nameList, textvariable = itemName)
        bomEntryBox = tk.Entry(bomWindow, width = 25)
        createBomButton = tk.Button(bomWindow, text = "Create", command=createBom)
        checkInventoryButton = tk.Button(bomWindow, text="Check Inventory", command=checkInventoryHelper)
        returnButton = tk.Button(bomWindow, text = 'Return', command = returnHelper)
        
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
    
    def inventoryBackup():
        tk.messagebox.showinfo("Alert", "Will create folders for year and month within selected directory.")
        saveFolder = filedialog.askdirectory()
        if(saveFolder):
            BU.createFile(saveFolder)
            messageDialog = "Database successfully backed up to:\n" + saveFolder
            tk.messagebox.showinfo("Success", messageDialog)
        return
    
    def removeItem():
        removeItemWindow = tk.Tk()
        removeItemWindow.geometry("600x150")
        removeItemWindow.title("Remove Item")
        removeVar = tk.StringVar()
        cur = DG.conn.cursor()
        
        def itemRemoval(bar_to_remove):
            sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE barcode = %s'''
            cur.execute(sql, [bar_to_remove])
            records = cur.fetchall()
            if(records):
                sql = '''DELETE FROM ''' + DG.invDatabase + ''' WHERE barcode = %s'''
                cur.execute(sql, [bar_to_remove])
                sql = '''DELETE FROM ''' + DG.locDatabase + ''' WHERE barcode = %s'''
                cur.execute(sql, [bar_to_remove])
                sql = '''DELETE FROM ''' + DG.barDatabase + ''' WHERE code = %s'''
                cur.execute(sql, [bar_to_remove])
                sql = '''SELECT name FROM ''' + DG.kitDatabase + ''' UNION SELECT name FROM ''' + DG.rmaDatabase + ''' UNION SELECT name FROM ''' + DG.buildDatabase + ''';'''
                cur.execute(sql)
                buildNames = cur.fetchall()
                if(buildNames):
                    for name in buildNames:
                        sql = '''DELETE FROM ''' + name[0] + ''' WHERE barcode = %s;'''
                        cur.execute(sql, [bar_to_remove])
                
                message = "Item:", records[0][0], "Barcode:", bar_to_remove, 'deleted'
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
                        removeTree.insert("", 'end', values=(record[0], record[4], record[6], record[5], record[8]))     #manID, name, barcode, quantity))
                    return
                
                def removeCheck():
                    #Double check that item should actually be removed
                    removeCheckWindow = tk.Tk()
                    removeCheckWindow.geometry("400x200")
                    removeCheckWindow.title("Are you sure?")
                    removeCheckWindow.focus_force()
                    
                    bar_to_remove = str(removeTree.item(removeTree.focus())['values'][2])
                    if(len(bar_to_remove) < 12):
                        zeroCount = 12 - len(bar_to_remove)
                        for i in range(zeroCount):
                            bar_to_remove = "0" + bar_to_remove
                    sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE barcode = %s;'''
                    cur.execute(sql, [bar_to_remove])
                    item_to_remove_records = cur.fetchall()
                    
                    removeText = "Are you sure you want to remove item:\n\nName:      " + item_to_remove_records[0][0] + "\nBarcode:   " + str(bar_to_remove) + "\nKit:     " + item_to_remove_records[0][8]
                    removeLabel = tk.Label(removeCheckWindow, text = removeText, font = ('calibre', 12))
                    yesButton = tk.Button(removeCheckWindow, text = "Yes", command = lambda: [itemRemoval(bar_to_remove), removeCheckWindow.destroy()])
                    noButton = tk.Button(removeCheckWindow, text = "No", command = removeCheckWindow.destroy)
                    removeItemEntry.unbind('<Return>')
                    
                    #removeCheckWindow.bind('<Return>', lambda event:[itemRemoval(removeVar.get()), removeCheckWindow.destroy(), removeItemEntry.bind('<Return>', lambda e: removeCheck())])
                    
                    removeLabel.place(relx=.5, rely=.3, anchor='center')
                    yesButton.place(relx=.2, rely=.6, anchor = 'center')
                    noButton.place(relx=.8, rely=.6, anchor='center')   
                    
                    removeCheckWindow.mainloop()
                    return
                
                removeTree = ttk.Treeview(removeItemWindow, selectmode = 'browse')
                removeTreeScrollbar = tk.Scrollbar(removeItemWindow, orient='vertical', command = removeTree.yview)
                
                removeTreeScrollbar.place(relx=.9, rely=.55, anchor = 'w')
                removeTree.place(relx=.5, rely=.55, anchor = 'center')
                returnButton.place(relx=.85, rely=.9, anchor='center')
                removeButton = tk.Button(removeItemWindow, text = 'Delete', command = removeCheck)
                removeButton.place(relx= .5, rely=.9, anchor='center')

                removeTree.configure(yscrollcommand = removeTreeScrollbar.set)
                removeTree["columns"] = ("1", "2", "3", "4", "5")
                removeTree['show'] = 'headings' 
                removeTree.column("1", width = 100, anchor = 'w')
                removeTree.column("2", width = 200, anchor = 'w')
                removeTree.column("3", width = 100, anchor = 'w')
                removeTree.column("4", width = 60, anchor = 'w')
                removeTree.column("5", width = 60, anchor = 'w')
                removeTree.heading("1", text = "Manufacturer #")
                removeTree.heading("2", text = "Description")
                removeTree.heading("3", text = "Barcode")
                removeTree.heading("4", text = "Quantity")
                removeTree.heading("5", text = "Kit")
                fillRemoveTree()
            return

        def returnHelper():
            subWindowLoc = childWindowLocation(removeItemWindow)
            removeItemWindow.destroy() 
            Admin(subWindowLoc)
            return

        removeVar.trace_add('write', removeCheckHelper)
        removeItemLabel = tk.Label(removeItemWindow, text = "Manufacturer Number:", font=('calibre', 12, 'bold'))
        removeItemEntry = tk.Entry(removeItemWindow, textvariable = removeVar, font=('calibre', 12))
        
        searchButton = tk.Button(removeItemWindow, text = 'Search', command = removeCheckHelper)
        removeItemEntry.bind('<Return>', lambda e: removeCheckHelper())
        
        returnButton = tk.Button(removeItemWindow, text = 'Return', command = returnHelper)
        
        removeItemLabel.place(relx=.01, rely=.4, anchor='w')
        removeItemEntry.place(relx=.48, rely=.4, anchor='center')
        searchButton.place(relx=.7, rely=.4, anchor='center')
        returnButton.place(relx=.85, rely=.85, anchor='center')
        
        removeItemEntry.focus_force()
        removeItemWindow.mainloop()
        return
    
    backupButton = ttk.Button(adminMenuWindow, text = "Backup Inventory", command = inventoryBackup)
    removeButton = ttk.Button(adminMenuWindow, text = "Remove Item", command = lambda:[adminMenuWindow.destroy(), removeItem()])
    bomButton = ttk.Button(adminMenuWindow, text = "BOM Menu", command = lambda:[adminMenuWindow.destroy(), createBOMGUI()])
    buildButton = ttk.Button(adminMenuWindow, text = "Builds", command = lambda: [adminBuildHelper()])
    homeButton = ttk.Button(adminMenuWindow, text = "Home", command = lambda:[adminMenuWindow.destroy(), mainMenu()])
    
    backupButton.place(relx=.5, rely=.4, anchor='center')
    removeButton.place(relx=.5, rely=.5, anchor='center')
    bomButton.place(relx=.5, rely=.6, anchor='center')
    buildButton.place(relx=.5, rely=.7, anchor='center')
    homeButton.place(relx=.75, rely=.85, anchor='center')
    
    adminMenuWindow.mainloop()
    
    return


# General functions used by all
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

def childWindowLocation(callingWindow):
    subWindow_x = str(callingWindow.winfo_x() + 100)
    subWindow_y = str(callingWindow.winfo_y() + 50)
    subWindowLoc = subWindow_x + "+" + subWindow_y
    return subWindowLoc

#TODO it might be a good idea to remove the searchType.get() checks and just use searchChoiceBox.get(). 
# I've had far fewer errors using that with other comboboxes
def mainMenu():
    cur = DG.conn.cursor()
    global mainMenuWindow
    global searchVar
    global searchType
    mainMenuWindow = tk.Tk()
    mainMenuWindow.geometry("600x200+200+300")
    mainMenuWindow.title("Main Menu")
    ttk.Style().configure("TButton", background="#ccc")

    searchVar = tk.StringVar()
    searchType = tk.StringVar()
    mainMenuWindow.focus_force()
    
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
            sql = '''SELECT DISTINCT manufacturerid FROM ''' + DG.invDatabase + ''' WHERE manufacturerid ILIKE %s order by manufacturerid;'''
            sType = 'manid'
        elif(searchType.get() == 'Item Name'):
            sql = '''SELECT DISTINCT Description FROM ''' + DG.invDatabase + ''' WHERE Description ILIKE %s order by Description;'''
            sType = 'description'
        else:
            print('Error in searchType comparison\nPrinting searchType: ' + searchType.get())
            return
        cur.execute(sql, [searchItem])
        records = cur.fetchall()
        if(records):
            for i in range(len(records)):
                args[0].insert(i, records[i][0])            

            def listBoxSelection(*listBoxArgs):
                itemIndex = args[0].curselection()[0]
                subWindow_x = str(mainMenuWindow.winfo_x() + 100)
                subWindow_y = str(mainMenuWindow.winfo_y() + 50)
                subWindowLoc = subWindow_x + "+" + subWindow_y
                selectedKit = 'None'
                
                
                if(sType == 'manid'):
                    sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE manufacturerid = %s;'''
                    cur.execute(sql, records[itemIndex])
                    searchRecords = cur.fetchall()
                    
                if(sType == 'description'):
                    sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE description = %s;'''
                    cur.execute(sql, records[itemIndex])
                    searchRecords = cur.fetchall()
                
                if(len(searchRecords) > 1):
                    def selectKit():
                        selectedKit = kitCheckComboBox.get()
                        for item in searchRecords:
                            if(selectedKit == 'None'):
                                selectedKit = '0'
                            if(item[8] == selectedKit):
                                kitCheckWindow.destroy()
                                adjustItemGUI(item[6], subWindowLoc)
                        return
                    kitChoice = tk.StringVar()
                    kitCheckWindow = tk.Tk()
                    kitCheckWindow.title("Kit Check")
                    subWindow_x = str(mainMenuWindow.winfo_x() + 100)
                    subWindow_y = str(mainMenuWindow.winfo_y() + 50)
                    subWindowLoc = subWindow_x + "+" + subWindow_y
                    kitCheckWindow.geometry("250x200+" + subWindowLoc)
                    kitCheckWindow.focus_force()
                    
                    kitCheckLabel = tk.Label(kitCheckWindow, text='Select kit item is a part of')
                    kitChoiceList = []
                    for item in searchRecords:
                        if(item[8] == '0'):
                            kitChoiceList.append("None")
                        else:
                            kitChoiceList.append(item[8])
                    kitCheckComboBox = ttk.Combobox(
                                        kitCheckWindow,
                                        state='readonly',
                                        values = kitChoiceList,
                                        textvariable=kitChoice
                                        )
                    kitCheckComboBox.set('None')
                    selectButton = tk.Button(kitCheckWindow, text='Select', command=selectKit)
                    
                    kitCheckLabel.place(relx=.5, rely=.3, anchor = 'center')
                    kitCheckComboBox.place(relx=.5, rely=.6, anchor='center')
                    selectButton.place(relx=.5, rely=.8, anchor='center')
                    
                    kitCheckWindow.mainloop()
                else:
                    selectedBarcode = searchRecords[0][6]
                    adjustItemGUI(selectedBarcode, subWindowLoc)

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
        subWindowLoc = childWindowLocation(mainMenuWindow)
        mainMenuWindow.destroy()
        adminLogin(subWindowLoc)
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
# =============================================================================
#                 sql = '''SELECT ManufacturerID FROM ''' + DG.invDatabase + ''' WHERE Barcode = %s'''
#                 cur.execute(sql, [records[0][0]])
#                 records = cur.fetchall()
# =============================================================================
                subWindow_x = str(mainMenuWindow.winfo_x() + 100)
                subWindow_y = str(mainMenuWindow.winfo_y() + 50)
                subWindowLoc = subWindow_x + "+" + subWindow_y
                searchInventoryEntry.delete(0, tk.END)
                adjustItemGUI(bar, subWindowLoc)
                
        else:
            print("Made it to barcodeSearch but searchType was not Barcode")
        return
    
    def buildsHelper():
        subWindowLoc = childWindowLocation(mainMenuWindow)
        viewBuilds(subWindowLoc, None)
        return
    
    def checkOutHelper():
        subWindowLoc = childWindowLocation(mainMenuWindow)
        checkOut(None, subWindowLoc, None)
        return
    

    searchVar.trace_add('write', searchHelper)
    searchInventoryLabel = tk.Label(mainMenuWindow, text='Search', font=('calibre', 12, 'bold'))
    searchInventoryEntry = tk.Entry(mainMenuWindow, textvariable = searchVar, font=('calibre', 12))  
    searchInventoryEntry.bind('<Return>', lambda e: barcodeSearchHelper())     
    searchButton = ttk.Button(mainMenuWindow, text = "Search", command = lambda: [barcodeSearch()])
    addItemButton = ttk.Button(mainMenuWindow, text = "Add Item", command = lambda: [addItemGUI()])
    buildsButton = ttk.Button(mainMenuWindow, text="Kits/Builds/RMAs", command = buildsHelper)
    checkOutButton = ttk.Button(mainMenuWindow, text = 'Check Out', command = checkOutHelper)
    adminButton = ttk.Button(mainMenuWindow, text = 'Admin', command = adminMenuHelper)

    # Row 1
    searchInventoryLabel.place(relx=.15, rely=.1, anchor='center')
    searchInventoryEntry.place(relx=.38, rely=.1, anchor='center')    
    searchChoiceBox.place(relx=.67, rely=.1, anchor='center')
    searchButton.place(relx=.88, rely=.1, anchor='center')
    
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
    
    
# Treeview barcode adjustment code
# Needed EVERY TIME a barcode is pulled from a treeview
# 
# barcode = str(barcode)  
# if(len(barcode) < 12):
#     zeroCount = 12 - len(barcode)
#     for i in range(zeroCount):
#         barcode = "0" + barcode