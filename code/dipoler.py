"""Calculates the expected mu given a set of ra, decs, a dipole direction and magnitude (and zs)."""

from pylab import *

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

def unit(ra, dec):
    d = dec + pi/2 #because we get dec in -pi/2 -> pi/2
    return array([sin(d)*cos(ra), sin(d)*sin(ra), cos(d)])

def muthdip(mu, ra, dec, dipra, dipdec, strength):
    dipole = unit(dipra, dipdec)
    sne = unit(ra, dec)
    return mu*(1 + strength*dot(dipole, sne))
    