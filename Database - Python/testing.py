# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 11:56:27 2023

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


def main():
    newLocationsList = [['manid5', '703919624397', 13, None], ['manid3', '287215318698', 52, None], ['manid2', '666227944499', 78, None], ['manid10', '413806797140', 12, None]]
    
    
    def editLocation(*args):
        #cur = DG.conn.cursor()     
        #loc is the location within newLocationsTree, it's only used to pull the selectedItemList
        loc = newLocationsTree.selection()[0]
        selectedItemList = newLocationsTree.item(loc)['values']
        barcode = selectedItemList[1]
        # Uncomment once added back into Database_GUI
        subWindow_x = str(newLocationsWindow.winfo_x() + 100)
        subWindow_y = str(newLocationsWindow.winfo_y() + 50)
        subWindowLoc = subWindow_x + "+" + subWindow_y
        
        adjustItemGUI(barcode, subWindowLoc)
        sql = '''SELECT * FROM ssg_locations WHERE barcode = %s;'''
        cur.execute(sql, [barcode])
        locationRecords = cur.fetchall()
        currentLocation = locationRecords[0][0] + " " + chr(locationRecords[0][1]) + '-' + locationRecords[0][2]
        
        labelText = selectedItemList[0].lower()
        labelText = labelText + " " + currentLocation
        print(labelText)
        PL.createBarcodeImage(labelText, newBarcode)
        PL.printBarcode()
        
        newLocationsTree.item(loc, values = (selectedItemList[0], selectedItemList[1], selectedItemList[2], currentLocation))
        
        return

    def submissionCheck():
        emptyLocationsList = []
        for line in newLocationsTree.get_children():
            if((str(newLocationsTree.item(line).get('values')[3])) == 'None'):
                emptyLocationsList.append(newLocationsTree.item(line).get('values'))
        if(emptyLocationsList):
            print(emptyLocationsList)
            tk.messagebox.showerror("ERROR", "Please add a location to all items")
        else:
            tk.messagebox.showinfo("Success", "Items added into inventory in their new locations")

        return

    
    newLocationsWindow = tk.Tk()
    newLocationsWindow.title("New Locations")
    newLocationsWindow.geometry("500x350")
    
    newLocationsTree = ttk.Treeview(newLocationsWindow, selectmode='browse', height = 10)
    newLocationsScrollbar = tk.Scrollbar(newLocationsWindow, orient='vertical', command = newLocationsTree.yview)
    completeButton = tk.Button(newLocationsWindow, text='Submit', command=submissionCheck)
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
    
    newLocationsWindow.mainloop()
    
    
    
    return


if __name__ == '__main__':
    main()