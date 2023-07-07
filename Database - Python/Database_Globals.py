# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:34:34 2023

@author: Stuck
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
        
# Small function just to clear the screen for CLI #
def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear')
        
def roomList():
    cur = conn.cursor()
    sql = '''SELECT DISTINCT Room FROM ssg_test_locations'''
    cur.execute(sql)
    rooms = []
    records = cur.fetchall()
    for row in records:
        rooms.append(row[0])
    
    return rooms

def searchID(ID):
    cur = conn.cursor()
    sql = '''SELECT Barcode FROM ssg_test_inventory
            WHERE ManufacturerID = %s'''
    cur.execute(sql, [ID])
    records = cur.fetchall()
    barcode = records[0][0]
    
    sql = '''SELECT * FROM ssg_test_inventory
           WHERE ManufacturerID = %s'''
    cur.execute(sql, [ID])
    invRecords = cur.fetchall()

            
    sql = '''SELECT * FROM ssg_test_locations
           WHERE Barcode = %s'''
    cur.execute(sql, [barcode])
    locRecords = cur.fetchall()
    
    return invRecords, locRecords

def searchTotal(ID, version):
    cur = conn.cursor()
    sql = '''SELECT Barcode FROM ssg_test_inventory
            WHERE %s = %s'''
    cur.execute(sql, [version, ID])
    records = cur.fetchall()
    barcode = records[0][0]
    
    sql = '''SELECT * FROM ssg_test_inventory
           WHERE %s = %s'''
    cur.execute(sql, [version, ID])
    invRecords = cur.fetchall()
    
    sql = '''SELECT * FROM ssg_test_locations
           WHERE Barcode = %s'''
    cur.execute(sql, [barcode])
    locRecords = cur.fetchall()
    
    return invRecords, locRecords

def searchByName(searchItem):
    cur = conn.cursor()
    userInputItem = '%' + searchItem + '%'
    sql = '''SELECT DISTINCT Name FROM ssg_test_inventory WHERE Name ILIKE %s'''
    cur.execute(sql, [userInputItem])
    records = cur.fetchall()
    return records

def main():
    global conn 
    conn = connect()

if __name__ == '__main__':
    main()
    
    
    
            