# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:05:02 2023

@author: Luke
"""
# Printer Testing
import sys, os
sys.path.append('C:\\Program Files\\gs\\gs10.01.2\\bin')
sys.path.append(os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
from brother_ql.devicedependent import models
import random
import treepoem

def createBarcodeImage(barcodeText, barcode):
    #"inkspread" : .1, The closer to 1.0, the thinner the lines. With the 62mm continuous-red roll, thinner lines won't scan
    image = treepoem.generate_barcode(
        barcode_type = "upca",
        data = barcode,
        options = {"includetext": True, "textfont" : "Times-Roman", "width": 2, "showborder": False}
        )
    
    # Create Barcodes folder if it doesn't exist (Doesn't help much currently as we need 'Base' folder within that holds 400x200 blank image)
    # Adding the Base folder should be easy but figure out how to generate the image
    if(not os.path.exists(os.path.dirname(__file__) + "\\Barcodes")):
        os.mkdir(os.path.dirname(__file__) + "\\Barcodes")
    
    # Create file location and convert treepoem 'image' into a .png
    filename = (os.path.dirname(__file__) + "\\Barcodes\\barcode.png")
    image.convert("1").save(filename)
    
    # Create final image starting with baseline of blank 400x200 image
    with Image.open(os.path.dirname(__file__) + "\\Barcodes\\Base\\4x2.png").convert("RGBA") as base:
        text = Image.new("RGBA", base.size, (255, 255, 255, 0))
        font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 20)
        draw = ImageDraw.Draw(text)
    
    # Establish location of text that goes over barcode
    text_x = int(0.5*base.width)
    text_y = 20
    draw.text((text_x, text_y), barcodeText, anchor="ms", font=font, fill="black")
    
    # Output alpha composite image
    out = Image.alpha_composite(base, text)
    
    # open and paste barcode image onto alpha composite image
    barcodeImage = Image.open(filename)
    barcode_x = text_x - int(0.5 * barcodeImage.width)
    barcode_y = base.height - 170
    out.paste(barcodeImage, (barcode_x, barcode_y))
    out.save(os.path.dirname(__file__) + "\\Barcodes\\barcode.png")
    
    return

def printBarcode():
    # Grab the model name, could really just type this out
    modelList = [m for m in models]
    
    # Might want to itemize backend and printer variables for easy adjustment to USB printing
    backend = 'network'
    model = modelList[11]
    printer = 'tcp://192.168.56.32'
    
    # Open barcode image at location saved from above and resize it to fit well on label
    barImage = Image.open(os.path.dirname(__file__) + "\\Barcodes\\barcode.png")
    barImage = barImage.resize((600, 300))
    barWidth, barHeight = barImage.size
    
    # Create new image that fits chosen label and center barcode .png in the center
    # Might be able to pull those two values from the 'Printable px' list (cmdprmpt -> brother_ql info labels)
    im = Image.new("L", (696, 300), color = "white")
    imWidth, imHeight = im.size
    offset = ((imWidth - barWidth) // 2, (imHeight - barHeight) // 2)
    im.paste(barImage, offset)
    
    # Instructions for actual printing. The 62mm needs 'red' after it's label and the 'red' variable needs to be True
    instructions = convert(
        qlr = BrotherQLRaster(model),
        images = [im],
        label = "62red",
        rotate='0',
        threshold=95.0,
        dither=False,
        compress=False,
        red=True,
        dpi_600=False,
        hq=True,
        cut=True  
        )
    
    # Send instructions to the printer
    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)
    
    return

def main():
    # Text that appears above barcode on label
    text = "Special Services Group"
    createBarcodeImage(text, "329018288409")
    printBarcode()
    return

if __name__ == "__main__":
    main()


# Label sizes and printable pixels
# =============================================================================
#  Name      Printable px   Description
#  12         106           12mm endless
#  29         306           29mm endless
#  38         413           38mm endless
#  50         554           50mm endless
#  54         590           54mm endless
#  62         696           62mm endless
#  62red      696           62mm endless (black/red/white)
#  102       1164           102mm endless
#  17x54      165 x  566    17mm x 54mm die-cut
#  17x87      165 x  956    17mm x 87mm die-cut
#  23x23      202 x  202    23mm x 23mm die-cut
#  29x42      306 x  425    29mm x 42mm die-cut
#  29x90      306 x  991    29mm x 90mm die-cut
#  39x90      413 x  991    38mm x 90mm die-cut
#  39x48      425 x  495    39mm x 48mm die-cut
#  52x29      578 x  271    52mm x 29mm die-cut
#  62x29      696 x  271    62mm x 29mm die-cut
#  62x100     696 x 1109    62mm x 100mm die-cut
#  102x51    1164 x  526    102mm x 51mm die-cut
#  102x152   1164 x 1660    102mm x 153mm die-cut
#  d12         94 x   94    12mm round die-cut
#  d24        236 x  236    24mm round die-cut
#  d58        618 x  618    58mm round die-cut
# =============================================================================

# Changes from testing labels

# rotate changed to 0
# label = "29x90" --> label = "52x29"
# barImage = barImage.resize((600, 300)) --> barImage = barImage.resize((400, 200))

    

# Generate a barcode image in zpl.label format
# Generates a .png of the barcode, may be useful for later 
# This is all for Zebra Label printers

# =============================================================================
# import zpl
# import random
#
# 
# l = zpl.Label(10,25)
# height = 0
# 
# l.origin(5, 1)
# barcode = generateBarcode()
# l.barcode('U', barcode, height=70, check_digit='Y')
# l.endorigin()
# 
# print(l.dumpZPL())
# print(type(l.preview()))
# #print(type(l))
# 
# =============================================================================


