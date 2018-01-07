import vrep
from constances_rev import joints_name, head_frame, virtual_chassis
import sys
import numpy as np
from math import sin, cos


def establish_connection():
    # Function purpose:
    # * Establish connection between python and v-rep >>> get client ID
    # * Get joints' handle
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 2000, 5)
    joints_handle = []
    for joint in joints_name:
        rc_joint_handle, joint_handle = vrep.simxGetObjectHandle(clientID, joint, vrep.simx_opmode_blocking)
        if rc_joint_handle is vrep.simx_return_ok:
            joints_handle.append(joint_handle)
        else:
            sys.exit("Get joint handle encounters error")
    # Get head frame handle
    rc_head_frame, head_frame_handle = vrep.simxGetObjectHandle(clientID, head_frame, vrep.simx_opmode_blocking)
    if rc_head_frame is not vrep.simx_return_ok:
        sys.exit("Get head frame encounters error")
    # Get virtual chassis handle
    rc_vc, vc_handle = vrep.simxGetObjectHandle(clientID, virtual_chassis, vrep.simx_opmode_blocking)
    if rc_vc is not vrep.simx_return_ok:
        sys.exit("Get virtual chassis encounters error")

    return clientID, joints_handle, head_frame_handle, vc_handle


def synchronize_with_vrep(clientID, head_frame_handle):
    # Function purpose:
    # * make python synchronize with v-rep

    vrep.simxSynchronous(clientID, True)  # Enable synchronous mode
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
    vrep.simxSynchronousTrigger(clientID)  # Trigger next simulation step

    # Streaming pose of head frame for the first time
    vrep.simxGetObjectPosition(clientID, head_frame_handle, -1, vrep.simx_opmode_streaming)
    vrep.simxGetObjectOrientation(clientID, head_frame_handle, -1, vrep.simx_opmode_streaming)

    vrep.simxGetPingTime(clientID)  # finish the first simulation time step
    return


def stream_head_frame_pose(clientID, head_frame_handle):
    rc_head_posi, head_posi = vrep.simxGetObjectPosition(clientID, head_frame_handle, -1, vrep.simx_opmode_buffer)
    rc_head_ori, head_ori = vrep.simxGetObjectOrientation(clientID, head_frame_handle, -1, vrep.simx_opmode_buffer)
    head_frame_pose = np.array([[cos(head_ori[-1]), -sin(head_ori[-1]), head_posi[0]],
                                [sin(head_ori[-1]), cos(head_ori[-1]), head_posi[1]],
                                [0, 0, 1]])
    return head_frame_pose
