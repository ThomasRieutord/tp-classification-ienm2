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


mtoparams = ["t","ff","precip"]
predictors = ["Tn","Tx","FFmax","RR"]
input_file = os.path.join("no_save", "SE2018.csv")
output_file = os.path.join("..", "data", "obs_SE_2018.csv")

# OBSERVATIONS
#==============
print("Reading observation data...")

# Read data
#-----------
df = pd.read_csv(input_file,parse_dates=[4],infer_datetime_format=True)


d0 = df['date'][0]
ndaysbatch = 1
datebins = [(d0 + k*dt.timedelta(days=ndaysbatch)) for k in range(int(365/ndaysbatch) + 1)]
stations = np.unique(df['number_sta'])
n_sta = np.unique(df['number_sta']).size

# Filter missing data
#---------------------
toolbar_width = int(n_sta/50) + 1
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
    if np.isnan(data).sum()==0:
        valid_stations.append(sta)
        valid_lat.append(lat)
        valid_lon.append(lon)
    i+=1
sys.stdout.write("]\n")

N = len(valid_stations)
p = len(predictors)
print(N, "valid stations (",N/n_sta*100,"%)")

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
    for j in range(len(predictors)):
        pred = predictors[j]
        if pred=="Tn":
            X[i,j] = df_sta.loc[:,"t"].groupby(date1j).min().mean()
        elif pred=="Tx":
            X[i,j] = df_sta.loc[:,"t"].groupby(date1j).max().mean()
        elif pred=="FFmax":
            X[i,j] = df_sta.loc[:,"ff"].groupby(date1j).max().mean()
        elif pred=="RR":
            X[i,j] = df_sta.loc[:,"precip"].sum()
        else:
            raise ValueError("Invalid predictor alias")
    i+=1

sys.stdout.write("]\n")


# Save data in a csv file
#-------------------------

df_obs = pd.DataFrame(index=valid_stations, columns=predictors, data=X)
df_obs['lat'] = valid_lat
df_obs['lon'] = valid_lon

if df_obs.isna().sum().sum() != 0:
    raise ValueError("Remaing NaN in the dataset")

df_obs.to_csv(output_file)
print("Data from observations saved in ", output_file)
