do_rm = True # if the rotation measure should be calculated
do_syncI = True
do_syncQU = True
faraday_rotate = True # if Qs and Us should be Faraday rotated along the way, computationally expensive!
direction = 0  # direction the cubes are integrated along (possible are 0, 1, 2)

# some physics
spectral_index = 3. # spectral index of synchrotron radioation, used 
lambda_square = .1  # 


#--------- options for the magnetic fields -------------------
data_path = "./Data/" # path where the magnetic field simulation boxes are stored
gaussian = False # if the gaussian 
low_mach = False #

#--------- options for the thermal electrons ---------------------
th_random = True   
th_n0 = 1.    # use this constant value if random=False

th_random_params = {
    "offset_mean": 0,
    "offset_std": (0, 0.00001), 
    "fulctuations": (1., 1.e-16), 
    "loglogavgslope": (3, 1.e-16),
    "asperity": None,
    "flexibility": None   
}


#--------- options for the comsic ray electrons ---------------------
cr_random = False   
cr_n0 = 1.    # use this constant value if random=False

cr_random_params = {
    "offset_mean": 0,
    "offset_std": (0, 0.00001), 
    "fulctuations": (1., 1.e-16), 
    "loglogavgslope": (5, 1.e-16),
    "asperity": None,
    "flexibility": None   
}


