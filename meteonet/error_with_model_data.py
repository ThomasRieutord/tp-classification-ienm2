#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DATA PREPARATION FOR THE PRACTICAL WORK OF UNSUPERVISED CLASSIFICATION WITH METEONET DATA.

@creationdate : 08/07/2021
@author : Thomas Rieutord (thomas.rieutord@meteo.fr)
"""

import os
import meteonet_toolbox.user_configuration
import xarray as xr
import pandas as pd
import numpy as np
import datetime as dt


output_file = os.path.join("..", "data", "obs_SE_2018.csv")
model = 'arpege' #weather model (arome or arpege)
level = '10m'      #vertical level (2m, 10m, P_sea_level or PRECIP)

# MODEL
#==============


# Read data
#-----------
d0 = dt.datetime(2018,7,16)
month = d0.month
fname = "_".join([model.lower(), level, "SE", d0.strftime("%Y%m%d%H%M%S")])+".grib"
input_file = os.path.join(
    "no_save",
    "2018"+str(month).zfill(2),
    model.upper(),
    level,
    fname
)

df = xr.open_dataset(input_file, engine='cfgrib')

