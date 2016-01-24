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
        self.union_rawdata
        self.all_rawdata
        self.names
        self.mu
        self.z
        self.z_err
        self.ra
        self.dec

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
