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
    
    def fuck(x):
        x += 5
        return
    
    x = 5
    fuck(x)
    print(x)
    
    DG.close()
    
    
    
    return


if __name__ == '__main__':
    main()