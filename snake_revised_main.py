import connect_func_rev
import numpy as np
from constances_rev import num_osc, delta_t, initial_phi_n, cpg_v, cpg_w, phase_bias, cpg_amp
import pose_func_rev
from math import atan2, cos, sin
import vrep
import matplotlib.pyplot as plt
import cpg_func_rev

''''
SET UP INITIAL CONDITION & STORING ARRAY
'''
mat_last_vc = np.identity(2)  # initial pose of virtual chassis
joints_angle_arr = np.zeros(num_osc)
time = 0  # starting time
phi_n = initial_phi_n

time_arr = []
robot_heading_arr = []

''''
SET UP V-REP ENVIRONMENT
'''
clientID, joints_handle, head_frame_handle, vc_handle = connect_func_rev.establish_connection()
connect_func_rev.synchronize_with_vrep(clientID, head_frame_handle)

''''
ENTERING ETERNITY LOOP
'''
flag_vrep_going = True
print('Enter while loop')

while flag_vrep_going is True:

    mat_links_com = pose_func_rev.links_com_respect_head(joints_angle_arr)  # calculate coordinate of all links COM
    robot_com, mat_vc = pose_func_rev.find_virtual_chassis(mat_links_com, mat_last_vc)  # find robot COM and
    # virtual chassis with respect to head frame

    # Streaming head frame pose relative to global frame
    mat_global_head = connect_func_rev.stream_head_frame_pose(clientID, head_frame_handle)

    # Calculate pose of VC relative to global
    mat_head_vc = np.array([[mat_vc[0, 0], mat_vc[0, 1], robot_com[0]],
                            [mat_vc[1, 0], mat_vc[1, 1], robot_com[1]],
                            [0, 0, 1]])
    mat_global_vc = np.dot(mat_global_head, mat_head_vc)

    # extract robot heading and position
    robot_heading = atan2(mat_global_vc[1, 0], mat_global_vc[0, 0])
    global_robot_com = mat_global_vc[: -1, -1]

    # Buffer gamma_head
    # rc_hf_2, ori_hf_2 = vrep.simxGetObjectOrientation(clientID, initial_frame_handle, -1, vrep.simx_opmode_buffer)

    '''
    DIRECTION CONTROL
    '''
    # Compute delta_amp - P controller
    # err = (VC_gamma - desired_ang)
    # delta_amp = CPG_const.dir_Kp * err
    # if delta_amp > 3.0:
    #     delta_amp = 3.0
    # elif delta_amp < - 3.0:
    #     delta_amp = -3.0

    # Compute CPG state variable - phi
    # phi_np1 = cpg_func_rev.rk4_phi(cpg_func_rev.head_navigating_ode, time, phi_n, delta_t, cpg_v, cpg_w, phase_bias)
    phi_np1 = cpg_func_rev.rk4_phi(cpg_func_rev.ode_phi, time, phi_n, delta_t, cpg_v, cpg_w, phase_bias)

    for i, phi_i in enumerate(phi_np1):
        theta_i = cpg_amp * sin(phi_i)
        # send theta_i to v-rep
        vrep.simxSetJointTargetPosition(clientID, joints_handle[i], theta_i, vrep.simx_opmode_oneshot)
        # update value of joints_angle_arr for the next loop
        joints_angle_arr[i] = theta_i

    # STORE JUST COMPUTED VALUE TO PLOT
    # COM_x_arr.append(VC_coord[0])
    # COM_y_arr.append(VC_coord[1])
    robot_heading_arr.append(robot_heading)
    time_arr.append(time)

    # UPDATE INITIAL CONDITION
    phi_n = phi_np1  # initial condition of CPG state variable
    time += delta_t
    mat_last_vc = mat_vc

    # ADVANCE V-REP TO NEXT TIME STEP
    if time > 30:
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
    returnCode = vrep.simxSynchronousTrigger(clientID)
    if returnCode is not vrep.simx_return_ok:  # check for the stop condition of the whole while loop
        print('Trigger simulation time step failed')
        flag_vrep_going = False
    else:
        # wait till the end of already advanced time step to finish before computing new set point of joints
        rc_pingTime, pingTime = vrep.simxGetPingTime(clientID)


''''
PLOT SIMULATION RESULTS
'''
plt.plot(time_arr, robot_heading_arr, 'b-', label='heading')
plt.xlabel('time(s)')
plt.ylabel('rad')
plt.legend()
plt.grid()

plt.show()
