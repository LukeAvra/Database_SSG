# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 07:38:36 2023

Functions for inputing database data from excel spreadsheets

@author: Luke

"""
import pandas as pd

def importExcel(path, sheets):
    dfFullList = pd.read_excel(path, sheet_name=sheets[0])
    dfByBox = pd.read_excel(path, sheet_name=sheets[1])
    print(dfFullList)

def main():
    path = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Production - Documents\\Inventory\\Cascade Inventory.xlsx"
    sheets = ['List', 'By Box']
    importExcel(path, sheets) 
    
    return

if __name__ == "__main__":
    main()


# =============================================================================
# path = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Production - Documents\\Inventory\\Cascade Inventory.xlsx"
# dfFullList = pd.read_excel(path, sheet_name='List')
# dfByBox = pd.read_excel(path, sheet_name='By Box')
# =============================================================================
