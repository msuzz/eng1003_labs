import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as sig


def expand_arrays(lat, lon, ele, time, tdeltas, tsecs):
    """Expansion function pads the data arrays to the total duration of the
    trip (calculated above) and moves the data to the correct position. e.g,
    we have a timeDelta of 5 seconds for a point, so we assign NaN to the next
    5 elements in the expanded array, jump ahead past those 5 indices, and
    continue iterating through the rest of the input array.
    This is great for our timespan plot, as the length of the data gap is now
    visually represented.
    We will interpolate the NaN values after with numpy.interp()"""
    ti = 0
    # Initialise default values in output arrays to NaN
    tspan = np.full(tsecs, np.nan)
    xlat = np.full(tsecs, np.nan)
    xlon = np.full(tsecs, np.nan)
    xele = np.full(tsecs, np.nan)
    for i in range(0, time):
        if tdeltas[i] == 1 or tdeltas[i] == 0:
            tspan[ti] = tdeltas[i]
            xlat[ti] = lat[i]
            xlon[ti] = lon[i]
            xele[ti] = ele[i]
            ti += 1
        else:
            ti += int(round(tdeltas[i]))  # Data missing, update time index
    return xlat, xlon, xele, tspan


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


def time_diff(time1, time2):
    """Returns a the difference between two given time value strings as
    a floating point number"""
    time1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S+00:00')
    time2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S+00:00')
    tdiff = time2 - time1            # Difference in time
    return tdiff.seconds             # Convert from datetime object


def nan_indices(a):
    """Returns an array of indices of NaNs and a lambda function which
    we use with the bitwise operator to interpolate only NaN elements of
    our data arrays."""
    return np.isnan(a), lambda b: b.nonzero()[0]


def lower_bound_estimate(h):
    """Calculate change in gravitational potential energy"""
    return 100 * 9.8 * h


def filter_data(d):
    """Applies a Butterworth filter to the input data array"""
    [b, a] = sig.butter(2, 0.01)
    return sig.lfilter(b, a, d)


csvData = pd.read_csv('ass1-track.csv')     # Load in our CSV data

# Set up our data arrays
latDeg = np.array(csvData['lat'].values)    # Latitude in degrees
lonDeg = np.array(csvData['lon'].values)    # Longitude in degrees
ele = np.array(csvData['ele'].values)       # Elevation
time = csvData['time'].values     # Store the time column as a string array
# Array of changes in time per point
timeDeltas = np.ones(len(time))   # np.ones avoids divide by zero
pointDists = np.zeros(len(time))  # Array of distances between points

# Loop populates the timeDeltas and pointDists arrays
for i in range(1, len(time)):   # Skip index 0
    timeDeltas[i] = time_diff(time[i-1], time[i])
    '''Note that we are calculating the distance based on the *current and
    previous* data points. I am aware that the assignment notes say to use
    the *current and next* data points, but this is inconsistent with the
    timeDeltas array and makes it arbitrarily difficult to calculate the
    average speed of the entire dataset.'''
    pointDists[i] = haversine(latDeg[i-1], lonDeg[i-1], latDeg[i], lonDeg[i])
    # pointDists[i] = equirectangular(latDeg[i-1], lonDeg[i-1],
    #                                 latDeg[i], lonDeg[i])
    # ^ Both equations are implemented btw ;)

avgSpeeds = pointDists/timeDeltas   # Populate average speeds in single loc

totalSecs = 0    # Int total number of seconds, including those without data
for i in range(len(time)):
    totalSecs += timeDeltas[i].astype(int)

# See expand_arrays() docstring about this
xlat, xlon, xele, timeSpan = expand_arrays(latDeg, lonDeg, ele, len(time),
                                           timeDeltas, totalSecs)

# This for loop interpolates the data for the NaNs in our 'expanded' arrays
for a in [xlat, xlon, xele]:
    ni, b = nan_indices(a)  # Returns array of NaN indices and lambda function
    a[ni] = np.interp(b(ni), b(~ni), a[~ni])

# Interpolated average speed *is* the distance between our interpolated points
xavgSpeeds = np.zeros(totalSecs)
xeleChanges = np.zeros(totalSecs)   # Interpolated changes in elevation
for i in (range(totalSecs)):
    xavgSpeeds[i] = haversine(xlat[i-1], xlon[i-1], xlat[i], xlon[i])
    xeleChanges[i] = xele[i] - xele[i-1]

riderPower = lower_bound_estimate(xeleChanges)  # Rider power per point

# Loop gets our total power exerted by rider for both arrays
riderPowTotal = 0
for i in (range(totalSecs)):
    if xeleChanges[i] < 0:
        riderPower[i] = 0
    else:
        riderPowTotal += riderPower[i]

riderPowerf = filter_data(riderPower)   # Filtered rider power per point

# Loop gets our filtered total power exerted
riderPowTotalf = 0
for i in (range(totalSecs)):
    if xeleChanges[i] < 0:
        riderPowerf[i] = 0
    else:
        riderPowTotalf += riderPowerf[i]

riderPowAvg = riderPowTotal/totalSecs       # Average rider power
riderPowAvgf = riderPowTotalf/totalSecs     # Filtered

print(f'Average raw rider power output: {riderPowAvg}')
print(f'Average filtered rider power output: {riderPowAvgf}')


''''Everything below here is plotting code'''


# Define figure and axis objects and set some display properties for plot
fig, axs = plt.subplots(3, 3, constrained_layout=True)
fig.set_figwidth(14.4)
fig.set_figheight(9.6)

# Longitude (x) and latitude (y) subplot
axs[0, 0].plot(lonDeg, latDeg, 'b.',            # Blue .
               lonDeg[0], latDeg[0], 'go',      # Green O on start
               lonDeg[-1], latDeg[-1], 'r+')    # Red + on finish
axs[0, 0].set_title('Longitude vs latitude')
axs[0, 0].set_xlabel('Longitude (°)')
axs[0, 0].set_ylabel('Latitude (°)')

# Long vs lat interpolated subplot
axs[0, 1].plot(xlon, xlat, 'rx',        # Red x
               lonDeg, latDeg, 'b.')    # Blue point
axs[0, 1].set_title("Longitude vs latitude (linear interpolation)")
axs[0, 1].set_xlabel('Longitude (°)')
axs[0, 1].set_ylabel('Latitude (°)')
axs[0, 1].set_xbound(0.001+1.5157e2, 0.011+1.5157e2)    # Zoom in on the
axs[0, 1].set_ybound(-32.8825, -32.878)                 # tunnel area

# Interpolated elevation subplot
axs[0, 2].plot(xele, 'm+')              # Purple!
axs[0, 2].set_title("Elevation vs time (linear interpolation)")
axs[0, 2].set_xlabel('Time (s)')
axs[0, 2].set_ylabel("Elevation (m above sea level")
axs[0, 2].set_xbound(5300, 5500)        # Zoom right in on our missing data

# Time deltas array subplot
axs[1, 0].plot(timeDeltas, 'gx')        # Green x
axs[1, 0].set_title('Change in time per point')
axs[1, 0].set_xlabel('Data point')
axs[1, 0].set_ylabel('Seconds since last data point')

# Zoomed timespan array subplot - this shows our data gap very well!
axs[1, 1].plot(timeSpan, 'gx')          # Green x
axs[1, 1].set_title('Timespan (zoomed to show gaps)')
axs[1, 1].set_xlabel('Time (s)')
axs[1, 1].set_ylabel('Data present?')
axs[1, 1].set_xbound(5300, 5500)        # Zoom right in on our missing data
axs[1, 1].set_ybound(0.75, 1.25)

# Raw power output subplot
axs[1, 2].plot(riderPower)
axs[1, 2].set_title("Rider power output (raw)")
axs[1, 2].set_xlabel('Time (s)')
axs[1, 2].set_ylabel('Power (W)')

# Average speed subplot
axs[2, 0].plot(avgSpeeds, 'r')      # Red
axs[2, 0].set_title("Speed vs time")
axs[2, 0].set_xlabel("Time (s)")
axs[2, 0].set_ylabel("Average speed (m/s)")

# Speed vs time interpolated subplot
axs[2, 1].plot(xavgSpeeds, 'r+')    # Red +
axs[2, 1].set_title("Speed vs time (linear interpolation)")
axs[2, 1].set_xlabel("Time (s)")
axs[2, 1].set_ylabel("Average speed (m/s)")
axs[2, 1].set_xbound(5300, 5500)        # Zoom right in on our missing data

# Filtered power output subplot
axs[2, 2].plot(riderPowerf)
axs[2, 2].set_title("Rider power output (filtered)")
axs[2, 2].set_xlabel('Time (s)')
axs[2, 2].set_ylabel('Power (W)')

plt.show()  # Display plots
