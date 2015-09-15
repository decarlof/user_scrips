"""
TomoPy example script to reconstruct the Anka topo-tomo tomography data as original tiff
"""

import tomopy

# Set path to the micro-CT data to reconstruct.
fname = 'data_dir/'
fname = '/local/dataraid/databank/templates/anka_topo-tomo/'

proj_start = 0
proj_end = 3167
flat_start = 0
flat_end = 100
dark_start = 0
dark_end = 100

ind_tomo = range(proj_start, proj_end)
ind_flat = range(flat_start, flat_end)
ind_dark = range(dark_start, dark_end)

# Select the sinogram range to reconstruct.
start = 800
end = 804

# Read the APS 1-ID raw data.
proj, flat, dark = tomopy.io.exchange.read_anka_topotomo(fname, ind_tomo, ind_flat, ind_dark, sino=(start, end))

# Set data collection angles as equally spaced between 0-180 degrees.
theta  = tomopy.angles(proj.shape[0], 0, 180)
print proj.shape
print flat.shape
print dark.shape

# Flat-field correction of raw data.
proj = tomopy.normalize(proj, flat, dark)

# Set rotation axis location manually.
best_center = 993.825; 
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
