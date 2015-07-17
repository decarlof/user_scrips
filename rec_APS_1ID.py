# -*- coding: utf-8 -*-
import tomopy

def rec_test(file_name, sino_start, sino_end, best_center, output_name):

    print '\n#### Processing '+ file_name
    print "Test reconstruction of slice [%d]" % sino_start

    # Read HDF5 file.
    prj, flat, dark = tomopy.io.exchange.read_aps_32id(file_name, sino=(sino_start, sino_end))

    # Manage the missing angles:
    theta  = tomopy.angles(prj.shape[0], ang1=0.0, ang2=360.0)
    
    # normalize the prj
    prj = tomopy.normalize(prj, flat, dark)
    calc_center = tomopy.find_center(prj, theta, emission=False, init=best_center, ind=0, tol=0.3)
    print best_center, calc_center

    # reconstruct 
    rec = tomopy.recon(prj, theta, center=calc_center, algorithm='gridrec', emission=False)
        
    # Write data as stack of TIFs.
    tomopy.io.writer.write_tiff_stack(rec, fname=output_name)

    print "Slice saved as [%s_00000.tiff]" % output_name
    
def main():
    ##################################### Inputs ##########################################################   
    file_name = '/local/dataraid/databank/templates/dataExchange/tmp/APS_1ID_bov_ver6_0N.h5' 
    output_name = '/local/dataraid/databank/templates/dataExchange/tmp/rec/rec_bov_ver6_0N'
    best_center = 976.6; sino_start = 1200; sino_end = 1202; 

#    file_name = '/local/dataraid/databank/templates/dataExchange/tmp/APS_1ID_bov_ver6_20N.h5' 
#    output_name = '/local/dataraid/databank/templates/dataExchange/tmp/rec/rec_bov_ver6_20N'
#    best_center = 995.4; sino_start = 1200; sino_end = 1202; 

#    file_name = '/local/dataraid/databank/templates/dataExchange/tmp/APS_1ID_bov_ver6_fail.h5' 
#    output_name = '/local/dataraid/databank/templates/dataExchange/tmp/rec/rec_bov_ver6_fail'
#    best_center = 998.4; sino_start = 1200; sino_end = 1202; 

    rec_test(file_name, sino_start, sino_end, best_center, output_name)

if __name__ == "__main__":
    main()


