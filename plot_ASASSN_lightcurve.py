#!/usr/bin/env python
"""
Example:
python3 plot_ASASSN_lightcurve.py file_path
python3 plot_ASASSN_lightcurve.py variable_stars_database/EDR3_2875434876156537472.csv
"""

import sys
import pandas as pd
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})

def plot_lightcurve(file):
    lc = pd.read_csv(file)
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(18, 10))
    fig.suptitle(file)
    # For each camera
    for camera in lc['camera'].unique():
        cam_mask = (lc['camera'] == camera)
        cam_lc = lc[cam_mask]
        ax1.errorbar(cam_lc['hjd']-2457000, cam_lc['mag'], yerr=cam_lc['mag_err'], fmt='o', markersize=4, capsize=2, label=camera)
        ax2.errorbar(cam_lc['hjd']-2457000, cam_lc['flux'], yerr=cam_lc['flux_err'], fmt='o', markersize=4, capsize=2, label=camera)
    ax1.invert_yaxis()
    ax1.set_ylabel("Magnitude")
    ax2.set_ylabel("Flux (mJy)")
    ax2.set_xlabel("Time (HJD-2457000)")
    ax1.legend(loc="upper right")
    ax2.legend(loc="upper right")
    fig.tight_layout(rect=[0, 0.03, 1, 0.98])
    fig.savefig("test.png")
    plt.show()


if __name__ == "__main__":
    file_path = sys.argv[1]
    plot_lightcurve(file_path)