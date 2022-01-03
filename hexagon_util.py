from hyperbolic_hexagon import HexagonAngles
import numpy as np
from math import pi


def create_phis(min_dist=0.4) -> HexagonAngles:
    variable_phis = np.sort(np.random.uniform(0, 2 * pi, 5))
    while np.min(np.abs(np.roll(variable_phis, shift=1) - variable_phis)) < min_dist \
            or variable_phis[0] < variable_phis[4] - 2 * pi + min_dist:
        variable_phis = np.sort(np.random.uniform(0, 2 * pi, 5))

    phis = HexagonAngles(variable_phis)
    return phis


def create_phi_transition(phi_old: HexagonAngles, phi_new: HexagonAngles, step_size=10):
    assert phi_old.shape == phi_new.shape
    transition = np.empty(shape=(step_size, phi_old.shape[0]))

    for t in range(step_size):
        step_variable_part = phi_old.variable_angles() * (1 - t / step_size) + phi_new.variable_angles() * t / step_size
        step = HexagonAngles(step_variable_part)
        transition[t] = step
    return transition


def create_radius_transition(radius, step_size=10):
    transition = np.empty(shape=(step_size, radius.shape[0]))

    for t in range(step_size):
        step_variable_part = radius * (1 - t / step_size) + 1 * t / step_size
        transition[t] = step_variable_part
    return transition
