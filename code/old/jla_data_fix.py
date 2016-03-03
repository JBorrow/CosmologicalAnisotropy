
# coding: utf-8

# In[39]:

get_ipython().magic('pylab inline')

import pandas
import numpy as np
from numpy import *
from matplotlib.pyplot import *
import pylab
from pylab import *

ducolors=['#321F20', '#7E317B', '#D8ACE0', '#006388', '#AA2B4A', '#CFDAD1', '#C4E5FA', '#C43B8E', '#91B8BD', '#968E85']


# In[40]:

with open("../data/jla_data_toconvert.txt", 'r') as jlaraw:
    jlarawstr = jlaraw.read()
    
jlarawlines = jlarawstr.split("\n")

i = 0
headings = []
while (jlarawlines[i] != r"#end"):
    thisline = jlarawlines[i]
    i+=1
    if thisline[0] == r"@":
        continue
    else:
        headings.append(thisline[1:-1])
        
#SNTYPE, SURVEY and name have str type but all others have float type
types = []

for heading in headings:
    if heading in ['STNYPE', 'SURVEY', 'name']:
        types.append(np.str_)
    else:
        types.append(np.float_)

# now we actually need to parse data into an array. This is going to be very messy. Sorry, future me if this breaks.
fulllist = []

for line in jlarawlines:
    if line:
        if (line[0]=='#') or (line[0]=='@'):
            continue
        else:
            thisarry = np.empty_like(types)
            thislist = line.split("  ")
            for i in range(len(thisarry)):
                thisarry[i] = thislist[i]
        
            fulllist.append(thisarry)
            

fullarray = np.array(fulllist)

jla = pandas.DataFrame(data=fullarray, columns=headings)


# In[41]:

def ra(survey, correction=0, df=jla):
    # gets ra from jla data, corrects by correction in deg. returns in rads
    return (array(df.loc[df['SURVEY']==survey]['RA'], dtype=float) - correction)*(pi/180)


def dec(survey, correction=0, df=jla):
    # same as above but dec. correction is always 0
    return (array(df.loc[df['SURVEY']==survey]['DEC'], dtype=float) - correction)*(pi/180)


def z(survey, df=jla):
    # gets ra from jla data, corrects by correction in deg. returns in rads
    return array(df.loc[df['SURVEY']==survey]['z'], dtype=float)


def msb(survey, df=jla):
    # gets ra from jla data, corrects by correction in deg. returns in rads
    return array(df.loc[df['SURVEY']==survey]['msb'], dtype=float)


def msbe(survey, df=jla):
    # gets ra from jla data, corrects by correction in deg. returns in rads
    return array(df.loc[df['SURVEY']==survey]['msbe'], dtype=float)



surveys = ['SDSS', 'SNLS', 'RiessHST', 'CalanTololo', 'CfAI', 'CfAII', 'CfAIII', 'lowz', 'CSP']
ra_corr = [0, 180, 180, 180, 180, 180, 180, 180, 180]
dec_corr = [0] * len(ra_corr)


# In[42]:

# separate all data by survey for sick plots
ras = empty(len(surveys), dtype=object)
decs = empty(len(surveys), dtype=object)
zs = empty(len(surveys), dtype=object) 
msbs = empty(len(surveys), dtype=object)
msbes = empty(len(surveys), dtype=object)

for i in range(len(surveys)):
    survey = surveys[i]
    ras[i] = ra(survey, correction=ra_corr[i])
    decs[i] = dec(survey, correction=dec_corr[i])
    zs[i] = z(survey)
    msbs[i] = msb(survey)
    msbes[i] = msbe(survey)





