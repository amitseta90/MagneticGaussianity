#-------- options for plotting ----------------------------

plot_path = "./Plot/"
plot_name = "test_all"
save_pdfs = True # If pdfs and bins of the matplotlib.hist command shall be saved to disk, for further comparisons
do_pi = True # If the polarized intensity shall be plotted instead of U

# -------- what to calculate ------------

do_rm = True # if the rotation measure should be calculated
do_i = True  # if Stokes I should be calculated
do_qu = True  # if Stokes Q and U should be calculated
faraday_rotate = False # if Qs and Us should be Faraday rotated along the way, computationally expensive compared to simple integration!
direction = None  # direction the cubes are integrated and stacked along (possible are None, 0, 1, 2). If None, the cubes are also stacked over all directions
rotate_cubes = False

shape = (512, 512) # shape parameter, unused if any simulated data is used

#--------- some physics -----------------
spectral_index = 3. # spectral index of synchrotron radioation, used for the relative normalization of Q and U and the magnetic field dependence of synchtrotron radiation
lambda_square = 1./512  # squared observing frequency, necessary for faraday rotation of Qs and Us (if B=1, nth=1 over the full loS, 1/len(LoS) equals 1 rad)

#--------- options for the simulation files -------------------

data_path = "./Data/" # path where the magnetic field and thermal electron simulation boxes are stored, the fields are automatically loaded 
single_file = None # "sm10_1210.h5" # None #  name of the file that should be used, if None all files will be used, depending on choices below 
low_mach = False # if the low or high mach cubes should be loaded

#--------- options for the magnetic fields -------------------
mag_type = "simulation" #possible are "simulation" or "constant"

# simulated params
gaussian = False # if the gaussian or non gaussian fields are used
# constant params
bx = 1.   
by = 1.   
bz = 1.    

#--------- options for the thermal electrons ---------------------

th_type = "simulation" #possible are "random", "simulation" or "constant"
 
# constant params
th_n0 = 1.    

# random params
th_random_params = {
    "offset_mean": 3,
    "offset_std": (1.e-16, 1.e-16), 
    "fluctuations": (4., 1.e-16), 
    "loglogavgslope": (3, 1.e-16),
    "asperity": None,
    "flexibility": None   
}


#--------- options for the comsic ray electrons ---------------------
cr_type = "constant" #possible are "random" or "constant"

# constant params
cr_n0 = 1.    

# random params
cr_random_params = {
    "offset_mean": 0,
    "offset_std": (1.e-16, 1.e-16), 
    "fluctuations": (1., 1.e-16), 
    "loglogavgslope": (5, 1.e-16),
    "asperity": None,
    "flexibility": None   
}



