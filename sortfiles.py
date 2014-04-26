#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 4 2013
@author: talifero

Module for imeges template convertation.
       Tamplates:
    HD      1920x1080
    720p    1280x720
    PAL     720x380
    300     300x120
    



"""
import os, locale
from PIL import Image
import pyexiv2

locale.setlocale(locale.LC_ALL, '')



#sootnoshenie storon
#_____________________________________________
def cfct(h, v, shabl):
    '''Calculate new image size, for propertly sizes interrelations '''
    #print h, v, shabl
    if shabl == 'HD':
        must_hor = 1920.0
        must_ver = 1080.0

    if shabl == '720p':
        must_hor = 1280.0
        must_ver = 720.0

    if shabl == 'PAL':
        must_hor = 720.0
        must_ver = 380.0

    if shabl == '300':
        must_hor = 350.0
        must_ver = 180.0
    

    # Здесь нужно удалить кусок кода, лишняя проверкя h/v.
    if h > v:
        if h < must_hor:
            return (int(h/(v/must_ver)), int(must_ver))
        else:
            return (int(must_hor), int(v/(h/must_hor)))
    else:
        if v < must_hor:
            return (int(must_ver), int(v/(h/must_ver)))
        else:
            return (int(h/(v/must_hor)), int(must_hor))
  
#_____________________________________________





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


# Основная функцыя
#_____________________________________________

def resize_func(name, tmpl, imformat='JPG'):
    '''Main function of sortfiles.py module.
Get name 'name' of file and template 'tmpl' like 'HD' or '300' 
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
        outfile = os.path.splitext(name)[0] + "_" + tmpl + ".png"
    elif isinstance(imformat, int):
        #проверка второго аргумента, евляится ли 'imformat' числом
        outfile = os.path.splitext(name)[0] + "_" + tmpl + ".jpg"
        qual=imformat
    else:
        outfile = os.path.splitext(name)[0] + "_" + tmpl + ".jpg"
        qual=75

    #return 1 in to interface if image to small
    if tmpl == 'HD':
        k = 1080
    if tmpl == '720p':
        k = 720
    if tmpl == 'PAL':
        k = 380
    if tmpl == '300':
        k = 180
    if ver < k:
        return 1
    if gor < k:
        return 1  


    

    try:
        if imformat == 'PNG':
            im.resize(cfct(gor, ver, tmpl)).save(outfile)
        else:
            im.resize(cfct(gor, ver, tmpl)).save(outfile, quality=qual)
            #im.save(outfile)
        exif_data(name, outfile, cfct(gor, ver, tmpl))

              
    except IOError:
        return 'IOError'
#_____________________________________________


# Hint
#_____________________________________________
def _help_():
    print '''
	Скрипт для уменьшения фото до шаблонных размеров.
 Имейте ввиду скрипт УДАЛЯЕТ исходные файлы безвозвратно! Удаление происходит непосредственно вовремя работы, то есть даже если прервать работу скрипта по Ctrl+C часть файлов будет утеряна.
 Для корректной работы скрипту должен быть передан хотя бы один аргумент, который и послужит шаблоном для ресайза фотографий. Список возможных шаблонов:

	HD 1920x1080
	720p 1280x720
	SQR1 1000x1000
	SQR3 300x300
	PAL 720x380
	300 350x180

 Обратите внимание что только два шаблона SQR1 и SQR3 уменьшают картинку до точных размеров 1000х1000 и 300х300 соответственно, чтобы сохранить пропорции часть фотографии обрезается. Остальные шаблоны уменьшают картинку только приблизительно при этом сохраняя соотношение сторон.
 Скрипт сохраняет оригинальные EXIF данные, изменяя только Pixel X Dimension и Pixel Y Dimension в соответствии с новыми размерами.
 В качестве второго аргумента может быть передано PNG, для записи в этом формате,или же целое число для указания качества JPG, по умолчанию качество будет равным 65.
 В последней версии скрипта добавлена возможность сохронять оригиналы фотографий в папку 'old_files', для этого нужно добавить аргумент 'backup'. 
 Примеры: 

	pic_res.py HD 
		- уменьшает все фото в директории до размера 1920x1080 
	pic_res.py PAL PNG
		- уменьшает все фото в директории до размера 720х380, сохраняет фотографии в формате .png
	pic_res.py 720p 50
		- уменьшает все фото в директории до размера 1280х720, сохраняет фотографии в формате .jpg качество 50

 Также стоит отметить что скрипт изменяет имя файла, к оригинальному имени файла добавляется имя шаблона. Расширение записывается в нижнем регистре независимо от регистра оригинала. Например файл с именем DSC09640.JPG после команды pic_res.py hd получит имя DSC09640HD.jpg.


 Версия от 6 января 2014 года.
 talifero@gmail.com

     '''


#_____________________________________________

