""" Sorting module for Supernova Cosmology

Takes Union2.1 Data and whole-sky supernovae data to find positions of U2.1 SNe.

Sorts by name """

import numpy as np

class dataset(object):

    def __init__(self):
        self.union_url = "http://supernova.lbl.gov/union/figures/SCPUnion2.1_mu_vs_z.txt"
        self.union_delim = "\t"
        self.total_url = "../data/all_rawdata.csv"
        self.total_delim = "\t"
        self._get_raw()
        self._get_names()
        self._get_mu()
        self._get_mu_err()
        self._get_z()
        self._get_ra_dec()

        return

    
    def _get_raw(self):
        self.union_rawdata = np.loadtxt(self.union_url, delimiter=self.union_delim)
        self.all_rawdata = np.loadtxt(self.total_url, delimiter=self.total-delim)

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
        total_rawnames = self.union_rawdata[:,0]
        indicies = np.array_like(self.names)

        for i in range(len(names)):
            indicies[i] = total_rawnames.index(names[i])

        return indicies


    def _get_ra_dec(self):
        self.ra = np.array_like(names)
        self.dec = np.array_like(names)

        indicies = __get_name_indicies()

        for i in range(len(self.ra)):
            self.ra[i] = self.union_rawdata[indicies[i],3]
            self.dec[i] = self.union_rawdata[indicies[i],4]

        return


if __name__ == "__main__":
    data = dataset()
    print(data.ra())
