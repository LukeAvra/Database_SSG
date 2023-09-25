# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:34:34 2023

@author: Stuck
"""
#from prettytable import PrettyTable
import psycopg2
#from config import config, configDBVars
import config
import random
from os import system, name

# Basic connection test, returns PostgreSQL DB version
def connect():
    # connects to the PostgreSQL database server 
    conn = None
    try:
        # read params from config file 
        params, parser = config.config()
        
        # Connect to the server 
        print('Connecting to the PostgreSQL database at ''' + parser[0][1] + '...')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
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
        
def createGlobalVars():
    invDatabase, userDatabase, barDatabase, bomDatabase, locDatabase, kitDatabase, rmaDatabase, buildDatabase = config.configDBVars()
    #print(invDatabase, userDatabase, barDatabase, bomDatabase, locDatabase)
    return invDatabase, userDatabase, barDatabase, bomDatabase, locDatabase, kitDatabase, rmaDatabase, buildDatabase

def roomList():
    cur = conn.cursor()
    sql = '''SELECT DISTINCT Room FROM ''' + locDatabase + ''';'''
    cur.execute(sql)
    rooms = []
    records = cur.fetchall()
    for row in records:
        rooms.append(row[0])
    
    return rooms

def searchID(ID):
    cur = conn.cursor()
    sql = '''SELECT * FROM ''' + invDatabase + ''' WHERE barcode = %s;'''
    cur.execute(sql, [ID])
    invRecords = cur.fetchall()
    sql = '''SELECT * FROM ''' + locDatabase + ''' WHERE Barcode = %s;'''
    cur.execute(sql, [ID])
    locRecords = cur.fetchall()
# =============================================================================
#         barcode = records[0][0]
#         
#         sql = '''SELECT * FROM ''' + invDatabase + '''
#                WHERE barcode = %s'''
#         cur.execute(sql, [ID])
#         invRecords = cur.fetchall()
#                 
#         sql = '''SELECT * FROM ''' + locDatabase + '''
#                WHERE Barcode = %s'''
#         cur.execute(sql, [barcode])
#         locRecords = cur.fetchall()
# =============================================================================
    if(not invRecords):
        invRecords = None
    if(not locRecords):
        locRecords = None
    
    return invRecords, locRecords

def searchTotal(ID, version):
    cur = conn.cursor()
    sql = '''SELECT Barcode FROM ''' + invDatabase + '''
            WHERE %s = %s'''
    cur.execute(sql, [version, ID])
    records = cur.fetchall()
    barcode = records[0][0]
    
    sql = '''SELECT * FROM ''' + invDatabase + '''
           WHERE %s = %s'''
    cur.execute(sql, [version, ID])
    invRecords = cur.fetchall()
    
    sql = '''SELECT * FROM ''' + locDatabase + '''
           WHERE Barcode = %s'''
    cur.execute(sql, [barcode])
    locRecords = cur.fetchall()
    
    return invRecords, locRecords

def createBarcode():
    cur = conn.cursor()
    barcodeList = []
    barcodeString = ''
    odds = 0
    barcodeList.append(random.randrange(1, 10))
    for i in range(0, 10):
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
    sql = '''SELECT * FROM ''' + barDatabase + ''' WHERE code=%s'''
    cur.execute(sql, [sqlCheck])
    records = cur.fetchone()
    if records:
        createBarcode()
    return sqlCheck

def searchByName(searchItem):
    cur = conn.cursor()
    userInputItem = '%' + searchItem + '%'
    sql = '''SELECT DISTINCT Description FROM ''' + invDatabase + ''' WHERE Description ILIKE %s order by Description'''
    cur.execute(sql, [userInputItem])
    records = cur.fetchall()
    return records

def main():
    global conn
    global invDatabase
    global userDatabase
    global barDatabase
    global bomDatabase
    global locDatabase
    global buildDatabase
    global kitDatabase
    global rmaDatabase

    conn = connect()
    invDatabase, userDatabase, barDatabase, bomDatabase, locDatabase, kitDatabase, rmaDatabase, buildDatabase = createGlobalVars()
    
if __name__ == '__main__':
    main()
    
    
    
            