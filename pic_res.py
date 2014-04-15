#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: talifero

Это позняя версия фаила ftest.py ( 6 апреля 2013 года  )
СКРИПТ для уменшения фоток до шаблонных размеров
Шаблоны:
    HD      1920x1080
    720p    1280x720
    SQR1    1000x1000 
    SQR3    300x300 
    PAL     720x380
    300     300x120
"""


import os, sys, curses, locale, glob, shutil
import sortfiles, sqr_con#, pic_res_conf #my own modules



locale.setlocale(locale.LC_ALL, '')


#proverka argumentov
#________________________________________

def arg1():
    """  Опредиление размеров по аргументам, размеры принимаются ввиде шаблона.   
Шаблоны:
    HD      1920x1080
    720p    1280x720
    SQR1    1000x1000
    SQR3    300x300
    PAL     720x380
    300     350x180
    
Return 'sortfiles' for call 'sortfiles.py' and 'sqr_con' to call 'sqr_con.py'.   
Call sortfiles._help_() if argument -?, -h or --help.
"""
    if len(sys.argv)>1:
        if sys.argv[1] == 'HD':
            return 'sortfiles'
        elif sys.argv[1]=='hd':
            sys.argv[1]='HD'
            return 'sortfiles'
        elif sys.argv[1]=='720p':
            return 'sortfiles'
        elif sys.argv[1]=='PAL':
            return 'sortfiles'
        elif sys.argv[1]=='300':
            return 'sortfiles'
        elif sys.argv[1]=='SQR1':
            return 'sqr_con'
        elif sys.argv[1]=='SQR3':
            return 'sqr_con'
        elif sys.argv[1]=='-h':
            sortfiles._help_()
            sys.exit(1)
        elif sys.argv[1]=='--help':
            sortfiles._help_()
            sys.exit(1)
        elif sys.argv[1]=='-?':
            sortfiles._help_()
            sys.exit(1)

            
        else:
            print 'Не верный аргумент номер один!  Допустимо: HD, 720p, PAL, SQR1, 300.'
            print '  --help для помощи'
            sys.exit(1)
            
    else:

        print 'Должен быть хотя бы один аргумент!  Допустимо: HD, 720p, PAL, SQR1, 300.'
        print '  --help для помощи'
        sys.exit(1)
    

#_____________________________________________


def arg2():
    
    if len(sys.argv)>2:
        if sys.argv[2] == 'PNG':
            return 'PNG'
        elif sys.argv[2] == 'png':
            return 'PNG'
        elif sys.argv[2] == 'backup':
            sys.argv.append('backup')
            return 75
        elif sys.argv[2] == 'b':
            sys.argv.append('backup')
            return 75            
        else:
            try:
                return int(sys.argv[2])
            except:
                print 'Не верный аргумент номер два, допустимо "PNG" или целое число для указания качества "JPG"'
                print '  --help для помощи'
                sys.exit()




#poluchenie vsex fajlov
#_____________________________________________
def files_str():
    """Take all files names from dir, and put to list 'img' """
    jpg=glob.glob('*.jpg')
    png=glob.glob('*.png')
    jpg_b=glob.glob('*.JPG')

    img = jpg+png+jpg_b
    
    return img
#_____________________________________________


#razmery fajlof
#_____________________________________________
def files_size(pic):
    """Return size of all files in directory"""
    pic_size = 0

    for files in pic:
            size=os.path.getsize(files)
            pic_size = pic_size + size

    pic_size=round((pic_size/1024)/1024.0,3)
    return pic_size
#____________________________________________


# meniu procenty
#________________________________________
def perce(n, f):
    """Percent bar, 'n' number of converted files, 'f' number of all files """
    one_per=100.0/f
    all_per=(one_per*n)*0.7
    lik = 70.0 - all_per
    bar = '<'+'='*int(all_per)+' '*int(lik)+'>'
    return bar
#________________________________________    


#collect Information

def _info_():

    if len(sys.argv)>2:
        if sys.argv[2] == 'PNG':
            return 'Конвертирование файлов.'+' Формат: '+str(sys.argv[1])+' Расширение: PNG'
        elif sys.argv[2] == 'png':
            return 'Конвертирование файлов.'+' Формат: '+str(sys.argv[1])+' Расширение: PNG'
        elif sys.argv[2] == 'backup':
            return 'Конвертирование файлов.'+' Формат: '+str(sys.argv[1])+' Режим: backup!'
        elif sys.argv[2] == 'b':
            return 'Конвертирование файлов.'+' Формат: '+str(sys.argv[1])+' Режим: backup!'

        
        else:
            return 'Конвертирование файлов.'+' Формат: '+str(sys.argv[1])+' Расширение: JPG (qual. '+str(sys.argv[2])+')'

    else:
        return 'Конвертирование файлов.'+' Формат: '+str(sys.argv[1])+' Расширение: JPG (qual. 75)'

#________________________________________



#sozdanie direktorii

def ensure_dir(d):
    if not os.path.exists(d):
        try:
            os.makedirs(d)
        except OSError:
            print 'Невозможно создать директорию old_files'
            sys.exit(1)
    else:
        pass


#________________________________________


#ИНТЕРФЕЙС
#_____________________________________________
n = 1
arg1()#Просто проверка аргументов до отрисовки интерфеиса
arg2()#Просто проверка аргументов до отрисовки интерфеиса
info=_info_()
filles_len = len(files_str())

if len(sys.argv)>3:
    if sys.argv[3]=='backup':
        ensure_dir('old_files')
    
if filles_len == 0:
    print 'Нечего конвертировать. Не найдено ни одного .jpg или .png фаила.'
    sys.exit(1)
err_line = 9 #Линия на которой в интефейсе будут ошибки
size_bifore=files_size(files_str())

myscreen = curses.initscr()
myscreen.border(0)

#myscreen.addstr(2, 3, 'Конвертирование файлов.'+' Формат '+str(sys.argv[1]))
myscreen.addstr(2, 3, info)
myscreen.addstr(3, 3, 'Всего файлов: '+str(filles_len))


for filename in files_str():
    if arg1() == 'sortfiles':
        sf=sortfiles.resize_func(filename, sys.argv[1], arg2())
    elif arg1() == 'sqr_con':
        sf=sqr_con.sqr(filename, sys.argv[1], arg2())
    else:
        sys.exit(1)
    if sf == 1:
        myscreen.addstr(5, 3, ' '*70)        
        #если картинка слишком мала 
        myscreen.addstr(5, 3, 'Пропуск файла: '+filename+', слишком маленький!')
        myscreen.addstr(7, 3, perce(n, filles_len))
        myscreen.refresh()
        
    elif sf == 'IOError':
        myscreen.addstr(err_line, 3, 'Ошибка IOError, '+filename)
        myscreen.addstr(7, 3, perce(n, filles_len))
        myscreen.refresh()
        #Все ошибки сюда...
        #Мини экран для ошибок. с 9 по 14 строку выводятся ошыбки.        
        err_line=err_line+1
        if err_line == 15:
            err_line == 9
    
    else:
        myscreen.addstr(5, 3, ' '*70)
        #Уменьшенийе файла 
        myscreen.addstr(5, 3, 'Уменьшенийе файла: '+ filename)
        myscreen.addstr(7, 3, perce(n, filles_len))
        myscreen.refresh()
        if len(sys.argv)>3:
            if sys.argv[3]=='backup':
                try:
                    shutil.copy2(filename, 'old_files')
                except IOError:
                    sys.exit(1)
        os.remove(filename)
    n=n+1
	
size_after=files_size(files_str())


# Подбиваем итоги, размеры фаилов до и после 
myscreen.addstr(18, 3, '_'*30)
myscreen.addstr(19, 3, 'Размеры до уменьшенийя: '+str(size_bifore)+' MB')
myscreen.addstr(20, 3, 'Размеры после уменьшенийя: '+str(size_after)+' MB')
myscreen.addstr(21, 3, 'Экономия места: '+str(size_bifore-size_after)+' MB')               
myscreen.refresh()
myscreen.getch()
curses.endwin()
