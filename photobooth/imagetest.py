'''
Created on Apr 13, 2014

@author: johannes
'''

import Image
image=Image.open("test.jpg")
if image.mode != '1':
    image = image.convert('1')

width  = image.size[0]
height = image.size[1]

rowBytes = (width + 7) / 8
bitmap   = bytearray(rowBytes * height)
pixels   = image.load()

for y in range(height):
    n = y * rowBytes
    x = 0
    for b in range(rowBytes):
        sum = 0
        bit = 128
        while bit > 0:
            if x >= width: break
            if pixels[x, y] == 0:
                sum |= bit
            x    += 1
            bit >>= 1
        bitmap[n + b] = sum
img=Image.new('RGB',(rowBytes,height))
img.putdata(bitmap)
img.save("test2.jpg")