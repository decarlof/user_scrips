# -*- coding: utf-8 -*-
"""
.. module:: validateRecDataExchange2tomoPy.py
   :platform: Unix
   :synopsis: validate data exchange conversion by running tomopy
   :INPUT
      data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>

:Version: 2014.01.19

""" 
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 


import matplotlib.pyplot as plt

def main():
    #****************************************************************************
    file_name = '/local/dataraid/databank/dataExchange/tmp/Australian_rank3.h5'
    output_name = '/local/dataraid/databank/dataExchange/tmp/rec/Australian_rank3'    
    sino_start = 290    
    sino_end = 294    

    # Read HDF5 file.
    exchange_rank = 3;
    prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, exchange_rank, sino=(sino_start, sino_end))
    theta  = tomopy.angles(prj.shape[0])

    # normalize the data
    prj = tomopy.normalize(prj, flat, dark)

    best_center=1184
    print "Best Center: ", best_center
    calc_center = best_center
    #calc_center = tomopy.find_center(prj, theta, emission=False, ind=0, init=best_center, tol=0.8)
    print "Calculated Center:", calc_center
    
    # reconstruct 
    rec = tomopy.recon(prj, theta, center=calc_center, algorithm='gridrec', emission=False)
    #rec = tomopy.circ_mask(rec, axis=0)
    
    # Write data as stack of TIFs.
    tomopy.io.writer.write_tiff_stack(rec, fname=output_name)
    plt.gray()
    plt.axis('off')
    plt.imshow(rec[0])

if __name__ == "__main__":
    main()

