import tomopy
import astra
import numpy as np

proj_type='cuda'
reduce_amount=1

def rec_test(file_name, sino_start, sino_end, astra_method, extra_options, num_iter=1):

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
    
    # remove ring artefacts
    prjn = tomopy.remove_stripe_fw(prj)

    # reconstruct 
    rec = tomopy.recon(prj[:,::reduce_amount,::reduce_amount], theta, center=float(best_center)/reduce_amount, algorithm=tomopy.astra, options={'proj_type':proj_type,'method':astra_method,'extra_options':extra_options,'num_iter':num_iter}, emission=False)
        
    # Write data as stack of TIFs.
    tomopy.io.writer.write_tiff_stack(rec, fname=output_name)

    print "Slice saved as [%s_00000.tiff]" % output_name
    
def rec_full(file_name, sino_start, sino_end, astra_method, extra_options, num_iter=1):

    print '\n#### Processing '+ file_name

    chunks = 10 # number of data chunks for the reconstruction

    nSino_per_chunk = (sino_end - sino_start)/chunks
    print "Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk)
    strt = 0
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
        
        # remove ring artefacts
        prj = tomopy.remove_stripe_fw(prj)

        # reconstruct 
        rec = tomopy.recon(prj[:,::reduce_amount,::reduce_amount], theta, center=float(best_center)/reduce_amount, algorithm=tomopy.astra, options={'proj_type':proj_type,'method':astra_method,'extra_options':extra_options,'num_iter':num_iter}, emission=False)
        
        print output_name

        # Write data as stack of TIFs.
        tomopy.io.writer.write_tiff_stack(rec, fname=output_name, start=strt)
        strt += prj[:,::reduce_amount,:].shape[1]

reconstruction_test = False
import astra

astra_method='SIRT-FBP'
if astra_method=='SIRT-FBP':
    import sirtfbp
    astra.plugin.register(sirtfbp.plugin)
    extra_options = {'filter_dir':'./filters'}
    num_iter = 100

##################################### Inputs ##########################################################
file_name = '/local/dataraid/2014_11/haozhe/Ce6Al4_3kbar_.h5' # best_center = 1232
output_name = 'local/dataraid/2014_11/haozhe/rec/Ce6Al4_3kbar/Ce6Al4_3kbar_rec'
best_center = 1232; sino_start = 740; sino_end = 1700; miss_angles = [141,226]
if reconstruction_test: rec_test(file_name, sino_start, sino_end, astra_method, extra_options, num_iter)
else: rec_full(file_name, sino_start, sino_end, astra_method, extra_options, num_iter)


