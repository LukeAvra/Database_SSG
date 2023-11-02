# Database_SSG
Inventory Management System

Requires a backend postgreSQL server to be established with tables as follows:
<pre>
Inventory:                                    Main inventory information
 column_name     | data_type
 ----------------+------------------
 bom_id          | smallint                   Random number that will be established automatically by the program. If more Bill of Materials are needed, adjust data_type and line ~2000 #bomID = random.randrange(0, 32750)# to a larger random range
 quantity        | integer                    Quantity of item in inventory
 supplierpartnum | character varying          Supplier part num, alphanumeric sequence 
 supplier        | character varying          Supplier name
 description     | character varying          Description of item
 barcode         | character varying          12 character sequence automatically assigned to each new item
 manufacturerid  | character varying          Manufacuter identification alphanumeric sequence 
 kit             | character varying          Kit that the item is a part of 
 manufacturer    | character varying          Manufacturer name
 

Locations:                                    Locations of individual items
  column_name   |     data_type
----------------+-------------------
 rack           | smallint                    Rack, entered as a character, A-Z, and converted to ASCII value 
 shelf          | smallint                    Shelf number
 shelf_location | smallint                    Shelf location number
 room           | character varying           Name of room/inventory location
 barcode        | character varying           Barcode automatically assigned to item, used as key between inventory and locations tables


 Barcodes:                                    Used to collect all barcodes to double check that nothing is being duplicated
  column_name |     data_type
-------------+-------------------
 code        | character varying              Automatically assigned barcodes 


 Builds, Kits and RMAs:                       Three separate tables that share the same structure. Builds and RMAs pull items fully out of inventory when they are placed in them. Kits will move items to a new location in inventory to establish a 'kit' to build units
  column_name |     data_type
-------------+-------------------
 userview    | integer                        integer used as bool, was thrown in last minute and can be adjusted. Used to determine whether kit/build/rma can be viewed by all or just admins
 name        | character varying              name of kit/build/rma
 barcode     | character varying              assigned barcode for kit/build/rma. Used for scanning items directly out of inventory into a kit/build/rma

</pre>
<pre>
These tables will need to be established in a 'Database.ini' file, placed in the 'Database - Python' folder with structure as follows:

[postgresql]
host=xxx.xxx.xxx.xxx
database=database_name
user=postgresql_username
password=postgresql_password

[database_table_names]
inventory_table=inventory_table_name
location_table=locations_table_name
user_table=ssg_users
barcode_table=barcodes_table_name
bill_of_material_table=bom_table_name
kit_table=kit_table_name
rma_table=rma_table_name
build_table=build_table_name

	
This system also relies on a brother label printer and will hang if one is not established and connected.
This setup will be added into the database.ini file but for now, Print_Label.py lines 66-68 need to be adjusted for the used printer
    backend = 'network'                #Needs to be adjusted according to brother_ql documentation if not running on WIFI
    model = modelList[index]              #Model of brother printer needs to be pulled from this list (I believe it can also be pulled in as a simple string)
    printer = 'tcp://xxx.xxx.xxx.xxx'    #Location of the printer on the network, check brother_ql documentation for a usb connected label printer

</pre>
