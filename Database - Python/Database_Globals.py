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
        
# Small function just to clear the screen #
def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear')
        
def roomList():
    cur = conn.cursor()
    sql = '''SELECT DISTINCT Room FROM main_inventory'''
    cur.execute(sql)
    rooms = []
    records = cur.fetchall()
    for row in records:
        rooms.append(row[0])
    
    return rooms

def main():
    global conn 
    conn = connect()

if __name__ == '__main__':
    main()
    
    
    
            