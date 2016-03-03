"""Module for finding anisotropies in supernovae data"""

import pylab as pl

def rotatera(inarray, delta):
    """Angles in 0, 2pi please.
    
    Changes the centre of the 'array' from 0 to delta."""

    toobig = inarray + delta
    wheretoobig = toobig > 2*pl.pi

    return toobig - 2*pl.pi*wheretoobig

def rotatedec(inarray, delta):
    """Same as above but for ra"""

    toobig = inarray + delta
    wheretoobig = toobig > pl.pi/2

    return toobig - pl.pi*wheretoobig 


from scipy.stats import pearsonr

def joshr(x1, x2, y):
    """Returns the two dimensional pearsonr:

        R(x1, x2, y) = 0.5 * (|r(x1, y)| + |r(x2, y)|)

    """

    r1 = pearsonr(x1, y)
    r2 = pearsonr(x2, y)
    return 0.5*(abs(r1[0])+abs(r2[0]))


def joshrwithrot(rotation, dmu, ra, dec):
    rotra = rotation[0]
    rotdec = rotation[1]
    return joshr(rotatera(ra, rotra), rotatedec(dec, rotdec), dmu)


def magrwithrot(rotation, dmu, ra, dec):
    rotra = rotation[0]
    rotdec = rotation[1]
    return pearsonr((rotatera(ra, rotra)**2 + rotatedec(dec, rotdec)**2)**0.5, dmu)[0]


def arrayofanis(ra, dec, dmu, method=joshrwithrot):
    """Gets a 2d array of anisotropies, like the one presented in the poster"""

    # ra, dec
    inputs = pl.mgrid[0:360,0:180].swapaxes(0,2).swapaxes(0,1)*(2*pl.pi/360)
    outputs = pl.empty_like(inputs[:,:,0])

    for i in range(len(inputs[0,:])):
        for j in range(len(inputs[:,0])):
            outputs[j,i] = method(inputs[j,i], dmu, ra, dec)

    return outputs


if __name__=="__main__":
    # Test with linearly correlated data
    
    inputra = pl.arange(0, 2*pl.pi, 0.01)
    inputdec = pl.arange(-0.5*pl.pi, 0.5*pl.pi, 0.005)
    dmu = inputra
    output = arrayofanis(inputra, inputdec, dmu).T
    
    pl.imshow(output)
    pl.colorbar()
    pl.show()
