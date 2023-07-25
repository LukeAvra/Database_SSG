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
                Barcode VARCHAR(100),
                BOM_ID SMALLINT
                );
        CREATE TABLE IF NOT EXISTS ssg_inventory (
                ManufacturerID VARCHAR(100),
                Manufacturer VARCHAR(100),
                SupplierPartNum VARCHAR(100),
                Supplier VARCHAR(100),
                Description VARCHAR(100),
                Quantity INT,
                Barcode VARCHAR(100),
                BOM_ID SMALLINT
                );
            CREATE TABLE IF NOT EXISTS ssg_test_locations (
                Room VARCHAR(100),
                Rack SMALLINT,
                Shelf SMALLINT,
                Shelf_Location SMALLINT,
                Barcode VARCHAR(100)
                );
            CREATE TABLE IF NOT EXISTS ssg_locations (
                Room VARCHAR(100),
                Rack SMALLINT,
                Shelf SMALLINT,
                Shelf_Location SMALLINT,
                Barcode VARCHAR(100)
                );
            CREATE TABLE IF NOT EXISTS ssg_test_users (
                userCode VARCHAR(100),
                userName VARCHAR(100)
                );
            CREATE TABLE IF NOT EXISTS ssg_users (
                userCode VARCHAR(100),
                userName VARCHAR(100)
                );
            CREATE TABLE IF NOT EXISTS ssg_test_boms (
                bom_id SMALLINT,
                bom_name VARCHAR(100)
                );
            CREATE TABLE IF NOT EXISTS ssg_boms (
                bom_id SMALLINT,
                bom_name VARCHAR(100)
                );
            END'''
            
    cur.execute(sql)
    
    print("Test Inventory, Location and Users tables created successfully...")
    cur.close()
    
def testData():
    cur = conn.cursor()
    sql = '''INSERT INTO ssg_test_inventory (ManufacturerID, SupplierPartNum, Name, Description, Quantity, Barcode, BOM_ID)
             VALUES 
                 ('manID1', 'supPartNum1', 'Power Cable - LHCDC', 'Power Cable for the LHCDC', 50, 'asd24ldk45', NULL),
                 ('manID2', 'supPartNum2', 'Screw #10', '#10 size machining screw, flat top', 10050, '12ke85dy03', NULL),
                 ('manID3', 'supPartNum3', 'AAA Battery', 'Battery: size AAA, Brand: Energizer', 22, 'nrlsd876wj', NULL),
                 ('manID4', 'supPartNum4', 'Extension Cord', 'Extended power cable, approximately 15 feet long, fits American outlets', 3, 'sflcb3928l', NULL),
                 ('manID5', 'supPartNum5', 'Computer Power Brick', 'Power Brick for laptop computer using a USB-C connection', 5, '345lcskl90', NULL),
                 ('manID6', 'supPartNum6', 'LHC', 'LHC ptz camera with Radon cover', 123, 'dlv1582swl', 1),
                 ('manID7', 'supPartNum7', 'Pelican Case - 1200', 'Pelican case sized for LHC with foam insert', 230, 'kdlo89bw46', NULL);
                 
             INSERT INTO ssg_inventory (ManufacturerID, Manufacturer, SupplierPartNum, Supplier, Description, Quantity, Barcode, BOM_ID)
             VALUES 
                 ('manID1', 'Manufacturer1', 'supPartNum1', 'Supplier1', 'Power Cable - LHCDC', 'Power Cable for the LHCDC', 50, 'asd24ldk45', NULL),
                 ('manID2', 'Manufacturer2', 'supPartNum2', 'Supplier2', 'Screw #10', '#10 size machining screw, flat top', 10050, '12ke85dy03', NULL),
                 ('manID3', 'Manufacturer3', 'supPartNum3', 'Supplier3', 'AAA Battery', 'Battery: size AAA, Brand: Energizer', 22, 'nrlsd876wj', NULL),
                 ('manID4', 'Manufacturer4', 'supPartNum4', 'Supplier4', 'Extension Cord', 'Extended power cable, approximately 15 feet long, fits American outlets', 3, 'sflcb3928l', NULL),
                 ('manID5', 'Manufacturer5', 'supPartNum5', 'Supplier5', 'Computer Power Brick', 'Power Brick for laptop computer using a USB-C connection', 5, '345lcskl90', NULL),
                 ('manID6', 'Manufacturer6', 'supPartNum6', 'Supplier6', LHC', 'LHC ptz camera with Radon cover', 123, 'dlv1582swl', 1),
                 ('manID7', 'Manufacturer7', 'supPartNum7', 'Supplier7', 'Pelican Case - 1200', 'Pelican case sized for LHC with foam insert', 230, 'kdlo89bw46', NULL);
             INSERT INTO ssg_test_locations (Room, Rack, Shelf, Shelf_Location, Barcode)
             VALUES
                 ('Main Inventory', 4, 2, 15, 'asd24ldk45'),
                 ('Main Inventory', 6, 3, 12, '12ke85dy03'),
                 ('Main Inventory', 2, 1, 9, 'nrlsd876wj'),
                 ('Main Inventory', 5, 3, 1, 'sflcb3928l'),
                 ('Prodution', 1, 2, 12, '345lcskl90'),
                 ('Mezzanine', 1, 1, 2, 'dlv1582swl'), 
                 ('Mezzanine', 2, 1, 3, 'kdlo89bw46');
             
             INSERT INTO ssg_test_users (userCode, userName)
             VALUES
                 ('ldo53j4kvc', 'Joey'),
                 ('l3kd0ckv56', 'Corey'),
                 ('lsk43ljk09', 'Andy'),
                 ('l3kd98g093', 'Mirriam'),
                 ('lucisgreat', 'Luke');
            END'''

    cur.execute(sql)
    print('Initial dummy data added to ssf_test_inventory, ssg_test_locations and ssg_test_users')
    cur.close()
    
def testData_Extended():
    cur = conn.cursor()
    sql = '''INSERT INTO ssg_inventory (ManufacturerID, Manufacturer, SupplierPartNum, Supplier, Description, Quantity, Barcode, BOM_ID)
             VALUES 
                 ('manID1', 'Manufacturer1', 'supPartNum1', 'Supplier1', 'Power Cable - LHCDC', 50, 'asd24ldk45', NULL),
                 ('manID2', 'Manufacturer2', 'supPartNum2', 'Supplier2', 'Screw #10', 10050, '12ke85dy03', NULL),
                 ('manID3', 'Manufacturer3', 'supPartNum3', 'Supplier3', 'AAA Battery', 22, 'nrlsd876wj', NULL),
                 ('manID4', 'Manufacturer4', 'supPartNum4', 'Supplier4', 'Extension Cord', 3, 'sflcb3928l', NULL),
                 ('manID5', 'Manufacturer5', 'supPartNum5', 'Supplier5', 'Computer Power Brick', 5, '345lcskl90', NULL),
                 ('manID6', 'Manufacturer6', 'supPartNum6', 'Supplier6', 'LHC', 123, 'dlv1582swl', 1),
                 ('manID7', 'Manufacturer7', 'supPartNum7', 'Supplier7', 'Pelican Case - 1200', 230, 'kdlo89bw46', NULL);
                 
             INSERT INTO ssg_locations (Room, Rack, Shelf, Shelf_Location, Barcode)
             VALUES
                 ('Main Inventory', 4, 2, 15, 'asd24ldk45'),
                 ('Main Inventory', 6, 3, 12, '12ke85dy03'),
                 ('Main Inventory', 2, 1, 9, 'nrlsd876wj'),
                 ('Main Inventory', 5, 3, 1, 'sflcb3928l'),
                 ('Prodution', 1, 2, 12, '345lcskl90'),
                 ('Mezzanine', 1, 1, 2, 'dlv1582swl'), 
                 ('Mezzanine', 2, 1, 3, 'kdlo89bw46');
                 
             INSERT INTO barcodes (code)
             VALUES
                 ('asd24ldk45'),
                 ('12ke85dy03'),
                 ('nrlsd876wj'),
                 ('sflcb3928l'),
                 ('345lcskl90'),
                 ('dlv1582swl'),
                 ('kdlo89bw46');
            END'''

    cur.execute(sql)
    print('Initial dummy data added to ssf_test_inventory, ssg_test_locations and ssg_test_users')
    cur.close()
    
def wipe():
    # BE FUCKING CAREFUL.
    # TESTING MISTAKES ONLY
    cur = conn.cursor()
    sql = '''DELETE FROM ssg_inventory;
             DELETE FROM ssg_locations;
             DELETE FROM barcodes;
         END'''
    cur.execute(sql)
    cur.close

def main():
    global conn 
    conn = DG.connect()
    create()
    #testData_Extended()

if __name__ == '__main__':
    main()