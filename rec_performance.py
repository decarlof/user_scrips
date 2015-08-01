# -*- coding: utf-8 -*-
"""
.. module:: rec_DAC.py
   :platform: Unix
   :synopsis: Reconstruct the DAC experiment data collected at the APS 32-ID TXM

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

"""
# tomoPy: https://github.com/tomopy/tomopy
import tomopy
import numpy as np
import matplotlib.pylab as pl
import time, datetime

def rec_test(file_name, sino_start, sino_end):

    print '\n#### Processing '+ file_name
    sino_start = sino_start + 200
    sino_end = sino_start + 100
    print "Test reconstruction of slice [%d]" % sino_start
    # Read HDF5 file.
    prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(sino_start, sino_end))

    # Fix flats because sample did not move
    flat = np.full((flat.shape[0], flat.shape[1], flat.shape[2]), 1000)

    # Create angle
    theta  = tomopy.angles(prj.shape[0])

    # normalize the prj
    prj = tomopy.normalize(prj, flat, dark, ncore = 12)

    # reconstruct 
    rec = tomopy.recon(prj, theta, center=best_center, algorithm='gridrec', emission=False, ncore = 12)
        
    # Write data as stack of TIFs.
    tomopy.io.writer.write_tiff_stack(rec, fname=output_name)

    print "Slice saved as [%s_00000.tiff]" % output_name
    # show the reconstructed slice
    pl.gray()
    pl.axis('off')
    pl.imshow(rec[0])
    
def rec_full(file_name, sino_start, sino_end):

    start_time = time.time()

    print '\n#### Processing '+ file_name
    chunks = 20 # number of data chunks for the reconstruction

    while (chunks <=60):
        nSino_per_chunk = (sino_end - sino_start)/chunks
        print "Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk)

        print '\n', datetime.datetime.today()
    #    for iChunk in range(0,chunks):
        for iChunk in range(0,1):
            print '\n  -- chunk # %i' % (iChunk+1)
            sino_chunk_start = sino_start + nSino_per_chunk*iChunk 
            sino_chunk_end = sino_start + nSino_per_chunk*(iChunk+1)
            print '\n  --------> [%i, %i]' % (sino_chunk_start, sino_chunk_end)
            
            if sino_chunk_end > sino_end: 
                break
                    
            step_00 = time.time()

            # Read HDF5 file.
            prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(sino_chunk_start, sino_chunk_end))

            step_01 = time.time()
            step_01_delta = step_01 - step_00
            print "**********************"        
            print "Read Raw:     ", str(datetime.timedelta(seconds=int(step_01_delta)))
            print "**********************"        


            # Fix flats because sample did not move
            flat = np.full((flat.shape[0], flat.shape[1], flat.shape[2]), 1000)

            # Set angles
            theta  = tomopy.angles(prj.shape[0])

            step_02 = time.time()

            # normalize the prj
            prj = tomopy.normalize(prj, flat, dark)

            step_03 = time.time()
            step_03_delta = step_03 - step_02
            print "**********************"        
            print "Normalize:    ", str(datetime.timedelta(seconds=int(step_03_delta))), int(step_03_delta)
            print "**********************"        

            ncore  = 2
            while (ncore <= 24):
                step_03 = time.time()
                # reconstruct 
                rec = tomopy.recon(prj, theta, center=best_center, algorithm='gridrec', emission=False, ncore = ncore)

                step_04 = time.time()
                step_04_delta = step_04 - step_03
                print nSino_per_chunk, prj.shape[0], prj.shape[1], prj.shape[2], ncore, str(datetime.timedelta(seconds=int(step_04_delta))), int(step_04_delta)
                ncore += 2

            #step_04 = time.time()
            #step_04_delta = step_04 - step_03
            print "**********************"        
            #print "Reconstruct ncore ", ncore, str(datetime.timedelta(seconds=int(step_04_delta)))
            #print "**********************"        
            #step_04 = time.time()

            #tomopy.io.writer.write_tiff_stack(rec, fname=output_name, start=sino_chunk_start)

            #step_05 = time.time()
            #step_05_delta = step_05 - step_04
            #print "**********************"        
            #print "Write:        ", str(datetime.timedelta(seconds=int(step_05_delta)))
            #print "**********************"        

            #step_06 = time.time()
            #step_06_delta = step_06 - step_00
            #print "**********************"        
            #print "Chunk:        ", str(datetime.timedelta(seconds=int(step_06_delta)))
            #print "**********************"        
            
            chunks +=20

    end_time = time.time()
    uptime = end_time - start_time
    print "******************"        
    print "Total:       ", str(datetime.timedelta(seconds=int(uptime)))
    print "******************"        

reconstruction_test = False

##################################### Inputs ##########################################################
file_name = '/local/dataraid/databank/templates/aps_2-BM/hdf5/proj_10.hdf' # best_center = 1232
output_name = './recon/proj10_rec'
best_center = 1298; sino_start = 0; sino_end = 2560;
if reconstruction_test: rec_test(file_name, sino_start, sino_end)
else: rec_full(file_name, sino_start, sino_end)


