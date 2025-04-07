"""
flight_control_util.py

Provides flight control utilities for combat flight simulation.

Author: Sean Zhou
Created: 2025-03-24
"""

import numpy as np

def roll_correction_cmd(desired_roll: float, current_roll: float, k_roll=0.05) -> float:
    """Stabilize roll degree at desired level by countering deviation with proportional command.
    Does not acount for wrap arounds (e.g. flip from 0 to 180)!

    Parameters:
        desired_roll (float): desired roll in degrees
        current_roll (float): current roll in degrees 
        k_roll (float): strengh of the proportional counter command 

    Returns:
        float: correction roll command between -1.0 (full left stick) and 1.0 (full right stick)
    """

    roll_error = desired_roll - current_roll
    roll_cmd = np.clip(roll_error * k_roll, -1.0, 1.0)
    return roll_cmd

def roll_correction_cmd_limit_left(current_roll: float, k_roll=0.001) -> float | None:
    """Prevent left rolls (negative roll) with a correction command. Correct based on quadrant:
    - slight left roll -> roll back right to 0 degrees
    - deep inverted left roll -> continue left roll toward +180 degrees (upright inverted)

    Parameters:
        current_roll (float): current roll angle [-180, 180] deg
        k_roll (float): strengh of the roll correction command

    Returns:
        float: Correction command [-1, 1] or None if no correction needed
    """
    if -90 < current_roll < 0:
        roll_error = -current_roll
        roll_cmd = np.clip(roll_error * k_roll, 0.0, 1.0)
        return roll_cmd

    elif -180 < current_roll <= -90:
        roll_error = -180 - current_roll
        roll_cmd = np.clip(roll_error * k_roll, -1.0, 0.0)
        return roll_cmd

    else:
        return None

def roll_correction_cmd_limit(roll: float, low: float, high: float, k_roll=0.001) -> float | None:
    """Clamps roll between two positive values (e.g. between 45 and 135 degrees) with a correction commands
    if necessarey

    Parameters:
        roll (float): current roll degrees 
        low (float): lower bound of the roll
        high (float): higher bound of the roll 

    Returns:
        float: Correction command [-1, 1] or None if no correction needed
    """
    if roll < low:
        roll_error = low - roll
        roll_cmd = np.clip(roll_error * k_roll, 0.0, 1.0)  # positive roll command (right stick)
        return roll_cmd
    elif roll > high:
        roll_error = high - roll
        roll_cmd = np.clip(roll_error * k_roll, -1.0, 0.0) # negative roll command (left stick)
        return roll_cmd
    else:
        return None