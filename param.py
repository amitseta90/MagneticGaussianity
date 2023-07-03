

do_rm = True # if the rotation measure should be calculated
do_i = True  # if Stokes I should be calculated
do_qu = True  # if Stokes Q and U should be calculated
faraday_rotate = True # if Qs and Us should be Faraday rotated along the way, computationally expensive compared to simple integration!
direction = 0  # direction the cubes are integrated along (possible are 0, 1, 2)

# some physics
spectral_index = 3. # spectral index of synchrotron radioation, used for the relative normalization of Q and U
lambda_square = .1  # squared observing 


#--------- options for the magnetic fields -------------------
data_path = "./Data/" # path where the magnetic field simulation boxes are stored
gaussian = False # if the gaussian 
low_mach = False #

#--------- options for the thermal electrons ---------------------
th_random = True   
th_n0 = 1.    # use this constant value if random=False

th_random_params = {
    "offset_mean": 3,
    "offset_std": (1.e-16, 1.e-16), 
    "fluctuations": (4., 1.e-16), 
    "loglogavgslope": (3, 1.e-16),
    "asperity": None,
    "flexibility": None   
}


#--------- options for the comsic ray electrons ---------------------
cr_random = False   
cr_n0 = 1.    # use this constant value if random=False

cr_random_params = {
    "offset_mean": 0,
    "offset_std": (1.e-16, 1.e-16), 
    "fluctuations": (1., 1.e-16), 
    "loglogavgslope": (5, 1.e-16),
    "asperity": None,
    "flexibility": None   
}


