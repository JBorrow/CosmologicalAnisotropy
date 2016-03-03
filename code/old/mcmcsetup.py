from jla_data_fix import *
import pymc as pymc
import scipy.integrate as si


hubble = 2e-18
sol=3e08


allz = hstack(zs)
allmsb = hstack(msbs)
allmsbe = hstack(msbes)


# In[24]:

# Cosmology Functions

def friedmann(z, omegaB):
    model = omegaB * ((1+z)**3) + (1-omegaB)
    
    return sqrt(model)


def integrand(x, b):
    return friedmann(x, b)**(-1)


def sk(z, omegaB):
    return float((si.quad(integrand, 0, z, args=(omegaB)))[0])


def lumdist(z, omegaB):
    return sk(z, omegaB) * (sol/hubble)


def flux(z, omegaB, lpeak):
    return 1e39*lpeak/(4 * np.pi * (lumdist(z, omegaB)*(1+z))**2)


def msbcalc(z, omegaB, lpeak):
    return -20.45 - 2.5*log10(1E-4 * flux(z, omegaB, lpeak))

vecmsbcalc = vectorize(msbcalc)


# In[25]:

omegaB = pymc.Uniform('omegaB', 0, 1, value=0.3)
leff = pymc.Uniform('leff', 0, 100, value=2)

@pymc.deterministic(plot=False)
def mymsb(z=allz, b=omegaB, l=leff):
    return vecmsbcalc(z, b, l)

y = pymc.Normal('y', mu=mymsb, tau=1./(allmsbe)**2, value=allmsb, observed=True)
