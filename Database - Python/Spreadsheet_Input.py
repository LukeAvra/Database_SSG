# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 07:38:36 2023

Functions for inputing database data from excel spreadsheets

@author: Luke

"""
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(__file__))
import Database_Globals as DG

def importExcel(path, sheets):
    cur = DG.conn.cursor()
    dfFullList = pd.read_excel(path, sheet_name=sheets[0])
    
    # Unused as far as I can tell but keeping it here just in case
    #dfByBox = pd.read_excel(path, sheet_name=sheets[1])
    
    inDB, outDB = [], []
    
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
                if(str(dfFullList['New Count'][i]) == 'nan' or not str(dfFullList['New Count'][i]).isdigit()):
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
                print("Man #: %25s   Count: %5s      Desc: %40s" % (manNumber, quantity, desc))
                
                
                
                ##
                ## Whenever you're ready, these two lines will put it all into the database. I fucking hope.
                ##
# =============================================================================
#                 sql = '''INSERT INTO ''' + DG.invDatabase + ''' (manufacturerid, quantity, description) VALUES (%s, %s, %s);'''
#                 cur.execute(sql, [manNumber, quantity, desc])
# =============================================================================
                
                


def main():
    DG.main()
    path = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Production - Documents\\Inventory\\Cascade Inventory.xlsx"
    sheets = ['List', 'By Box']
    importExcel(path, sheets) 
    DG.close()    
    return

if __name__ == "__main__":
    main()


# =============================================================================
# path = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Production - Documents\\Inventory\\Cascade Inventory.xlsx"
# dfFullList = pd.read_excel(path, sheet_name='List')
# dfByBox = pd.read_excel(path, sheet_name='By Box')
# =============================================================================
