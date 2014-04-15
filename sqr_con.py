#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:53:22 2013

@author: talifero

Module for imeges template convertation.
       Tamplates:
    SQR1    1000x1000
    SQR3    300x300
"""


import sys, pyexiv2, os
from PIL import Image


#EXIF data  Maksym Kozlenko
#http://stackoverflow.com/questions/400788/resize-image-in-python-without-losing-exif-data
#_____________________________________________


def exif_data(source_path, dest_path, size):
    ''' EXIF data  Maksym Kozlenko
http://stackoverflow.com/questions/400788/resize-image-in-python-without-losing-exif-data
Take all EXIF data from source image, and put to the new image file, with new x-y sizes.    
    '''
    image = Image.open(dest_path)

    # copy EXIF data
    source_image = pyexiv2.ImageMetadata(source_path)
    source_image.read()
    dest_image = pyexiv2.ImageMetadata(dest_path)
    dest_image.read()
    source_image.copy(dest_image)

    # set EXIF image size info to resized size
    dest_image["Exif.Photo.PixelXDimension"] = image.size[0]
    dest_image["Exif.Photo.PixelYDimension"] = image.size[1]
    dest_image.write()
#_____________________________________________



#resizing image to square with side 1000 or 300
#_____________________________________________
def re_size(h, v, mode):
    '''Calculate new image size, for propertly square sizes'''
    if mode == 1000:
        must_hor, must_ver = 1000.0, 1000.0
    elif mode == 300:
        must_hor, must_ver = 300.0, 300.0
    else:
        print "Ошибка функции sqr_con.re_size() неверный аргумент 'mode'"
    
    coordinats=0    
    if h > v:
        new_im = [int(h/(v/must_ver)), int(must_ver)]
        coordinats = [(new_im[0]/2)-(mode/2), 0, (new_im[0]/2)+(mode/2), mode]
    else:
        new_im = [int(must_hor), int(v/(h/must_hor))]
        coordinats = [0, (new_im[1]/2)-(mode/2), mode, (new_im[1]/2)+(mode/2)]
    
    
    return new_im, coordinats

#_____________________________________________



def sqr(name, tmpl, imformat):
    '''Main function of sortfiles.py module.
Get name 'name' of file and template 'tmpl' 'SQR1' or 'SQR3'
'imformat' get "PNG" or "JPG".
    '''        
        #open image
    try:
        im=Image.open(name)
    except IOError:
        return 'IOError'

    #get size x-y
    gor=im.size[0]
    ver=im.size[1]
    
    #new name format    
    if imformat == 'PNG':
        outfile = os.path.splitext(name)[0] + tmpl + ".png"
    else:
        outfile = os.path.splitext(name)[0] + tmpl + ".jpg"
        
    #return 1 in to interface if image to small
    if tmpl=='SQR1':
        size_xy=1000
        if gor < 1000:
            if ver <1000:
                return 1
    elif tmpl=='SQR3':
        size_xy=300
        if gor < 300:
            if ver <300:
                return 1        
    else:
        sys.exit(1)
        
    cordinates=(re_size(gor, ver, size_xy))
    
    try:
        im.resize(cordinates[0]).crop(cordinates[1]).save(outfile)
        exif_data(name, outfile, (size_xy, size_xy))

              
    except IOError:
        return 'IOError'
    
