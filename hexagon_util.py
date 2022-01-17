from math import pi

import numpy as np

from hexagon import IntersectingHexagonAngles, NonIntersectingHexagonAngles
from hyperbolic_hexagon import HexagonAngles


def create_phis(min_dist=0.4, max_dist=-1) -> IntersectingHexagonAngles:
    variable_phis = np.sort(np.random.uniform(0, 2 * pi, 5))
    while np.min(np.abs(np.roll(variable_phis, shift=1) - variable_phis)) < min_dist \
            or np.max(np.abs(np.roll(variable_phis, shift=1) - variable_phis)) < max_dist \
            or variable_phis[0] < variable_phis[4] - 2 * pi + min_dist:
        variable_phis = np.sort(np.random.uniform(0, 2 * pi, 5))

    phis = HexagonAngles(variable_phis)
    return phis


def create_phis_non_intersecting(min_dist=0.4) -> NonIntersectingHexagonAngles:
    phis = np.sort(np.random.uniform(0, 2 * pi, 6))
    while np.min(np.abs(np.roll(phis, shift=1) - phis)) < min_dist \
            or phis[0] < phis[5] - 2 * pi + min_dist:
        phis = np.sort(np.random.uniform(0, 2 * pi, 6))
    phis = HexagonAngles(phis)
    return phis


def create_phi_transition(phi_old: IntersectingHexagonAngles, phi_new: IntersectingHexagonAngles, step_size=10):
    assert phi_old.shape == phi_new.shape
    transition = np.empty(shape=(step_size, phi_old.shape[0]))

    for t in range(step_size):
        step_variable_part = phi_old.variable_angles() * (1 - t / step_size) + phi_new.variable_angles() * t / step_size
        step = HexagonAngles(step_variable_part)
        transition[t] = step
    return transition


def create_radius_transition(radius, step_size=10, end_point=1):
    transition = np.empty(shape=(step_size, radius.shape[0]))

    for t in range(step_size):
        step_variable_part = radius * (1 - t / step_size) + end_point * t / step_size
        transition[t] = step_variable_part
    return transition
