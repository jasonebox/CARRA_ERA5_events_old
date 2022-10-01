#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Adrien Wehrlé, University of Zurich, Switzerland

"""

import pygrib
import sys
import numpy as np
import xarray as xr

sys.path.append("/home/adrien/EO-IO/geomatcher")
import geomatcher.geomatcher as gm

# %% read ERA5 example

grbs = pygrib.open(
    "/home/adrien/EO-IO/CARRA_ERA5_events/data/ERA5/tcwv/202206_3hourly_tcwv.grib"
)

grbs.seek(0)
for grb in grbs:
    print(grb)

selected_grb = grbs.select(name="Total column water vapour")[0]

era5_ex, era5_lats, era5_lons = selected_grb.data()

era_grid = np.dstack([era5_ex, era5_lats, era5_lons])

# %% read CARRA grid

fn = "/home/adrien/EO-IO/CARRA_rain/ancil/CARRA_W_elev_lat_lon.nc"

carra_ds = xr.open_dataset(fn)

carra_elev = np.array(carra_ds["z"])
carra_lat = np.array(carra_ds["latitude"])
carra_lon = np.array(carra_ds["longitude"])

carra_grid = np.dstack([carra_elev, carra_lat, carra_lon])

# %%

m2m_results = gm.match_m2m(era5_grid, carra_grid)
