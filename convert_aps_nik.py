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

    experimenter_name = 'Nikhilesh Chawla Group'
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

#    proj = dxreader.read_hdf5(fname_proj, proj_grp, slc=(None, sino), dtype=None)
#    flat = dxreader.read_hdf5(fname_flat, flat_grp, slc=(None, sino), dtype=None)
#    dark = dxreader.read_hdf5(fname_dark, dark_grp, slc=(None, sino), dtype=None)

    proj = dxreader.read_hdf5(fname_proj, proj_grp, dtype=None)
    flat = dxreader.read_hdf5(fname_flat, flat_grp, dtype=None)
    dark = dxreader.read_hdf5(fname_dark, dark_grp, dtype=None)
        
    theta = np.linspace(0., 180., proj.shape[0]+1)
    
    number_of_projections = proj.shape[0]
    detector_dimension_y = proj.shape[1]
    detector_dimension_x = proj.shape[2]
    
    print (proj.shape)
    print (flat.shape)
    print (dark.shape)
    print (theta.shape)


    if (fname != None):
        if os.path.isfile(fname):
            print ("Data Exchange file already exists: ", fname)
        else:
            # Create new folder.
            dirPath = os.path.dirname(fname)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            # Open DataExchange file
            f = dx.File(fname, mode='w') 

            # Write the Data Exchange HDF5 file.
            f.add_entry(dx.Entry.sample( name={'value':sample_name}))
            f.add_entry(dx.Entry.sample( fatigue_cycle={'value':fatigue_cycle}))
            f.add_entry(dx.Entry.sample_stack_setup(sample_detector_distance={'value':sample_detector_distance, 'units':'mm'}))

            f.add_entry(dx.Entry.attenuator( name={'value':attenuator_name}))
            f.add_entry(dx.Entry.attenuator( description={'value':attenuator_description}))

            f.add_entry(dx.Entry.experiment( proposal={'value':experiment_prosal}))
            f.add_entry(dx.Entry.experiment( activity={'value':experiment_activity}))
            f.add_entry(dx.Entry.experiment( title={'value':experiment_title}))

            f.add_entry(dx.Entry.experimenter(name={'value':experimenter_name}))
            f.add_entry(dx.Entry.experimenter(role={'value':experimenter_role}))
            f.add_entry(dx.Entry.experimenter(affiliation={'value':experimenter_affiliation}))
            f.add_entry(dx.Entry.experimenter(address={'value':experimenter_address}))
            f.add_entry(dx.Entry.experimenter(phone={'value':experimenter_phone}))
            f.add_entry(dx.Entry.experimenter(email={'value':experimenter_email}))

            f.add_entry(dx.Entry.instrument(name={'value':instrument_name}))
            f.add_entry(dx.Entry.instrument(comment={'value':instrument_comment}))

            f.add_entry(dx.Entry.objective(name={'value':objective_name}))
            f.add_entry(dx.Entry.objective(description={'value':objective_description}))
            f.add_entry(dx.Entry.objective(manufacturer={'value':objective_manufacturer}))
            f.add_entry(dx.Entry.objective(magnification={'value':objective_magnification}))
    
            f.add_entry(dx.Entry.acquisition_setup(rotation_start_angle={'value':acquisition_setup_rotation_start_angle, 'units':'deg'}))
            f.add_entry(dx.Entry.acquisition_setup(rotation_end_angle={'value':acquisition_setup_rotation_end_angle, 'units':'deg'}))
            f.add_entry(dx.Entry.acquisition_setup(rotation_speed={'value':acquisition_setup_rotation_speed, 'units':'deg/s'}))
            f.add_entry(dx.Entry.acquisition_setup(number_of_projections={'value':number_of_projections}))

            f.add_entry(dx.Entry.acquisition_setup(number_of_darks={'value':acquisition_setup_number_of_darks}))
            f.add_entry(dx.Entry.acquisition_setup(number_of_whites={'value':acquisition_setup_number_of_whites}))
            f.add_entry(dx.Entry.acquisition_setup(mode={'value':acquisition_setup_mode}))
            f.add_entry(dx.Entry.acquisition(start_date={'value':acquisition_start_date}))

            f.add_entry(dx.Entry.detector(name={'value':detector_name}))
            f.add_entry(dx.Entry.detector(exposure_time={'value':detector_exposure_time}))
            f.add_entry(dx.Entry.detector(shutter_mode={'value':detector_shutter_mode}))
            f.add_entry(dx.Entry.detector(pixel_size_x={'value':detector_pixel_size_x, 'units':'m'}))
            f.add_entry(dx.Entry.detector(pixel_size_y={'value':detector_pixel_size_y, 'units':'m'}))
            f.add_entry(dx.Entry.detector(actual_pixel_size_x={'value':detector_actual_pixel_size_x, 'units':'um'}))
            f.add_entry(dx.Entry.detector(actual_pixel_size_y={'value':detector_actual_pixel_size_y, 'units':'um'}))
            f.add_entry(dx.Entry.detector(dimension_x={'value':detector_dimension_x}))
            f.add_entry(dx.Entry.detector(dimension_y={'value':detector_dimension_y}))

            f.add_entry(dx.Entry.scintillator(name={'value':scintillator_name}))
            f.add_entry(dx.Entry.scintillator(scintillating_thickness={'value':scintillator_scintillating_thickness, 'units':'um'}))

            f.add_entry(dx.Entry.mirror( name={'value':mirror_name}))
            f.add_entry(dx.Entry.mirror( description={'value':mirror_description}))
            f.add_entry(dx.Entry.mirror( angle={'value':mirror_angle, 'units':'rad'}))
            
            f.add_entry(dx.Entry.monochromator( name={'value':monochromator_name}))
            f.add_entry(dx.Entry.monochromator( description={'value':monochromator_description}))
            f.add_entry(dx.Entry.monochromator( energy={'value':monochromator_energy, 'units':'keV'}))

            f.add_entry(dx.Entry.data(data={'value': proj, 'units':'counts'}))
            f.add_entry(dx.Entry.data(data_white={'value': flat, 'units':'counts'}))
            f.add_entry(dx.Entry.data(data_dark={'value': dark, 'units':'counts'}))
            f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

            f.close()
    

