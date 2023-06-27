# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 09:36:29 2023

@author: Luke Avra
"""

from prettytable import PrettyTable
import psycopg2
from config import config
from os import system, name

#Basic connection test, returns PostgreSQL DB version
def connect():
    # connects to the PostgreSQL database server #
    
    conn = None
    try:
        # read params from config file #
        params = config()
        
        # Connect to the server #
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # Create cursor #
        cur = conn.cursor()
        
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        
        # Display PostgreSQL DB version #
        db_version = cur.fetchone()
        print(db_version)
        
        # Close communication with the DB #
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            
#Initial create function, create's an empty inventory table with the listed columns
def create():
    conn = psycopg2.connect(
        database='inventory', user='postgres', password='SSGllc2023@)@#', host='127.0.0.1', port='5432'
        )
    conn.autocommit = True
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
    conn.close()
    
# Simple initialization function to place some test data into the table created by create() function
def initialData():
    
    conn = psycopg2.connect(
        database='inventory', user='postgres', password='SSGllc2023@)@#', host='127.0.0.1', port='5432'
        )
    conn.autocommit = True
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
    conn.close()
                 
    
def addData(name, room, rack, shelf, shelfLocation, quantity):
    conn = psycopg2.connect(
        database='inventory', user='postgres', password='SSGllc2023@)@#', host='127.0.0.1', port='5432'
        )
    conn.autocommit = True
    cur = conn.cursor()
    
    
    # Adds data into the inventory ONLY IF THE NAME IS NOT ALREADY PRESENT #
            
    sql = '''INSERT INTO main_inventory (Name, Room, Rack, Shelf, Shelf_Location, Quantity)
             SELECT %s, %s, %s, %s, %s, %s
             WHERE NOT EXISTS
                 (SELECT * FROM main_inventory WHERE Name=%s);
            END'''
    
    cur.execute(sql, [name, room, rack, shelf, shelfLocation, quantity, name])
    print(" Initial Data added to main_inventory table")
    conn.close()

# Removes data from inventory with name matching the name passed to the function
# May be a good idea to switch to Serial numbers when those are added to avert spelling issues
def removeData(name):
    
    conn = psycopg2.connect(
        database='inventory', user='postgres', password='SSGllc2023@)@#', host='127.0.0.1', port='5432'
        )
    conn.autocommit = True
    cur = conn.cursor()
    
    sql = '''DELETE FROM main_inventory WHERE name=%s'''
    
    
    cur.execute(sql, [name])
    print(" Items removed from inventory database")
    conn.close()

def displayAll():
    conn = psycopg2.connect(
        database='inventory', user='postgres', password='SSGllc2023@)@#', host='127.0.0.1', port='5432'
        )
    conn.autocommit = True
    cur = conn.cursor()
    
    sql = '''SELECT * FROM main_inventory'''
    cur.execute(sql) 
    
    fullRecords = cur.fetchall()
    recordTable = PrettyTable(['ID', 'Name', 'Room', 'Rack Number', 'Shelf Number', 'Shelf Location', 'Quantity'])
    for row in fullRecords:
        recordTable.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
        recordTable.add_row(['-----', '-----', '-----', '-----', '-----', '-----', '-----' ])
    clear()
    print(recordTable)
    print("\n\n\n")        
    conn.close()

def displayParticular():
    conn = psycopg2.connect(
        database='inventory', user='postgres', password='SSGllc2023@)@#', host='127.0.0.1', port='5432'
        )
    conn.autocommit = True
    cur = conn.cursor()
    
    while True:
        print(" Select how you would like to search for item")
        print(" 1) Name")
        print(" 2) Serial Number")
        print(" 3) Return To Main Menu")
        
        try:
            userInput = int(input())
        except ValueError:
            print("\n\n\n Please enter an Integer")
            continue
        if(userInput == 1):
            # Search By Name
            clear()
            print(" Please enter the name of the product")
            nameInput = input()
            sql = '''SELECT * FROM main_inventory WHERE Name=%s'''
            cur.execute(sql, [nameInput])
            records = cur.fetchall()
            printTable(records, 0)
        elif(userInput == 2):
            # Search By Serial Number
            clear()
            print(" Please enter the serial number of the product")
            serialInput = int(input())
            sql = '''SELECT * from main_inventory WHERE ID=%s'''
            cur.execute(sql, [serialInput])
            records = cur.fetchall()
            printTable(records, 0)
        elif(userInput == 3):
            clear()
            return False
        else:
            print("\n\n\n\n *** Incorrect input, please enter the number corresponding with your choice. ***\n")
    conn.close()
            
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

    
# Small function just to clear the screen #
def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 

def admin():    
    print(" =============Special Services Group Inventory Managment=============")
    while(1):
        print(" 1) Display Entire Inventory")
        print(" 2) Display Details on Particular Inventory Item")
        
        try:
            userInput = int(input())
        except ValueError:
            print("\n\n\n Please enter an Integer")
            continue
        if(userInput == 1):
            displayAll()
        elif(userInput == 2):
            displayParticular()
        else:
            print(" Incorrect input, please enter the number corresponding with your choice. \n")
        


if __name__ == '__main__':
    #connect()
    #create()
    #initialData()
    #addData('Soldering Iron', 'Main Inventory', 3, 5, 12, 8)
    #addData('Test', 'Test', 1, 1, 1, 1)
    #removeData('Test')
    admin()
                    
# When displaying entire inventory, maybe have it take up the entire screen and user has to hit enter to exit? Menu beneath looks bad
