"""
Haversine and equirectangular equations as functions, as written for
Assignment 1.
"""

import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """Python does have a built-in haversine function, but where's the fun in
    using that?"""
    # Convert latitudes and longitudes to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    latd = lat2 - lat1      # Latitude delta
    lond = lon2 - lon1      # Longitude delta

    # Haversine formula
    a = np.sin(latd/2)**2 + np.cos(lat1) * np.cos(lat2) \
        * np.sin(lond/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    # Volumetric mean radius of the Earth (m) * c = distance between points (m)
    d = 6371e3 * c
    return d

def equirectangular(lat1, lon1, lat2, lon2):
    """Implementation of the equirectangular approximation, returning a
    distance in metres."""
    # Convert latitudes and longitudes to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    latd = lat2 - lat1      # Latitude delta
    lond = lon2 - lon1      # Longitude delta

    # Equirectangular approximation returning metres
    x = lond * 0.839
    d = np.sqrt(x**2 + latd**2)
    return 6371e3 * d
