# -*- coding: utf-8 -*-
"""
.. module:: convert_APS_1ID.py
   :platform: Unix
   :synopsis: Convert APS 1-ID TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 1-ID TIFF raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import xtomo_importer as xtomo_imp 
import xtomo_exporter as xtomo_exp

import re
import os.path

def main():

    fname = '/local/dataraid/databank/templates/aps_1-ID/data_'


    fname = os.path.abspath(fname)
    _fname = fname + '000001.tif'
    log_file = os.path.dirname(fname) + os.path.sep + 'TomoStillScan.dat'

    print "file_name: ", fname
    print "file: ", fname
    print "_fname: ", _fname
    print "log_file: ", log_file

    #Read APS 1-ID log file data
    contents = open(log_file, 'r')
    for line in contents:
        ls = line.split()
        if len(ls)>1:
            if (ls[0]=="Tomography" and ls[1]=="scan"):
                prj_start = int(ls[6])
            elif (ls[0]=="Number" and ls[2]=="scan"):
                nprj = int(ls[4])
            elif (ls[0]=="Dark" and ls[1]=="field"):
                dark_start = int(ls[6])
            elif (ls[0]=="Number" and ls[2]=="dark"):
                ndark = int(ls[5])
            elif (ls[0]=="White" and ls[1]=="field"):
                flat_start = int(ls[6])
            elif (ls[0]=="Number" and ls[2]=="white"):
                nflat = int(ls[5])
    contents.close()

    
   
     
##    # these are correct per Peter discussion
##    prj_start = 943
##    prj_end = 1833
##    flat_start = 1844
##    flat_end = 1853
##    dark_start = 1854
##    dark_end = 1863

    print "proj", prj_start, prj_start + nprj
    print "flat", flat_start, flat_start + nflat
    print "dark", dark_start, dark_start + ndark

    ind_tomo = range(prj_start, prj_start + nprj)
    ind_flat = range(flat_start, flat_start + nflat)
    ind_dark = range(dark_start, dark_start + ndark)

  

if __name__ == "__main__":
    main()

