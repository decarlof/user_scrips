#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to read APS 2-BM 
"""

from __future__ import print_function
import os
import tomopy
import numpy as np
import dxchange
import dxchange.reader as dxreader
import dxfile.dxtomo as dx

if __name__ == '__main__':


    data_index = 106
    sample_name = 'H14_7075PA_172HV_99NF'
    fatigue_cycle = '10000'
    
    sample_detector_distance = 60

    detector_pixel_size_x = 0.65e-4
    detector_pixel_size_y = 0.65e-4
    monochromator_energy = 27.4
    monochromator_energy_units = 'keV'
       
    # Set path to the micro-CT data to reconstruct.
    fname_proj = '/local/decarlo/data/tomobank/' + sample_name + '_' + fatigue_cycle + 'C' + '/' + 'proj_' + "{:04d}".format(data_index) + '.hdf'
    fname_flat = '/local/decarlo/data/tomobank/' + sample_name + '_' + fatigue_cycle + 'C' + '/' + 'proj_' + "{:04d}".format(data_index+1) + '.hdf'
    fname_dark = '/local/decarlo/data/tomobank/' + sample_name + '_' + fatigue_cycle + 'C' + '/' + 'proj_' + "{:04d}".format(data_index+2) + '.hdf'
    fname = '/local/decarlo/data/tomobank/' + sample_name + '_' + fatigue_cycle + 'C'  + '.h5'

    # Select the sinogram range to reconstruct.
    start = 1022
    end = 1024

    sino=(start, end)

    exchange_base = "exchange"
    proj_grp = '/'.join([exchange_base, 'data'])
    flat_grp = '/'.join([exchange_base, 'data'])
    dark_grp = '/'.join([exchange_base, 'data'])
    
    print (proj_grp)
    print (fname_proj)
    
    acquisition_start_date = dxreader.read_hdf5(fname_proj, '/file_creation_datetime')
    print (acquisition_start_date[0][0])

    proj = dxreader.read_hdf5(fname_proj, proj_grp, slc=(None, sino), dtype=None)
    flat = dxreader.read_hdf5(fname_flat, flat_grp, slc=(None, sino), dtype=None)
    dark = dxreader.read_hdf5(fname_dark, dark_grp, slc=(None, sino), dtype=None)
      
    theta = np.linspace(0., 180., proj.shape[0]+1)
    
    number_of_projections = proj.shape[0]
    detector_dimension_y = proj.shape[1]
    detector_dimension_x = proj.shape[2]
    
    print (proj.shape)
    print (flat.shape)
    print (dark.shape)
    print (theta.shape)

    
    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark)

    # remove stripes    
    data = tomopy.prep.stripe.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)

    # phase retrieval
    data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=8e-3,pad=True)

    # Find rotation center.
    rot_center = 1235
    print("Center of rotation: ", rot_center)

    data = tomopy.minus_log(data)

    theta = tomopy.angles(proj.shape[0])

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='recon_dir/aps_nik')
