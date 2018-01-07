from constances_rev import num_osc
from math import sin, pi, cos
import numpy as np


def rk4_phi(f, t_n, phi_n, t_samp, v, w, phase_bias):
    # Runge-Kutta 4-th
    k1 = t_samp * f(t_n, phi_n, v, w, phase_bias)
    k2 = t_samp * f(t_n + 0.5 * t_samp, phi_n + 0.5 * k1, v, w, phase_bias)
    k3 = t_samp * f(t_n + 0.5 * t_samp, phi_n + 0.5 * k2, v, w, phase_bias)
    k4 = t_samp * f(t_n + t_samp, phi_n + k3, v, w, phase_bias)
    phi_np1 = phi_n + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return phi_np1


def ode_phi(t_n, phi_n, v, w, phase_bias):
    # Bidirectional coupling CPG
    dphi = np.zeros(num_osc)
    for i in range(num_osc):
        if i is 0:
            dphi_i = 2 * pi * v + w * sin(phi_n[i + 1] - phi_n[i] + phase_bias)
        elif i < (num_osc - 1):
            dphi_i = 2 * pi * v + w * sin(phi_n[i - 1] - phi_n[i] - phase_bias) + w * sin(phi_n[i + 1] - phi_n[i]
                                                                                          + phase_bias)
        else:
            dphi_i = 2 * pi * v + w * sin(phi_n[i - 1] - phi_n[i] - phase_bias)
        dphi[i] += dphi_i
    return dphi


def ode_phi_mod(t_n, phi_n, v, w, phase_bias):
    # Bidirectional coupling CPG
    dphi = np.zeros(num_osc)
    for i in range(num_osc):
        if i is 0:
            dphi_i = 2 * pi * v + w * cos(phi_n[i + 1] - phi_n[i] + phase_bias)
        elif i < (num_osc - 1):
            dphi_i = 2 * pi * v + w * cos(phi_n[i - 1] - phi_n[i] - phase_bias) + w * cos(phi_n[i + 1] - phi_n[i]
                                                                                          + phase_bias)
        else:
            dphi_i = 2 * pi * v + w * cos(phi_n[i - 1] - phi_n[i] - phase_bias)
        dphi[i] += dphi_i
    return dphi


def head_navigating_ode(t_n, phi_n, v, w, phase_bias):
    dphi = np.array([])
    for i in range(num_osc):
        if i is 0:
            dphi_i = 2 * pi * v + w * sin(phi_n[2] - phi_n[i] + pi)
        elif i is 1:
            dphi_i = 2 * pi * v + w * sin(phi_n[2] - phi_n[i] + phase_bias)
        elif i is 2:
            dphi_i = 2 * pi * v + w * sin(phi_n[i - 1] - phi_n[i] - phase_bias) \
                     + w * sin(phi_n[i + 1] - phi_n[i] + phase_bias) + w * sin(phi_n[0] - phi_n[i] - pi)

        elif i < (num_osc - 1):
            dphi_i = 2 * pi * v + w * sin(phi_n[i - 1] - phi_n[i] - phase_bias) + w * sin(phi_n[i + 1] - phi_n[i]
                                                                                          + phase_bias)
        else:
            dphi_i = 2 * pi * v + w * sin(phi_n[i - 1] - phi_n[i] - phase_bias)
        dphi = np.append(dphi, np.array([dphi_i]))
    return


def head_navigating_ode_mod(t_n, phi_n, v, w, phase_bias):
    dphi = np.array([])
    for i in range(num_osc):
        if i is 0:
            dphi_i = 2 * pi * v + w * cos(phi_n[2] - phi_n[i] + pi)
        elif i is 1:
            dphi_i = 2 * pi * v + w * cos(phi_n[2] - phi_n[i] + phase_bias)
        elif i is 2:
            dphi_i = 2 * pi * v + w * cos(phi_n[i - 1] - phi_n[i] - phase_bias) \
                     + w * cos(phi_n[i + 1] - phi_n[i] + phase_bias) + w * cos(phi_n[0] - phi_n[i] - pi)

        elif i < (num_osc - 1):
            dphi_i = 2 * pi * v + w * cos(phi_n[i - 1] - phi_n[i] - phase_bias) + w * cos(phi_n[i + 1] - phi_n[i]
                                                                                          + phase_bias)
        else:
            dphi_i = 2 * pi * v + w * cos(phi_n[i - 1] - phi_n[i] - phase_bias)
        dphi = np.append(dphi, np.array([dphi_i]))
    return dphi


