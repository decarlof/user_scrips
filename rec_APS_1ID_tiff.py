# -*- coding: utf-8 -*-
import tomopy
import os.path
import time, datetime

def read_log(fname):

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

    print "    start end"
    print "proj ", prj_start, prj_start + nprj
    print "flat", flat_start, flat_start + nflat
    print "dark", dark_start, dark_start + ndark

def rec_tiff(file_name, sino_start, sino_end, best_center, output_name):

    print '\n#### Processing '+ file_name

    start_time = time.time()
    # Read tiff files.
    prj, flat, dark = tomopy.io.exchange.read_aps_1id(file_name, sino=(sino_start, sino_end))
    end_time = time.time()
    uptime = end_time - start_time
    print "******************"        
    print "Read time:", str(datetime.timedelta(seconds=int(uptime)))
    print "******************"        

    # Manage the missing angles:
    theta  = tomopy.angles(prj.shape[0], ang1=0.0, ang2=180.0)
    
    # normalize the prj
    prj = tomopy.normalize(prj, flat, dark)
    calc_center = best_center
    #calc_center = tomopy.find_center(prj, theta, emission=False, init=best_center, ind=0, tol=0.3)
    print "Center [%d]" % calc_center

    # reconstruct 
    print "Test reconstruction of slice [%d]" % sino_start
    rec = tomopy.recon(prj, theta, center=calc_center, algorithm='gridrec', emission=False)
        
    # Write data as stack of TIFs.
    tomopy.io.writer.write_tiff_stack(rec, fname=output_name)

    print "Slice saved as [%s_00000.tiff]" % output_name

def rec_h5(file_name, sino_start, sino_end, best_center, output_name):

    print '\n#### Processing '+ file_name

    start_time = time.time()
    # Read HDF5 file.
    prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(sino_start, sino_end))
    end_time = time.time()
    uptime = end_time - start_time
    print "******************"        
    print "Read time:", str(datetime.timedelta(seconds=int(uptime)))
    print "******************"        

    # Manage the missing angles:
    theta  = tomopy.angles(prj.shape[0], ang1=0.0, ang2=180.0)
    
    # normalize the prj
    prj = tomopy.normalize(prj, flat, dark)
    calc_center = best_center
    #calc_center = tomopy.find_center(prj, theta, emission=False, init=best_center, ind=0, tol=0.3)
    print "Center [%d]" % calc_center

    # reconstruct 
    print "Test reconstruction of slice [%d]" % sino_start
    rec = tomopy.recon(prj, theta, center=calc_center, algorithm='gridrec', emission=False)
        
    # Write data as stack of TIFs.
    tomopy.io.writer.write_tiff_stack(rec, fname=output_name)

    print "Slice saved as [%s_00000.tiff]" % output_name

    
def main():
    ##################################### Inputs ##########################################################   

    file_name = '/local/dataraid/databank/templates/aps_1-ID/data_'
    output_name = '/local/dataraid/databank/templates/dataExchange/tmp/rec/CAT4B_2_tiff'
    best_center = 1026; sino_start = 1000; sino_end = 1004; 

    read_log(file_name)
    rec_tiff(file_name, sino_start, sino_end, best_center, output_name)    

    file_name = '/local/dataraid/databank/dataExchange/tmp/APS_1_ID.h5'
    output_name = '/local/dataraid/databank/templates/dataExchange/tmp/rec/CAT4B_2_h5'
    rec_h5(file_name, sino_start, sino_end, best_center, output_name)

if __name__ == "__main__":
    main()


