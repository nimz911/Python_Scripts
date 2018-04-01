import re
import urllib
import os
import numpy


artist = 'Titian'
print artist

if os.path.isdir('artist') == False:
    os.mkdir('artist')
if os.path.isdir('artist/'+artist) == False:
    os.mkdir('artist/'+artist)

urllib.urlretrieve('http://totallyhistory.com/art-history/famous-artists/', 'artist/mainpage.html')
file = open('mainpage.html', 'r')
out = open('artist/' + artist+'.html', 'w')
start = False
for line in file:
    line = line.strip()
    artist_url = re.sub('\W+', '-' ,artist)
    regex_start = 'href="http://totallyhistory.com/'+artist_url+'/">'
    #print regex_start
    match = re.search(regex_start, line, re.IGNORECASE) 
    if match:
        start = True
    match = re.search('</div>', line, re.IGNORECASE) 
    if match:
        start = False
    if start and len(line) > 0:
        line = re.sub('<[^>]+>', ' ', line) 
        out.write(line + '\n')
file.close()
out.close()

file = open('artist/' + artist+'.html', 'r')
for line in file:
    line = line.strip()
    if len(line) < 100 and len(line) > 1:
        title = re.sub('\W+', '-' ,line)
        url = 'http://totallyhistory.com/' + title
        urllib.urlretrieve( url , 'artist/' + artist + '/' + title +'.html')
        
file.close()

#%%

filenames = os.listdir('artist/'+artist)
print filenames
start = False
dimension = []
for filename in filenames:
    file = open('artist/'+ artist +'/'+ filename, 'r')
    for line in file:
        line = line.strip()
        line = line.lower()
        match = re.search('<th>Dimensions</th>', line, re.IGNORECASE)
        if match:
            start = True
        match = re.search('</table>', line, re.IGNORECASE)
        if match:
            start = False
        if start:
            match = re.search('(.+)×(.+) cm', line, re.IGNORECASE)
            if match:
                size1 = re.sub(' cm','',match.group(1))
                size1 = float(re.sub('<td>','', size1))
                size2 = float(match.group(2))
                sum1 = size1 + size2
                print 'size: ', size1 , ' x ' , size2, '   /   sum = ' , sum1
                dimension.append(sum1)
            match = re.search('(.+) x (.+) cm</td>', line, re.IGNORECASE)
            if match:
                size1 = float(match.group(1))
                size2 = float(match.group(2))
                sum2 = size1 + size2
                print 'size: ', size1 , ' x ' , size2, '  /   sum = ' , sum2
                dimension.append(sum2)
            match = re.search('>(.+) x (.+) cm<', line, re.IGNORECASE)
            if match:
                size1 = float(match.group(1))
                size2 = float(match.group(2))
                sum3 = size1 + size2
                print 'size: ', size1 , ' x ' , size2, '    /   sum = ' , sum3
                dimension.append(sum3)
    file.close()

print 'mean = ' , numpy.mean(dimension)
print 'STD = ' , numpy.std(dimension)


