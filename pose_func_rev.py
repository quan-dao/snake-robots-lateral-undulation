import numpy as np
import numpy.linalg as LA
from constances_rev import link_length, num_osc
from math import cos, sin


def planar_homo_trans(theta, a=link_length):
    # Function purpose:
    # *create homogeneous transformation matrix represent 2D pose of link i relative to link (i - 1)
    # Input:
    # * angular position of revolute joint
    # Predefined parameters:
    # * link length
    homo_trans = np.array([[cos(theta), -sin(theta), -a * cos(theta)],
                           [sin(theta), cos(theta), -a * sin(theta)],
                           [0, 0, 1]])
    return homo_trans


def links_com_respect_head(joints_angle_arr):
    # Function purpose:
    # *compute coordinate of links COM with respect to head frame
    # Input:
    # *joints angle array
    # Method:
    # *use homogeneous transformation matrix
    # link i-th COM = middle point of origins of frame i & frame i + 1
    # Remark:
    # joint i (i=1,num_osc) is fixed with respect to link i - 1
    # frame i is attached to link i at its end (coincident with joint i+1)
    # D-H convention provide pose of frame i (i=0,num_ocs) relative to frame 0 (attached to link 0)
    # homogeneous transformation name convetion: mat_up_down >>> up is the reference frame

    mat_head_0 = planar_homo_trans(0, 0.1525)  # 0.1525 = distance from joint 1 to head frame
    mat_0_i = np.identity(3)  # Since i starts at 0, mat_0_i = pose of frame 0 relative to itself

    mat_links_com = np.zeros([num_osc + 1, 2])  # each row is 2D coordinate of links COM relative to head frame
    mat_frames_coor = np.zeros([num_osc + 1, 2])  # each row is 2D coordinate of frames' origin relative to head frame
    mat_frames_coor[0, :] += mat_head_0[:-1, -1]  # coordinate of frame 0 relative to head frame

    for i, theta in enumerate(joints_angle_arr):
        if i < num_osc - 1:
            mat_i_ip1 = planar_homo_trans(theta)  # pose of frame i + 1 relative to i
        else:
            mat_i_ip1 = planar_homo_trans(theta, 0.5 * link_length)  # length of final link = 0.5 of the others
        mat_0_ip1 = np.dot(mat_0_i, mat_i_ip1)  # pose of frame i + 1 relative to 0
        mat_head_ip1 = np.dot(mat_head_0, mat_0_ip1)
        mat_frames_coor[i + 1, :] += mat_head_ip1[:-1, -1]
        mat_links_com[i + 1, :] += 0.5 * (mat_frames_coor[i + 1, :] + mat_frames_coor[i, :])
        # update value of mat_0_i
        mat_0_i = mat_0_ip1

    return mat_links_com


def find_virtual_chassis(mat_links_com, mat_last_vc):
    # Function purpose:
    # *find pose of the Virtual Chassis with respect to head frame
    # Input:
    # *coordinate of all links COM with respect to head frame
    # *last value of virtual chassis to prevent flip sign
    # Method:
    # *find eigenvectors of covariance matrix formed by links COM

    robot_com = np.sum(mat_links_com, axis=0) / mat_links_com.shape[0]  # find COM of the whole robot

    mat_deviation = mat_links_com  # create deviation matrix
    for i in range(mat_deviation.shape[0]):
        mat_deviation[i, :] -= robot_com

    mat_covariance = np.dot(mat_deviation.T, mat_deviation)
    eig_val, eig_vec = LA.eig(mat_covariance)
    if eig_val[1] > eig_val[0]:
        temp_vec = eig_vec[0]
        eig_vec[0] = eig_vec[1]
        eig_vec[1] = temp_vec
    # enforce positive dot between singular vector at the current and the last time step
    if np.dot(eig_vec[:, 0], mat_last_vc[:, 0]) < 0:
        eig_vec[:, 0] *= -1
    if np.dot(eig_vec[:, 1], mat_last_vc[:, 1]) < 0:
        eig_vec[:, 1] *= -1
    mat_vc = eig_vec  # orientation of VC relative to initial body frame

    return robot_com, mat_vc


