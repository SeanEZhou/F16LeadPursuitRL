"""
flight_metrics_util.py

Provides utilities for computing flight metrics like angular difference or distance.

Author: Sean Zhou
Created: 2025-03-24
"""

def haversine(lat1, lon1, lat2, lon2):
    """Compute approximate distance (in meters) between two lat-long points."""
    R = 6371000  # Earth radius in meters
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    
    a = np.sin(dphi/2.0)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    return R * c  # Distance in meters

def angular_difference(new_angle, old_angle):
    """Compute the smallest difference between two angles, handling wraparound at ±180°."""
    return ((new_angle - old_angle + 180) % 360) - 180