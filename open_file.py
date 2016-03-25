# -*- coding: utf-8 -*-
import io

def open_file(file):
    open_file = io.open(file)
    file = open_file.read()
    open_file.close()
    return file, 'utf-8'


open_file('inspection_page.html')
