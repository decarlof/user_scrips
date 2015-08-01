"""
TomoPy example script to reconstruct the ESRF ID-19 tomography data as original edf
"""

import tomopy

# Set path to the micro-CT data to reconstruct.
fname = 'data_dir/'
fname = '/local/dataraid/databank/templates/esrf_ID19/'

# Select the sinogram range to reconstruct.
start = 300
end = 304

# Read the ESRF ID-19 raw data.
proj, flat, dark = tomopy.io.exchange.read_esrf_id19(fname, sino=(start, end))

# Set data collection angles as equally spaced between 0-180 degrees.
theta  = tomopy.angles(proj.shape[0], 0, 180)
print proj.shape
print flat.shape
print dark.shape

# Flat-field correction of raw data.
proj = tomopy.normalize(proj, flat, dark)

# Set rotation axis location manually.
best_center = 549.84; 
rot_center = best_center

# Find rotation center.
#rot_center = tomopy.find_center(proj, theta, emission=False, init=best_center, ind=0, tol=0.3)
print "Center of rotation:", rot_center

# Reconstruct object using Gridrec algorithm.
rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec', emission=False)
    
# Mask each reconstructed slice with a circle.
rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

# Write data as stack of TIFs.
tomopy.io.writer.write_tiff_stack(rec, fname='recon_dir/recon')
