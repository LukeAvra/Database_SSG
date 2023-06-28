# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 09:36:29 2023

@author: Luke Avra
"""

from prettytable import PrettyTable
import psycopg2
from config import config
from os import system, name

# Basic connection test, returns PostgreSQL DB version
def connect():
    # connects to the PostgreSQL database server 
    conn = None
    try:
        # read params from config file 
        params = config()
        
        # Connect to the server 
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return conn

def close():
    if conn is not None:
        conn.close()
        print('Database connection closed.')
        
# Small function just to clear the screen #
def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 
            
#Initial create function, create's an empty inventory table with the listed columns
def create():
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS main_inventory (
                id serial PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Room VARCHAR(100) NOT NULL,
                Rack SMALLINT NOT NULL,
                Shelf SMALLINT NOT NULL,
                Shelf_Location SMALLINT NOT NULL,
                Quantity INT NOT NULL
                );
            
            END'''
            
    cur.execute(sql)
    
    print(" Test table created successfully...")
    cur.close()

# Neither of these work yet, implement and incorporate when you get the chance
######################    
def searchBySerial():
    return

def searchByName():
    return
######################
# Simple initialization function to place some test data into the table created by create() function
def initialData():

    cur = conn.cursor()
    
    sql = '''INSERT INTO main_inventory (Name, Room, Rack, Shelf, Shelf_Location, Quantity)
             VALUES 
                 ('Power Cable - LHCDC', 'Main Inventory', 3, 2, 25, 50),
                 ('Screw #10', 'Main Inventory', 1, 3, 4, 1000),
                 ('AAA Battery', 'Main Inventory', 2, 4, 20, 15),
                 ('Extension Cord', 'Manufacturing', 3, 2, 10, 12),
                 ('Toilet Paper', 'Bathroom Closet', 1, 2, 3, 8),
                 ('Floor Mats', 'Production', 3, 2, 1, 9);
             
            END'''
            
    cur.execute(sql)
    print(" Initial Data added to main_inventory table")
    conn.commit()
    cur.close()
    
def addItem(cur):
    clear()
    print("Please enter all details presented")
    name = input("Item Name: ")

    room = input("Room Name: ")
    rack = input("Rack Number: ")
    shelf = input("Shelf Number: ")
    shelfLocation = input("Shelf Location (Integer): ")
    quantity = input("Quantity: ")
    
    sql = ''' INSERT INTO main_inventory (Name, Room, Rack, Shelf, Shelf_Location, Quantity)
              SELECT %s, %s, %s, %s, %s, %s'''
    cur.execute(sql, [name, room, rack, shelf, shelfLocation, quantity])
    print(name, "added to inventory in", room)
    conn.commit()
    
def addData():
    cur = conn.cursor()

    # Variables used
    #    name, room, rack, shelf, shelfLocation, quantity
    # 
    clear()
    print(" Please enter the item you wish to add to inventory (or type 'exit' to exit)")
    itemInput = '%' + input() + '%'
    if(itemInput == '%exit%'):
        return
    sql = '''SELECT DISTINCT Name FROM main_inventory WHERE Name ILIKE %s'''
    cur.execute(sql, [itemInput])
    records = cur.fetchall()
    if(records):
        clear()
        print("There are similar items already in inventory")
        for record in records:
            print(" >>", record[0], "<<")
        print('\n Please type the full name of the item if you wish to adjust quantity or location, otherwise type "n" to add new item')
        userInput = input()
        
        if(userInput == 'n'):
            addItem(cur)
        else:
# =============================================================================
#             sql = '''SELECT * FROM main_inventory WHERE ILIKE %s'''
#             cur.execute(sql, [userInput])
#             records = cur.fetchall()
#             print(">>", records[0][0], "<<")
# =============================================================================
            check = False
            for record in records:
                if(record[0].lower() == userInput.lower()):
                    clear()
                    print(">>", record[0], "<<")
                    yesNoResponse = input(" Is this the item you want to adjust? (y/n) ")
                    if(yesNoResponse == "y"):
                        check = True
                        adjustItem(cur, record[0])
                        return
                    else:
                        return

            if not check:
                print(" It doesn't seem as though that item is in our inventory")
                
               

    else:
        print(" Item not found, new form created.\nPress Enter to continue...") 
        input()
        addItem(cur)

        
    input(" Press Enter to continue...")
    
# =============================================================================
#     # Adds data into the inventory ONLY IF THE NAME IS NOT ALREADY PRESENT         
#     sql = '''INSERT INTO main_inventory (Name, Room, Rack, Shelf, Shelf_Location, Quantity)
#              SELECT %s, %s, %s, %s, %s, %s
#              WHERE NOT EXISTS
#                  (SELECT * FROM main_inventory WHERE Name=%s);
#             END'''
#     
#     cur.execute(sql, [name, room, rack, shelf, shelfLocation, quantity, name])
#     print(" Initial Data added to main_inventory table")
# =============================================================================
    cur.close()
    
def adjustItemHelper():
    cur = conn.cursor()
    while True:
        # Essentially just the 'Display All' func but I didn't like having the 'press enter to continue bit
        # ---------------------------------------------------   
# =============================================================================
#         sql = '''SELECT * FROM main_inventory'''
#         cur.execute(sql) 
#         fullRecords = cur.fetchall()
#         recordTable = PrettyTable(['ID', 'Name', 'Room', 'Rack Number', 'Shelf Number', 'Shelf Location', 'Quantity'])
#         for row in fullRecords:
#             recordTable.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
#             recordTable.add_row(['-----', '-----', '-----', '-----', '-----', '-----', '-----' ])
#         clear()
#         print(recordTable)
# =============================================================================
        # ---------------------------------------------------
        displayAll()
        
        print(" Enter the full name of the Item you would like to adjust (or type 'exit' to exit)")
        adjustInput = '%' + input("Item Name: ") + '%'
        if(adjustInput.lower() == '%exit%'):
            return
        sql = '''SELECT Name FROM main_inventory
                 WHERE Name ILIKE %s'''
        cur.execute(sql, [adjustInput])
        records = cur.fetchall()
        check = False
        if(records):
            if(len(records) == 1):
                print(">>", records[0][0], "<<")
                yesNoResponse = input("Is this the item you want to adjust? (y/n) ")
                if(yesNoResponse == "y"):
                    check = True
                    adjustItem(cur, records[0][0])
                    return
            else:
                for record in records:
                    print(" >> " + record[0] + " << ")
                input("\n There are multiple results from that search, please be more specific\nPress Enter to continue...")
                continue
                    
# =============================================================================
#         for record in records:
#             if(record[0].lower() == adjustInput.lower()):
#                 print(">>", record[0], "<<")
#                 yesNoResponse = input("Is this the item you want to adjust? (y/n) ")
#                 if(yesNoResponse == "y"):
#                     check = True
#                     adjustItem(cur, record[0])
#                     return
# =============================================================================
    
        else:
            input("It doesn't seem as though that item is in our inventory\nPress Enter to continue...")        


def adjustItem(cur, item):
    #print("Item adjustment here")
    sql = '''SELECT * FROM main_inventory WHERE name=%s'''
    cur.execute(sql, [item])
    records = cur.fetchall()
    while True:
        clear()
        printTable(records, 0)
        print("Please enter the number next to the field you would like to adjust: ")
        print(" 1) ID")
        print(" 2) Name")
        print(" 3) Room")
        print(" 4) Rack Number")
        print(" 5) Shelf Number")
        print(" 6) Shelf Location")
        print(" 7) Quantity")
        print(" 8) Exit")
        
        try:
            adjustSelection = int(input())
        except ValueError:
            print("Please enter an integer\nPress Enter to continue...")
            input()
            continue
        
        if(adjustSelection == 1):
            print("Please enter the new ID number (or type 'exit' to cancel): ")
            idInput = input()
            if(idInput.lower() == 'exit'):
                return False
            else:
                try:
                    idInput = int(idInput)
                except ValueError:
                    input("Please enter an integer\n\nPress Enter to continue...")
                    return
                    
                sql = '''UPDATE main_inventory
                         SET id=%s
                         WHERE Name=%s'''
                cur.execute(sql, [idInput, item])
                conn.commit()
                print("ID number changed to", idInput)
                print("Press Enter to continue...")
                input()
                return False
                
        elif(adjustSelection == 2):
            print("Please enter the new Item Name (or type 'exit' to cancel): ")
            nameInput = input()
            if(nameInput.lower() == 'exit'):
                return False
            else:
                sql = '''UPDATE main_inventory
                         SET Name=%s
                         WHERE Name=%s'''
                cur.execute(sql, [nameInput, item])
                conn.commit()
                print("Item name changed to", nameInput)
                print("Press enter to continue...")
                input()
                return False
            
        elif(adjustSelection == 3):
            print("Please enter the new Room Name (or type 'exit' to cancel): ")
            roomInput = input()
            if(roomInput.lower() == 'exit'):
                return False
            else:
                sql = '''UPDATE main_inventory
                         SET Room=%s
                         WHERE Name=%s'''
                cur.execute(sql, [roomInput, item])
                conn.commit()
                print("Room name changed to", roomInput)
                print("Press enter to continue...")
                input()
                return False
            
        elif(adjustSelection == 4):
            print("Please enter the new Rack Number (or type 'exit' to cancel): ")
            checkInput = input()
            if(checkInput.lower() == 'exit'):
                return False
            else:
                try:
                    rackInput = int(checkInput)
                except ValueError:
                    print("An integer must be entered\nPress Enter to continue...")
                    input()
                    continue
                sql = '''UPDATE main_inventory
                         SET Rack=%s
                         WHERE Name=%s'''
                cur.execute(sql, [rackInput, item])
                conn.commit()
                print("Rack number changed to", rackInput)
                print("Press enter to continue...")
                input()
                return False
            

        elif(adjustSelection == 5):
            print("Please enter the new Shelf Number (or type 'exit' to cancel): ")
            checkInput = input()
            if(checkInput.lower() == 'exit'):
                return False
            else:
                try:
                    shelfInput = int(checkInput)
                except ValueError:
                    print("An integer must be entered\nPress Enter to continue...")
                    input()
                    continue
                sql = '''UPDATE main_inventory
                         SET Shelf=%s
                         WHERE Name=%s'''
                cur.execute(sql, [shelfInput, item])
                conn.commit()
                print("Shelf number changed to", shelfInput)
                print("Press enter to continue...")
                input()
                return False

        elif(adjustSelection == 6):
            print("Please enter the new Shelf Location (number) (or type 'exit' to cancel): ")
            checkInput = input()
            if(checkInput.lower() == 'exit'):
                return False
            else:
                try:
                    locInput = int(checkInput)
                except ValueError:
                    print("An integer must be entered\nPress Enter to continue...")
                    input()
                    continue
                sql = '''UPDATE main_inventory
                         SET Shelf_Location=%s
                         WHERE Name=%s'''
                cur.execute(sql, [locInput, item])
                conn.commit()
                print("Shelf Location number changed to", locInput)
                print("Press enter to continue...")
                input()
                return False

        elif(adjustSelection == 7):
            print("Please enter the new Quantity (or type 'exit' to cancel): ")
            checkInput = input()
            if(checkInput.lower() == 'exit'):
                return False
            else:
                try:
                    quantityInput = int(checkInput)
                except ValueError:
                    print("An integer must be entered\nPress Enter to continue...")
                    input()
                    continue
                sql = '''UPDATE main_inventory
                         SET Quantity=%s
                         WHERE Name=%s'''
                cur.execute(sql, [quantityInput, item])
                conn.commit()
                print("Quantity changed to", quantityInput)
                print("Press enter to continue...")
                input()
                return False
            
        elif(adjustSelection == 8):
            return False
            
    
    return


#
#
# FINISH ME, I NEED TO BE FINISHED
#
#
def removeData():
    cur = conn.cursor()
    clear()
    while True:
        displayAll()
        print(" Delete item by name or serial number?")
        print(" 1) Name")
        print(" 2) Serial Number")
        print(" 3) Exit")
        userChoice = input()
        try:
            userChoice = int(userChoice)
        except ValueError:
            input("Please enter a valid integer\n\n Press Enter to continue...")
            continue
        if(userChoice == 1):
            deletion = '%' + input(" Enter the name of the item you wish to delete\n Name: ") +'%'
            
            sql = '''SELECT * FROM main_inventory WHERE Name ILIKE %s'''
            cur.execute(sql, [deletion])
            records = cur.fetchall()
            if(not records):
                input(" Could not find a record of that item\n\n Press Enter to continue...")
                continue
            elif(len(records) > 1):
                printTable(records, 1)
                input("Multiple items found, please enter the full name of the item to be deleted or delete by serial number\n\n Press Enter to continue...")
                continue
            else:
                printTable(records, 0)
                yesNoSelection = input("Is this the item you want to delete? (y, n)\n")
                if(yesNoSelection.lower() == 'n'):
                    input("Operation cancelled\n\n Press Enter to continue...")
                    continue
                elif(yesNoSelection.lower() == 'y'):
                    print("Are you sure you want to delete item:", records[0][1] + "? (y/n)")
                    deleteConfirmation = input()
                    if(deleteConfirmation.lower() == 'n'):
                        input("Operation cancelled\n\n Press Enter to continue...")
                        continue
                    elif(deleteConfirmation.lower() == 'y'):
                        deletion = records[0][1]
                        sql = '''DELETE FROM main_inventory WHERE Name=%s'''
                        cur.execute(sql, [deletion])
                        conn.commit()
                        print("Item:", deletion, "deleted succesfully\n\n Press Enter to continue...")
                        input()
                        continue
                else:
                    continue
                        
            
        elif(userChoice == 2):
            deletion = input(" Enter the Serial Number of the item you wish to delete\n Serial Number: ")
            try:
                deletion = int(deletion)
            except ValueError:
                input(" Please enter a valid integer \n\n Press Enter to continue...")
                continue
            sql = '''SELECT * FROM main_inventory WHERE id=%s'''
            cur.execute(sql, [deletion])
            records = cur.fetchall()
            if(records):
                if(len(records) > 1):
                    printTable(records, 1)
                    input(" There seem to be more than one records with that Serial Number\n Please return to the main menu to adjust records or delete by item name \n\n Press Enter to continue...")
                    return
                else:
                    printTable(records, 0)
                    yesNoSelection = input("Are you sure you wish to delete this item? (y/n)\n")
                    if(yesNoSelection.lower() == 'n'):
                        input("Operation cancelled\n\n Press Enter to continue...")
                        continue
                    elif(yesNoSelection.lower() == 'y'):
                        sql = '''DELETE FROM main_inventory WHERE id=%s'''
                        cur.execute(sql, [records[0][0]])
                        conn.commit()
                        print("Item:", records[0][1], "deleted successfully\n\n Press Enter to continue...")
                        input()
                        continue   
            else:
                input(" Could not find a record of that item\n\n Press Enter to continue...") 
                continue
        elif(userChoice == 3):
            return
            
        else:
            input("Please enter a valid response:\n\n Press Enter to continue...")
            continue
        

         
    
    # Removes data if identical to name
# =============================================================================
#     sql = '''DELETE FROM main_inventory WHERE name=%s'''
#     cur.execute(sql, [name])
#     print(" Items removed from inventory database")
# =============================================================================
    cur.close()

def displayAll():
    cur = conn.cursor()
    sql = '''SELECT * FROM main_inventory'''
    cur.execute(sql) 
    
    fullRecords = cur.fetchall()
    clear()
    printTable(fullRecords, 1)     
    cur.close()
    

def displayParticular():
    cur = conn.cursor()
    
    while True:
        clear()
        print(" Select how you would like to search for item")
        print(" 1) Name")
        print(" 2) Serial Number")
        print(" 3) Location")
        print(" 4) Return To Main Menu")
        
        # Checks to make sure the user actually put an integer in 
        try:
            userInput = int(input())
        except ValueError:
            continue
        
        # Search By Name
        if(userInput == 1):
            clear()
            print(" Please enter the name of the product")
            nameInput = '%' + input() + '%'
            sql = '''SELECT * FROM main_inventory WHERE Name ILIKE %s'''
            cur.execute(sql, [nameInput])
            records = cur.fetchall()
            if(not records):
                input(' Could not find that item\n\n Press Enter to continue...')
                continue
            printTable(records, 0)
            input("Press Enter to continue...")
            
        # Search By Serial Number
        elif(userInput == 2):
            clear()
            print(" Please enter the serial number of the product")
            try:
                serialInput = int(input())
            except ValueError:
                print("Please enter a valid integer\nPress Enter to continue...")
                input()
                continue
            sql = '''SELECT * from main_inventory WHERE ID=%s'''
            cur.execute(sql, [serialInput])
            records = cur.fetchall()
            if(not records):
                print("Item with serial", serialInput, "is not in the database\nPress Enter to continue...")
                input()
                continue
            printTable(records, 0)
            input("Press Enter to continue...")
        
        # Search By Inventory Room
        elif(userInput == 3):
            clear()
            print(" Please enter the name of the room to be displayed")
            sql = '''SELECT DISTINCT Room FROM main_inventory'''
            cur.execute(sql)
            records = cur.fetchall()
            for row in records:
                print("--", row[0], "--")
            roomInput = '%' + input("Room Name: ") + '%'
            sql = '''SELECT * FROM main_inventory WHERE Room ILIKE %s'''
            cur.execute(sql, [roomInput])
            records = cur.fetchall()
            if(records):
                if(len(records) == 1):
                    printTable(records, 0)
                    input("Press Enter to continue...")
                else:
                    printTable(records, 1)
                    input("Press Enter to continue...")
            else:
                input("Could not find location in inventory\n\n Press Enter to continue...")
        
        # Return To previous menu
        elif(userInput == 4):
            clear()
            return False
        
        # Catch-all if the input is an integer but doesn't match menu items
        else:
            print("\n\n\n\n *** Incorrect input, please enter the number corresponding with your choice. ***\n")
    cur.close()
            
def printTable(records, style):
    recordTable = PrettyTable(['ID', 'Name', 'Room', 'Rack Number', 'Shelf Number', 'Shelf Location', 'Quantity'])
    if style == 0:
        for row in records:
            recordTable.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
    if style == 1:
        for row in records:
            recordTable.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
            recordTable.add_row(['-----', '-----', '-----', '-----', '-----', '-----', '-----' ])
    print(recordTable)

# Home screen for CLI
def admin():   
    clear()
    print(" =============Special Services Group Inventory Managment=============")
    while(1):
        clear()
        print(" 1) Display Entire Inventory")
        print(" 2) Display Details on Particular Inventory Items")
        print(" 3) Add Item to Inventory")
        print(" 4) Adjust Item in Inventory")
        print(" 5) Remove Item from Inventory")
        
        try:
            userInput = int(input())
        except ValueError:
            print("\n\n\n Please enter an Integer")
            continue
        if(userInput == 1):
            displayAll()
            input("Press Enter to continue...")
        elif(userInput == 2):
            displayParticular()
        elif(userInput == 3):
            addData()
        elif(userInput == 4):
            adjustItemHelper()
        elif(userInput == 5):
            removeData()
        else:
            print(" Incorrect input, please enter the number corresponding with your choice. \n")

if __name__ == '__main__':
    conn = connect()
    admin()
    close()
    
    
               
# Add in Admin/User accounts?
#   Admin can do everything
#   Users can only view records

#
# Shelf Location should probably be switched to a VARCHAR for ease of use, although Shelf 3, Loc 6 could work fine
# 
# Should be noted whether Shelves are numbered top to bottom or bottom to top
# 

#
# While adjusting values in database, maybe pull out to a different function for the sql statment, could make code cleaner (two sections, one for name one for number)
#

#
# Might want to add ability to search by Serial Number for adjusting items
#

#
# Not sure if it'll actually save space but finish the searchBySerial and searchByName functions, both should just return 'records'
# See if they can be implemented 
#


# Saving for later in case keeping an open connection bricks this thing
#
# =============================================================================
#     conn = psycopg2.connect(
#         database='inventory', user='postgres', password='SSGllc2023@)@#', host='127.0.0.1', port='5432'
#         )
#     conn.autocommit = True
# =============================================================================