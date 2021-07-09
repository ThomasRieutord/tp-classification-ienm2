#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DATA PREPARATION FOR THE PRACTICAL WORK OF UNSUPERVISED CLASSIFICATION WITH METEONET DATA.

@creationdate : 08/07/2021
@author : Thomas Rieutord (thomas.rieutord@meteo.fr)
"""

import os
import sys
import pandas as pd
import numpy as np
import datetime as dt


mtoparams = ["t","precip"]
input_file = os.path.join("no_save", "SE2018.csv")
output_file = os.path.join("..", "data", "obs_SE_2018.csv")

# OBSERVATIONS
#==============
print("Reading observation data...")

# Read data
#-----------
df = pd.read_csv(input_file,parse_dates=[4],infer_datetime_format=True)


d0 = df['date'][0]
datebins = [(d0 + k*dt.timedelta(days=1)) for k in range(365+1)]
stations = np.unique(df['number_sta'])
N_raw = np.unique(df['number_sta']).size
p = len(mtoparams)*(len(datebins)-1)

# Filter missing data
#---------------------
toolbar_width = int(N_raw/50) + 1
sys.stdout.write(
    "\nFilter missing data : [%s]" % ("." * toolbar_width)
)
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width + 1))

valid_stations = []
valid_lat = []
valid_lon = []
i=0
for sta in stations:
    
    if np.mod(i, 50) == 0:
            sys.stdout.write("*")
            sys.stdout.flush()
    
    idx = df["number_sta"]==sta
    lat, lon = df.loc[idx,['lat','lon']].values[0]
    df_sta = df.loc[idx,['date']+mtoparams]
    
    date1j = np.digitize(
        [d.timestamp() for d in df_sta['date']],
        [d.timestamp() for d in datebins]
    )
    
    data = df_sta.loc[:,mtoparams].groupby(date1j).mean().values.ravel()
    if np.isnan(data).sum()==0 and data.shape == (p,):
        valid_stations.append(sta)
        valid_lat.append(lat)
        valid_lon.append(lon)
    i+=1
sys.stdout.write("]\n")
N = len(valid_stations)
print(N, "valid stations (",N/N_raw*100,"%)")

# Extract relevant data
#-----------------------

toolbar_width = int(N/50) + 1
sys.stdout.write(
    "\nExtract relevant data : [%s]" % ("." * toolbar_width)
)
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width + 1))

X = np.zeros((N,p))

i=0
for sta in valid_stations:
    if np.mod(i, 50) == 0:
            sys.stdout.write("*")
            sys.stdout.flush()
    
    idx = df["number_sta"]==sta
    df_sta = df.loc[idx,['date']+mtoparams]
    date1j = np.digitize(
        [d.timestamp() for d in df_sta['date']],
        [d.timestamp() for d in datebins]
    )
    X[i,:] = df_sta.loc[:,mtoparams].groupby(date1j).mean().values.ravel()
    i+=1

sys.stdout.write("]\n")


# Save data in a csv file
#-------------------------
tcolnames = ["t-"+d.strftime("%Y-%m-%d") for d in datebins[:-1]]
hucolnames = ["hu-"+d.strftime("%Y-%m-%d") for d in datebins[:-1]]
colnames = []
for t,hu in zip(tcolnames,hucolnames):
    colnames += [t,hu]

df_obs = pd.DataFrame(index=valid_stations, columns=colnames, data=X)
df_obs['lat'] = valid_lat
df_obs['lon'] = valid_lon
df_obs.to_csv(output_file)
print("Data from observations saved in ", output_file)
