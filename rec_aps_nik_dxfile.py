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

    attenuator_name = 'filter set in 2-BM-A'
    attenuator_description = '1mm C + 1mm Glass'
   
    experiment_prosal = '41928'
    experiment_activity = '104291'
    experiment_title = '4D Dynamics of Stress Corrosion Cracking in High Performance Aluminum Alloy'

    experimenter_name = 'Nikhilesh Chawla'
    experimenter_role = 'PI'
    experimenter_affiliation = 'Arizona State University'
    experimenter_address = 'School for Engineering of Matter, Transport, and Energy (SEMTE), 501 E. Tyler Mall, ECG 303, Tempe, AZ 85287-6106'
    experimenter_phone = '(480) 965-2402'
    experimenter_email = 'Nikhilesh.Chawla@asu.edu'

    instrument_name = '2-BM fast tomography'  
    instrument_comment = '2-BM-A Experimental Station'  
    
    acquisition_setup_rotation_start_angle = 0
    acquisition_setup_rotation_end_angle = 180
    acquisition_setup_rotation_speed = 0.750

    objective_name = 'Mitutoyo long-working'
    objective_description = 'a nice objective'
    objective_manufacturer = 'Mitutoyo'
    objective_magnification = '10x'

    detector_name = 'PCO edge'
    detector_exposure_time = 0.0001
    detector_shutter_mode = 'global'
    detector_pixel_size_x = 0.65e-4
    detector_pixel_size_y = 0.65e-4
    detector_actual_pixel_size_x = 0.65
    detector_actual_pixel_size_y = 0.65

    acquisition_setup_number_of_projections = 1500
    acquisition_setup_number_of_darks = 10
    acquisition_setup_number_of_whites = 10
    acquisition_setup_mode = 'fly-scan'
    
    scintillator_name = 'LuAG' 
    scintillator_scintillating_thickness = 10

    mirror_name = '2-BM-A mirror'
    mirror_description = 'Pt coating'
    mirror_angle = 2.657

    monochromator_name = '2-BM-A DMM'
    monochromator_description = 'Double Multi-layer Monochromator'
    monochromator_energy = 27.4
    monochromator_energy_units = 'keV'
       
    # Set path to the micro-CT data to reconstruct.
    fname = '/local/decarlo/data/tomobank/' + sample_name + '_' + fatigue_cycle + 'C'  + '.h5'

    # Select the sinogram range to reconstruct.
    start = 1022
    end = 1024

    sino=(start, end)

    proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=(start, end))

        
#    theta = np.linspace(0., 180., proj.shape[0]+1)
    
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
