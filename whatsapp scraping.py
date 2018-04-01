import pandas as pd
import re
import codecs

#%%
f = open("","r") # Enter Whatsapp log file location
fw = open("","w") # Enter NEW file location

timestamp = []
for line in f:
    line = re.sub("\n", " ", line)
    match = re.search('(\d+/\d+/\d+, \d+:\d+)', line)
    if match:
        timestamp.append(match.group(1))
    line = re.sub("(\d+/\d+/\d+, \d+:\d+ - )", "\n", line)
    #line = line.strip()
    #line = re.sub(": ", "\n", line)
    fw.write(line)
f.close()
fw.close()

#%%

f = codecs.open('','r', encoding='UTF-8') # Enter the NEW file location created (fw)
lines= f.readlines()
df = pd.DataFrame({'lines': lines})
df = df.iloc[1:]
df['timestamp'] = timestamp
df['name'], df['message']= df['lines'].str.split(': ', 1).str
df = df.drop('lines', 1)
df = df.iloc[1:]
df['message'] = df['message'].str[:-3]

#%%
writer = pd.ExcelWriter('', engine='xlsxwriter',options={'strings_to_urls': False}) # Enter xlsx file name & path
df.to_excel(writer)
writer.close()

