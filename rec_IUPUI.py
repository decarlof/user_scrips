# -*- coding: utf-8 -*-
# Recon a single slice for testing.
import tomopy
import numpy as np
import h5py

##################################### Inputs ##########################################################
file_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Cement/Cement_S3_180proj_500ms_11800eV_new_mount_5_.h5' # best_center = 1142
output_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Cement/Cement_S3_180proj_500ms_11800eV_new_mount_5_recon/Cement_S3_180proj_500ms_11800eV_new_mount_5_recon_'
best_center = 1142

file_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Cement/Cement_S2_180proj_500ms_11800eV_new_mount_7_.h5' # best_center = 1248
output_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Cement/Cement_S2_180proj_500ms_11800eV_new_mount_7_recon/Cement_S2_180proj_500ms_11800eV_new_mount_7_recon_'
best_center = 1248

file_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Amber/Amber_insect_360proj_1s_11800eV_15_.h5' # best_center = 1262
output_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Amber/Amber_insect_360proj_1s_11800eV_15_recon/Amber/Amber_insect_360proj_1s_11800eV_15_recon_'
best_center = 1262

file_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Mongolia_flower/flower_720proj_2s_11800eV_1_.h5' # best_center = 1135
output_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Mongolia_flower/flower_720proj_2s_11800eV_1_recon/flower_720proj_2s_11800eV_1_recon_'
best_center = 1136

file_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Wood_Joseph/Wood_S3_360proj_1s_11800eV_13_.h5' # best_center = 1066
output_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Wood_Joseph/Wood_S3_360proj_1s_11800eV_13_recon/Wood_S3_360proj_1s_11800eV_13_recon_'
best_center = 1066

file_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Wood_Joseph/Wood_S2_360proj_1s_11800eV_11_.h5' # best_center = 1276
output_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Wood_Joseph/Wood_S2_360proj_1s_11800eV_11_recon/Wood_S2_360proj_1s_11800eV_11_recon_'
best_center = 1276

file_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Wood_Joseph/Wood_S1_360proj_1s_11800eV_9_.h5' # best_center = 1238
output_name = '/local/prom04/vdeandrade/dataraid/2015_06/Anne/Wood_Joseph/Wood_S1_360proj_1s_11800eV_9_recon/Wood_S1_360proj_1s_11800eV_9_recon_'
best_center = 1238


medfilt_size = 2
perform_norm = 1 # 1 or 0 to apply or not a flat-field correction
remove_stripe1 = 0 # 1 or 0 to apply or not the stripe removal algo based on wavelet transform
remove_stripe2 = 0 # 1 or 0 to apply or not the stripe removal algo based on wavelet transform
stripe_lvl = 8 # level for the stripe removal algo
sig = 8 # sigma for the stripe removal algo
Wname = 42 #  # wavelet shape for the stripe removal algo
drift_correct = 0
level = 1 # 2^level binning
RingW = 10 # for ring artifact removal M. Rivers algo
chunk = 6 # number of data chunks for the reconstruction
ExchangeRank = 0 # exchange rank corresponding to the dataset
########################################################################################################



print '\n#### Processing '+file_name

#### for 1 slice reconstruction:
#-------------------------------
if 0:
    slice_first = 1500
    # Read HDF5 file.
    #data, white, dark, theta = tomopy.xtomo_reader(file_name,
    #                                               exchange_rank = ExchangeRank,
    #                                               slices_start=slice_first,
    #                                               slices_end=slice_first+1)
    
    data, white, dark = tomopy.io.exchange.read_aps_32id(file_name, 
                                                        exchange_rank=ExchangeRank, 
                                                        sino=(slice_first, slice_first+1))

    theta  = tomopy.angles(data.shape[0])
    
    # Xtomo object creation and pipeline of methods.
    ##d = tomopy.xtomo_dataset(log='debug')
    ##d.dataset(data, white, dark, theta)

    #if perform_norm: d.normalize() # flat & dark field correction
    if perform_norm: data = tomopy.normalize(data, white, dark)

    ##if drift_correct: d.correct_drift()
    if drift_correct: data = tomopy.normalize_bg(data)

    #d.median_filter(size=medfilt_size, axis=0) # Apply a median filter in the projection plane
    data = tomopy.median_filter(data, size=medfilt_size, axis=0)

    #if remove_stripe1: d.stripe_removal(level=stripe_lvl, sigma=sig, wname=Wname)
    if remove_stripe1: data = tomopy.remove_stripe_fw(data, level=stripe_lvl, wname=Wname, sigma=sig)

#    z = 3
#    eng = 31
#    pxl = 0.325e-4
#    rat = 5e-03
#    rat = 1e-03
    #d.phase_retrieval(dist=z, energy=eng, pixel_size=pxl, alpha=rat,padding=True)
    #data = tomopy.retrieve_phase(data, dist=z, energy=eng, pixel_size=pxl, alpha=rat,pad=True)
    
    #if remove_stripe2: d.stripe_removal2()
    if remove_stripe2: data = tomopy.remove_stripe_ti(data)

    #d.downsample2d(level=level) # apply binning on the data
    data = tomopy.downsample(data, level=level) # apply binning on the data
    theta  = tomopy.angles(data.shape[0])
    if 1:
        #if not best_center: d.optimize_center()
        if not best_center: calc_center = tomopy.find_center(data, theta, emission=False, ind=0, tol=0.3)
        else: 
            #d.center=best_center/pow(2,level) # Manage the rotation center
            calc_center = best_center/pow(2,level) # Manage the rotation center
        #d.gridrec(ringWidth=RingW) # Run the reconstruction
        rec = tomopy.recon(data, theta, center=calc_center, algorithm='gridrec', emission=False)
        
        #d.apply_mask(ratio=1)
        rec = tomopy.circ_mask(rec, axis=0)

        # Write data as stack of TIFs.
        #tomopy.xtomo_writer(d.data_recon, output_name, 
        #                    axis=0,
        #                    x_start=slice_first)
        tomopy.io.writer.write_tiff_stack(rec, fname=output_name, axis=0, start=slice_first)

#### for the whole volume reconstruction
if 1:
    f = h5py.File(file_name, "r"); nProj, nslices, nCol = f["/exchange/data"].shape
    nslices_per_chunk = nslices/chunk

    for iChunk in range(0,chunk):
        print '\n  -- chunk # %i' % (iChunk+1)
        slice_first = nslices_per_chunk*iChunk 
        slice_last = nslices_per_chunk*(iChunk+1)
        
        # Read HDF5 file.
        #data, white, dark, theta = tomopy.xtomo_reader(file_name,
        #                                               exchange_rank = ExchangeRank,
        #                                               slices_start=slice_first,
        #                                               slices_end=slice_last)
        data, white, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(slice_first, slice_last))
        theta  = tomopy.angles(data.shape[0])

        print '\n  -- 1st & last slice: %i, %i' % (slice_first, slice_last)
        
        # Xtomo object creation and pipeline of methods.
        ##d = tomopy.xtomo_dataset(log='debug')
        ##d.dataset(data, white, dark, theta)

        #if perform_norm: d.normalize() # flat & dark field correction
        if perform_norm: data = tomopy.normalize(data, white, dark)
        ##if drift_correct: d.correct_drift()

        #d.median_filter(size=medfilt_size, axis=0)
        data = tomopy.median_filter(data, size=medfilt_size, axis=0)
        
        if remove_stripe1:
            #d.stripe_removal_horiz(level=stripe_lvl, sigma=sig, wname=Wname)
            data = tomopy.remove_stripe_fw(data, level=stripe_lvl, wname=Wname, sigma=sig)

        if remove_stripe2: 
            #d.stripe_removal2()
            data = tomopy.remove_stripe_ti(data)

#        d.downsample2d(level=level)
#        d.downsample3d(level=level)
        data = tomopy.downsample(data, level=level) # apply binning on the data
        theta  = tomopy.angles(data.shape[0])

        if 0:
            ## Save modified data into the hdf5 file:
            #data = d.data
            File = h5py.File(file_name, "r+")
            dset = File.create_dataset("/exchange1/data", np.shape(data))
            dset = File['/exchange1/data']
            dset[...] = data
            File.close()
        if 0:
            #tomopy.xtomo_writer(d.data, output_name, 
            #                    axis=1,
            #                    x_start=slice_first)
            tomopy.io.writer.write_tiff_stack(data, fname=output_name, axis=1, start=slice_first)
        if 1:
            #if not best_center: d.optimize_center()
            if not best_center: calc_center = tomopy.find_center(data, theta, emission=False, ind=0, tol=0.3)
            #else: d.center=best_center/pow(2,level) # Manage the rotation center
            else: calc_center = best_center/pow(2,level) # Manage the rotation center 

            #d.gridrec(ringWidth=RingW) # Run the reconstruction
            rec = tomopy.recon(data, theta, center=calc_center, algorithm='gridrec', emission=False)
            #d.apply_mask(ratio=1)
            rec = tomopy.circ_mask(rec, axis=0)

            # Write data as stack of TIFs.
#            tomopy.xtomo_writer(d.data_recon, output_name, 
#                                axis=0,dtype='uint16',
#                                x_start=slice_first)
            #tomopy.xtomo_writer(d.data_recon, output_name, 
            #                    axis=0,
            #                    x_start=slice_first)
            tomopy.io.writer.write_tiff_stack(rec, fname=output_name, axis=0, start=slice_first)



