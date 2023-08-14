# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 07:38:36 2023

Functions for inputing database data from excel spreadsheets

@author: Luke

"""
import pandas as pd
import random
import sys, os
sys.path.append(os.path.dirname(__file__))
import Database_Globals as DG

def generateBarcode():
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
        generateBarcode()
        return
    else:    
        return sqlCheck, barcodeString, str(checkDigit)

def importExcel(path, sheets):
    cur = DG.conn.cursor()
    dfFullList = pd.read_excel(path, sheet_name=sheets[0])
    
    # Unused as far as I can tell but keeping it here just in case
    #dfByBox = pd.read_excel(path, sheet_name=sheets[1])
    count = 0
    countOut = 0
    for i in range(len(dfFullList)):
        #print("Part Number: %30s      New Count: %10s" % (dfFullList['Part Number'][i], dfFullList['New Count'][i]))
        if(str(dfFullList['Part Number'][i]) != 'nan'):
            sql = '''SELECT * FROM ''' + DG.invDatabase + ''' WHERE manufacturerid = %s;'''
            cur.execute(sql, [str(dfFullList['Part Number'][i]).lower()])
            records = cur.fetchall()
            if(records):
                count = count + 1
            else:
                # Converting Counts to integers for input
                if(str(dfFullList['New Count'][i]) == 'nan' or not str(dfFullList['New Count'][i]).isdigit() or str(dfFullList['New Count'][i]) == '0'):
                    quantity = None
                else:
                    quantity = int(dfFullList['New Count'][i])
                # Converting Descriptions to strings for input
                if(str(dfFullList['Description'][i]) == 'nan'):
                    desc = None
                else:
                    desc = str(dfFullList['Description'][i].upper()) 
                manNumber = str(dfFullList['Part Number'][i]).lower()
                
                countOut = countOut + 1
                fullBar, bar, checkDigit = generateBarcode()
                print("Man #: %25s   Count: %5s      Barcode: %12s       Desc: %40s" % (manNumber, quantity, fullBar, desc))
                

                ## Testing SQL inputs
                
# =============================================================================
#                 sql = '''INSERT INTO testinput (manufacturerid, quantity, description, barcode) VALUES (%s, %s, %s, %s);
#                         INSERT INTO testlocations(barcode) VALUES (%s);
#                         INSERT INTO testbarcodes (code) VALUES (%s);'''
#                 cur.execute(sql, [manNumber, quantity, desc, fullBar, fullBar, fullBar])
# =============================================================================
                sql = '''INSERT INTO ''' + DG.invDatabase + ''' (manufacturerid, quantity, description, barcode) VALUES (%s, %s, %s, %s);
                        INSERT INTO ''' + DG.locDatabase + '''(barcode) VALUES (%s);
                        INSERT INTO ''' + DG.barDatabase + '''(code) VALUES (%s);'''
                cur.execute(sql, [manNumber, quantity, desc, fullBar, fullBar, fullBar])


                
def barCheck():
    cur = DG.conn.cursor()
    barcodes, invCodes = [], []
    sql = '''SELECT barcode FROM ssg_inventory;'''
    cur.execute(sql)
    invBarRecords = cur.fetchall()
    for rec in invBarRecords:
        invCodes.append(rec[0])
    sql = '''SELECT code FROM barcodes;'''
    cur.execute(sql)
    barRecords = cur.fetchall()
    for rec in barRecords:
        barcodes.append(rec[0])
    
    for i in barcodes:
        if i not in invCodes:
            print(i)
    return

def main():
    DG.main()
    path = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Production - Documents\\Inventory\\Cascade Inventory.xlsx"
    sheets = ['List', 'By Box']
    importExcel(path, sheets) 
    #barCheck()
    DG.close()    
    return

if __name__ == "__main__":
    main()


# =============================================================================
# path = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Production - Documents\\Inventory\\Cascade Inventory.xlsx"
# dfFullList = pd.read_excel(path, sheet_name='List')
# dfByBox = pd.read_excel(path, sheet_name='By Box')
# =============================================================================
