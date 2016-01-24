""" Sorting module for Supernova Cosmology

Takes Union2.1 Data and whole-sky supernovae data to find positions of U2.1 SNe.

Sorts by name """

import numpy as np
import csv
from astropy import units as u
from astropy.coordinates import SkyCoord

class dataset(object):

    def __init__(self):
        self.union_url = "../data/SCPUnion2.1_mu_vs_z.txt"
        self.union_delim = "\t"
        self.total_url = "../data/all_rawdata_parsed_v2.csv"
        self.total_delim = ","
        self._get_raw()
        self._get_names()
        self._get_mu()
        self._get_mu_err()
        self._get_z()
        self._get_ra_dec()

        return

    
    def _get_raw(self):
        self.union_rawdata = np.loadtxt(self.union_url, delimiter=self.union_delim, dtype=object)
        
        # I realise this is convoluted but this IAU data was *awful*.
        self.total_rawdata = []

        with open(self.total_url, 'rb') as total:
            myreader = csv.reader(total, delimiter=self.total_delim, quotechar="\"")
            for row in myreader:
                self.total_rawdata.append(row)

        self.total_rawdata = np.array(self.total_rawdata, dtype=str)

        return


    def _get_names(self):
        self.names = self.union_rawdata[:,0]

        return

    
    def _get_z(self):
        self.z = self.union_rawdata[:,1]
        
        return

    
    def _get_mu(self):
        self.mu = self.union_rawdata[:,2]

        return


    def _get_mu_err(self):
        self.mu_err = self.union_rawdata[:,3]

        return


    def __get_name_indicies(self):
        """Finds the row numbers where names appear from U2.1 in all dataset so
        we can extract the ra/dec"""
        total_rawnames = list(self.total_rawdata[:,0])
        rawnames = list(self.union_rawdata[:,0])
        indicies = []
        names = []

        for name in rawnames:
            try:
                indicies.append(total_rawnames.index(name.upper()))
                names.append(name)
            except ValueError:
                try:
                    indicies.append(total_rawnames.index(name))
                    names.append(name)
                except ValueError:
                    print("Could not find %s in catalogue. Skipping" % name)
        
        self.names = np.array(names)  # if some not in catalogue

        return np.array(indicies)


    def _get_ra_dec(self):
        self.ra = np.empty_like(self.names)
        self.dec = np.empty_like(self.names)
        
        indicies = self.__get_name_indicies()

        for i in range(len(indicies)):
            current_index = indicies[i]
            self.ra[i] = self.total_rawdata[current_index,1]
            self.dec[i] = self.total_rawdata[current_index,2]

        return

    
    def __clean_ra_dec(self):
        clean_ra_dec = np.empty_like(self.ra, dtype=SkyCoord)

        for i in range(len(self.ra)):
            numbers = 0
            for item in self.ra[i].split(" "):
                if item and numbers == 0:
                    hours = float(item)
                    numbers += 1
                elif item and numbers == 1:
                    mins = float(item)
                    numbers += 1
                elif numbers == 2:
                    break
                else:
                    continue
                
            numbers = 0
            for item in self.dec[i].split(" "):
                if item and numbers == 0:
                    deg = float(item)
                    numbers += 1
                elif item and numbers == 1:
                    am = float(item)
                    numbers += 1
                elif numbers == 2:
                    break
                else:
                    continue


            clean_ra_dec[i] = SkyCoord('%2.0fh%2.1fh' % (hours, mins), '%2.0fd%2.0fm' % (deg, am))

        self.clean_ra_dec = clean_ra_dec

        return



if __name__ == "__main__":
    data = dataset()
    self.clean_ra_dec()
    print(clean_ra_dec)


