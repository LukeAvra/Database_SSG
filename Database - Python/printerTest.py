# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:05:02 2023

@author: Luke
"""
# Printer Testing

import zpl
import random

def generateBarcode():
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
    
    return barcodeString

l = zpl.Label(10,25)
height = 0

l.origin(5, 1)
barcode = generateBarcode()
l.barcode('U', barcode, height=70, check_digit='Y')
l.endorigin()

print(l.dumpZPL())
l.preview()