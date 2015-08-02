# -*- coding: utf-8 -*-
import tomopy
import numpy as np
import time, datetime
import sys, getopt

def main(argv):
    try:        opts, args = getopt.getopt(argv,"hc:s:",["core=","sino="])    except getopt.GetoptError:        print 'test.py -c <ncore> -s <nsino>'        sys.exit(2)    for opt, arg in opts:        if opt == '-h':            print 'test.py -c <ncore> -s <nsino>'            sys.exit()        elif opt in ("-c", "--core"):            ncore = int(arg)        elif opt in ("-s", "--sino"):            nsino = int(arg)
    file_name = '/local/decarlo/data/proj_10.hdf'
    output_name = './recon/proj10_rec'
    sino_start = 0
    sino_end = 2160

    step_00 = time.time()
    while (sino_start <= (sino_end - nsino)):
        # Read HDF5 file.
        prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(sino_start, sino_start+nsino))

        # Fix flats because sample did not move
        flat = np.full((flat.shape[0], flat.shape[1], flat.shape[2]), 1000)

        # Set angles
        theta  = tomopy.angles(prj.shape[0])

        # normalize the prj
        prj = tomopy.normalize(prj, flat, dark)

        best_center = 1298
        step_01 = time.time()

        # reconstruct 
        rec = tomopy.recon(prj, theta, center=best_center, algorithm='gridrec', emission=False, ncore = ncore)

        step_02 = time.time()
        step_02_delta = step_02 - step_01
        print prj.shape[1], prj.shape[2], prj.shape[0], ncore, str(datetime.timedelta(seconds=int(step_02_delta))), int(step_02_delta)
        #tomopy.io.writer.write_tiff_stack(rec, fname=output_name)        
        sino_start = sino_start + nsino
    step_03 = time.time()    
    step_03_delta = step_03 - step_00
    print "*", prj.shape[1], prj.shape[2], prj.shape[0], ncore, str(datetime.timedelta(seconds=int(step_03_delta))), int(step_03_delta)

if __name__ == "__main__":   main(sys.argv[1:])
   
   
