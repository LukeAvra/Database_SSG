# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 07:45:41 2023

@author: Luke
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.setrecursionlimit(5000)
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import ttk
from datetime import datetime
import Database_Globals as DG
import Print_Label as PL
import psqlBackupScript as BU
import random
import bcrypt


def mainMenu():

    return

def main():
    DG.main()
    cur = DG.conn.cursor()
    sql = 'select name from ssg_builds UNION select name from ssg_rmas UNION select name from ssg_kits;'
    cur.execute(sql)
    records = cur.fetchall()
    for rec in records:
        sql = '''ALTER TABLE ''' + rec[0] + ''' ALTER COLUMN description TYPE VARCHAR(1000);'''
        print(sql)
        cur.execute(sql)
    
    return


if __name__ == '__main__':
    main()