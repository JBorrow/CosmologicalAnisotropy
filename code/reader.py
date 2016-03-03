from pylab import *

import pandas



# -------------------------------- COSMOLOGY FUNCTIONS ---------------------------------------

h0 = 2.27e-18
sol = 3e08
omegam = 0.2889

def muth(lumdist):
    return 5*log10(lumdist/3.09e17)  # dl in pc

def mu(lumdist, nhat, dipole):
    return muth(lumdist)*(1+dot(nhat, dipole))

import scipy.integrate as si

def dl(z, omegam):
    myint = si.quad(integrand, 0, z, args=(omegam))
    
    return 3e08*((1+z)/(h0))*myint[0]

def integrand(z, omegam):
    return 1/E(z, omegam)

def E(z, omegam):
    return sqrt(omegam*(1+z)**3 + (1-omegam))

# ----------------------------------- READING SCRIPT -----------------------------------------

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

for heading in headings:  # this doesn't actually work bro
    if heading in ['SNTYPE', 'SURVEY', 'name', 'LCSRC_0']:
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

# correct SDSS data

corrected = array(jla.loc[jla['SURVEY']=='SDSS']['RA'], dtype=float) + 180
jla.loc[jla['SURVEY']=='SDSS', 'RA'] = corrected

# now convert to different data types

for heading in headings:
    if heading in ['SNTYPE', 'SURVEY', 'name', 'LCSRC_0']:
        jla[heading] = jla[heading].astype(str)
    else:
        jla[heading] = jla[heading].astype(float)
        

# ---------------------------------------------- EXPORT TO LOCAL ARRAYS ------------------------------------
        
zs = array(jla['z'])
mus = array(jla['msb']) + 19.2
mues = array(jla['msbe'])
ras = array(jla['RA'])
decs = array(jla['DEC'])
radra, raddec = (ras-180)*(pi/180), decs*(pi/180)
