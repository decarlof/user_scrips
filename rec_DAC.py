# -*- coding: utf-8 -*-
import tomopy
import numpy as np
import matplotlib.pylab as pl
import h5py

def rec_test(file_name, sino_start, sino_end):

    print '\n#### Processing '+ file_name
    sino_start = sino_start + 200
    sino_end = sino_start + 2
    print "Test reconstruction of slice [%d]" % sino_start
    # Read HDF5 file.
    prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(sino_start, sino_end))

    # Manage the missing angles:
    theta  = tomopy.angles(prj.shape[0])
    prj = np.concatenate((prj[0:miss_angles[0],:,:], prj[miss_angles[1]+1:-1,:,:]), axis=0)
    theta = np.concatenate((theta[0:miss_angles[0]], theta[miss_angles[1]+1:-1]))

    # normalize the prj
    prj = tomopy.normalize(prj, flat, dark)

    # reconstruct 
    rec = tomopy.recon(prj, theta, center=best_center, algorithm='gridrec', emission=False)
        
    # Write data as stack of TIFs.
    tomopy.io.writer.write_tiff_stack(rec, fname=output_name)

    print "Slice saved as [%s_00000.tiff]" % output_name
    # show the reconstructed slice
    pl.figure(figsize=(10,8))    
    pl.imshow(rec[0])
    pl.axis('off')
    
def rec_full(file_name, sino_start, sino_end):

    print '\n#### Processing '+ file_name

    chunks = 10 # number of data chunks for the reconstruction[/local/dataraid/2014_11/haozhe/rec/Ce6Al4_3kbar/Ce6Al4_3kbar_rec

    nSino_per_chunk = (sino_end - sino_start)/chunks
    print "Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk)
    
    for iChunk in range(0,chunks):
        print '\n  -- chunk # %i' % (iChunk+1)
        sino_chunk_start = sino_start + nSino_per_chunk*iChunk 
        sino_chunk_end = sino_start + nSino_per_chunk*(iChunk+1)
        print '\n  --------> [%i, %i]' % (sino_chunk_start, sino_chunk_end)
        
        if sino_chunk_end > sino_end: 
            break
                
        # Read HDF5 file.
        prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(sino_chunk_start, sino_chunk_end))

        # Manage the missing angles:
        theta  = tomopy.angles(prj.shape[0])
        prj = np.concatenate((prj[0:miss_angles[0],:,:], prj[miss_angles[1]+1:-1,:,:]), axis=0)
        theta = np.concatenate((theta[0:miss_angles[0]], theta[miss_angles[1]+1:-1]))

        # normalize the prj
        prj = tomopy.normalize(prj, flat, dark)

        # reconstruct 
        rec = tomopy.recon(prj, theta, center=best_center, algorithm='gridrec', emission=False)
        
        # Write data as stack of TIFs.
        tomopy.io.writer.write_tiff_stack(rec, fname=output_name)
    

def rec_whole(file_name):

    print '\n#### Processing '+ file_name

    chunks = 30 # number of data chunks for the reconstruction

    f = h5py.File(file_name, "r"); 
    nProj, nSino, nCol = f["/exchange/data"].shape
    nSino_per_chunk = nSino/chunks
    print "Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk)
    
    for iChunk in range(0,chunks):
        print '\n  -- chunk # %i' % (iChunk+1)
        sino_chunk_start = nSino_per_chunk*iChunk 
        sino_chunk_end = nSino_per_chunk*(iChunk+1)
        print '\n  --------> [%i, %i]' % (sino_chunk_start, sino_chunk_end)
        
        if sino_chunk_end > sino_end: 
            break
                
        # Read HDF5 file.
        prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(sino_chunk_start, sino_chunk_end))

        # Manage the missing angles:
        theta  = tomopy.angles(prj.shape[0])
        prj = np.concatenate((prj[0:miss_angles[0],:,:], prj[miss_angles[1]+1:-1,:,:]), axis=0)
        theta = np.concatenate((theta[0:miss_angles[0]], theta[miss_angles[1]+1:-1]))

        # normalize the prj
        prj = tomopy.normalize(prj, flat, dark)

        # reconstruct 
        rec = tomopy.recon(prj, theta, center=best_center, algorithm='gridrec', emission=False)
        
        # Write data as stack of TIFs.
        tomopy.io.writer.write_tiff_stack(rec, fname=output_name)
    

reconstruction_test = True

##################################### Inputs ##########################################################
file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_3kbar_.h5' # best_center = 1232
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_3kbar/Ce6Al4_3kbar_rec'
best_center = 1232; sino_start = 740; sino_end = 1700; miss_angles = [141,226]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_5P7kbar_.h5' # best_center = 1321
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_5P7kbar/CCe6Al4_5P7kbar_rec'
best_center = 1321; sino_start = 1000; sino_end = 1440; miss_angles = [141,228]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_8P59GPa_.h5' # best_center = 1219
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_8P59GPa/Ce6Al4_8P59GPa_rec'
best_center = 1219; sino_start = 550; sino_end = 1370; miss_angles = [147,233]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_13P37GPa_.h5' # best_center = 1286
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_13P37GPa/Ce6Al4_13P37GPa_rec'
best_center = 1286; sino_start = 740; sino_end = 1500; miss_angles = [142,227]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_17p44GPa_.h5' # best_center = 1292
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_17p44GPa/Ce6Al4_17p44GPa_rec'
best_center = 1292; sino_start = 620; sino_end = 1320; miss_angles = [140,226]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_19GPa_decrease_.h5' # best_center = 1116
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_19GPa_decrease/Ce6Al4_19GPa_decrease_rec'
best_center = 1116; sino_start = 800; sino_end = 1200; miss_angles = [140,225]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_20kbar_.h5' # best_center = 1314
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_20kbar/Ce6Al4_20kbar_rec'
best_center = 1314; sino_start = 610; sino_end = 1500; miss_angles = [71,113]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_21p39GPa_.h5' # best_center = 1140
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_21p39GPa/Ce6Al4_21p39GPa_rec'
best_center = 1140; sino_start = 610; sino_end = 1200; miss_angles = [140,226]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_26p17GPa_.h5' # best_center = 1124
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_26p17GPa/Ce6Al4_26p17GPa_rec'
best_center = 1124; sino_start = 740; sino_end = 1270; miss_angles = [140,227]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_29P5GPa_decrease_.h5' # best_center = 1338
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_29P5GPa_decrease/Ce6Al4_29P5GPa_decrease_rec'
best_center = 1338; sino_start = 760; sino_end = 1180; miss_angles = [140,227]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_33p07GPa_.h5' # best_center = 1232
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_33p07GPa/Ce6Al4_33p07GPa_rec'
best_center = 1232; sino_start = 710; sino_end = 1210; miss_angles = [140,227]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_41p88GPa_.h5' # best_center = 1292
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_41p88GPa/Ce6Al4_41p88GPa_rec'
best_center = 1292; sino_start = 700; sino_end = 1180; miss_angles = [138,225]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_47p89GPa_.h5' # best_center = 1114
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_47p89GPa/Ce6Al4_47p89GPa_rec'
best_center = 1114; sino_start = 740; sino_end = 1210; miss_angles = [141,228]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_54p73GPa_.h5' # best_center = 1352
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_54p73GPa/Ce6Al4_54p73GPa_rec'
best_center = 1352; sino_start = 750; sino_end = 1230; miss_angles = [138, 224]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)

file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_59GPa_.h5' # best_center = 1352
output_name = '/local/dataraid/2014_11/haozhe/rec/Ce6Al4_59GPa/Ce6Al4_59GPa_rec'
best_center = 1352; sino_start = 630; sino_end = 1100; miss_angles = [138, 224]
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)





