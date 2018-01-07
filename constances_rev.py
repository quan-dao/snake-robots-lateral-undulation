
import numpy as np
from math import pi

num_osc = 5  # number of vertical joints
cpg_v = 0.5  # frequency parameter
cpg_w = 15  # coupling weight

# Link length
link_length = 170 * 10 ** -3

# Initial value of oscillators' phase
initial_phi_n = np.zeros(num_osc)

# Phase bias parameters
num_S = 1  # number of S-shape
phase_bias = 2 * pi * num_S / num_osc

# Amplitude parameters
cpg_amp = 15 * pi / 180  # amp of CPG output

# Time parameters
delta_t = 50 * 10 ** (-3)

'''
Controller parameter
'''
# Direction controller
dir_Kp = 0.75
delta_amp_max = 2.0


'''
VREP scene object names
'''
# Name of vertical joint
joints_name = []
for i in range(num_osc):
    joints_name.append('Khop_quay_DC_v'.__add__(str(i)))

# Initial body frame (to serve virtual chassis calculation)
head_frame = 'head_frame'

# Virtual Chassis animated graph
virtual_chassis = 'VC_Graph'