'''
Edit pictures EXIF metadata. Add titles and tags by reading excel files contains file names, titles and tags columns.
'''

import pyexiv2
import pandas as pd


#### insert TITLES ####
import pyexiv2
data = pd.read_excel('<xlsx file name>','fixed') # Enter excel file name 
for i in range(len(data['file_name'])):
    metadata = pyexiv2.ImageMetadata('<Pictures folder location>'+data['file_name'][i]) # Enter pictures folder path 
    metadata.read()
    key = 'Exif.Image.ImageDescription'
    value = data['long description'][i]
    metadata[key] = pyexiv2.ExifTag(key, value)
    metadata.write()
    
#### insert TAGS ####
import pyexiv2
data = pd.read_excel('<xlsx file name>','fixed')  # Enter excel file name
for i in range(len(data['file_name'])):
    metadata = pyexiv2.ImageMetadata('<Pictures folder location>'+data['file_name'][i]) # Enter pictures folder path
    metadata.read()
    metadata['Exif.Image.XPKeywords']=pyexiv2.utils.string_to_undefined(data['TAGS'][i].encode('utf-16'))
    metadata.write()

