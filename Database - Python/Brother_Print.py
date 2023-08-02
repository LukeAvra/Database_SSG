# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:59:41 2023

@author: Luke

Client Script
"""
from PIL import Image, ImageDraw
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
from brother_ql.devicedependent import models

import os
models = [m for m in models]

backend = 'network'
model = models[11]
printer = 'tcp://192.168.56.32'

barImage = Image.open(os.path.dirname(__file__) + "\\Barcodes\\barcode.png")
barImage = barImage.resize((600, 300))
barWidth, barHeight = barImage.size

im = Image.new("L", (991, 306), color = "white")
imWidth, imHeight = im.size
offset = ((imWidth - barWidth) // 2, (imHeight - barHeight) // 2)
im.paste(barImage, offset)
#barImage.resize((991, 306))

# =============================================================================
# im = Image.new("L", (991, 306), color = "white")
# g = ImageDraw.Draw(im)
# g.text((10,150), "PLEASE WORK GODDAMNIT", fill="black")
# =============================================================================



instructions = convert(
    qlr = BrotherQLRaster(model),
    images = [im],
    label = "29x90",
    rotate='90',
    threshold=70.0,
    dither=False,
    compress=False,
    red=False,
    dpi_600=False,
    hq=True,
    cut=True  
    )

send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)


