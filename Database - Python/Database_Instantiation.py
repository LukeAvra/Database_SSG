# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:36:00 2023

@author: Luke
"""
import Database_Globals as DG


#Initial create function, create's an empty inventory table with the listed columns
def create():
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS ssg_test_inventory (
                ManufacturerID VARCHAR(100),
                SupplierPartNum VARCHAR(100),
                Name VARCHAR(100),
                Description VARCHAR(100),
                Quantity INT,
                Barcode VARCHAR(100)
                );
            CREATE TABLE IF NOT EXISTS ssg_test_locations (
                Room VARCHAR(100),
                Rack SMALLINT,
                Shelf SMALLINT,
                Shelf_Location SMALLINT,
                Barcode VARCHAR(100)
                )
            END'''
            

            
    cur.execute(sql)
    
    print("Test Inventory and Location table's created successfully...")
    cur.close()