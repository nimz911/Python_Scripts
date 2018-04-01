import pyexiv2
import pandas as pd
import  os

#%%
path = ''  # Enter pictures folder path
file_list = [s for s in os.listdir(path) if s.endswith('.jpg')]

hashtags = []

for i in range(len(file_list)):
    jpg = file_list[i]
    metadata = pyexiv2.ImageMetadata(path+jpg)
    metadata.read()
    if len(metadata['Exif.Image.XPKeywords'].value) != 0:
        hashtags.append(pyexiv2.utils.undefined_to_string(metadata['Exif.Image.XPKeywords'].value).decode("utf-16"))
    else:
        hashtags.append('NO TAGS')
        
hashDF = pd.DataFrame({'file_list': file_list,'hashtags': hashtags})
hashDF['hashtags_NEW'] = hashDF['hashtags'].str.replace(';',' ')
hashDF = hashDF.loc[hashDF['hashtags_NEW'] != 'NO TAGS']

#%%
from nltk import *
text = hashDF['hashtags_NEW'].to_string()
tokens1 = word_tokenize(text)

from nltk.corpus import stopwords
stops = set(stopwords.words('english'))
pun = ['\'','.',',','(',')','[',']','...','&']
txt1 = []
for word in tokens1:
    if word.lower() not in stops:
        if word.lower() not in pun:
            txt1.append(word)
            
df1 = pd.DataFrame(txt1)
df1['1'] = 1
df1.columns = ['word', 'count']
count1 = df1[['word', 'count']].groupby(df1['word']).count()['count']
count1 = count1.to_frame()
count1 = count1.sort_values('count',ascending = False)
count1['P'] = count1['count'] / float(len(tokens1))

count1.head(20)

#%%
file_list = pd.DataFrame({'file_list': file_list})
file_list['date'], file_list['time'], file_list['filname']= file_list['file_list'].str.split(' ', 2).str
file_list = file_list.drop('file_list', 1)
file_list['year'], file_list['month'], file_list['day']= file_list['date'].str.split('-', 2).str
file_list['hour'], file_list['minute'], file_list['second']= file_list['time'].str.split('.', 2).str
file_list['hr_mn'] = file_list['hour'].astype(str) +':'+ file_list['minute']
file_list['weekday']= pd.to_datetime(file_list['date']).dt.dayofweek  # monday=0

#%%
hr = file_list['hour'].value_counts().to_frame()
hr = hr.reset_index()
hr = hr.rename(columns={'index': 'hour', 'hour': 'post_count'})

hr_mn = file_list['hr_mn'].value_counts().to_frame()
hr_mn = hr_mn.reset_index()
hr_mn = hr_mn.rename(columns={'index': 'hh:mm', 'hr_mn': 'post_count'})

weekday = file_list['weekday'].value_counts().to_frame()
weekday = weekday.reset_index()
weekday = weekday.rename(columns={'index': 'weekday', 'weekday': 'post_count'})

#%%


#%%