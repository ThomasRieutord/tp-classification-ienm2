#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MODULE D'AIDE POUR LE TP DE CLASSIFICATION
Ne cherchez pas la correction ici, elle n'y est pas...

Date : 13/12/2020
Auteur : Thomas Rieutord (thomas.rieutord@meteo.fr)
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import datetime as dt

def solution_bonus1(alldata_pd):
    '''Solution aux questions bonus sur la mise en forme des données avec des
    dataframe Pandas.
    
    Parameters
    ----------
    alldata_pd: pandas.Dataframe
        Données issues de la lecture du fichier avec `pandas.read_csv`
    
    Returns
    -------
    TN_pd: pandas.Dataframe
        Sous-ensemble des données ne contenant que les Tn et indexé par le temps
    '''
    TN_pd = alldata_pd.iloc[:,1::2]
    TN_pd.index = [dt.datetime.strptime(str(d), "%Y%m%d") for d in alldata_pd.DATE]
    
    return TN_pd


def plot_silhouette(silhouette_values,labels,method=""):
    '''Fonction pour tracer la silhouette des différents clusters à partir
    des coefficients de silhouette calculés en chaque point de l'échantillon
    
    Parameters
    ----------
    silhouette_values: ndarray of shape (N,)
        Coefficients de silhouette en chaque point de l'échantillon.
    
    labels: ndarray of shape (N,)
        Numéro du cluster auquel appartient chaque point.
    
    method: str, optional
        Nom de la méthode utilisée pour le clustering (pour titre)
    
    Returns
    -------
    Creates a matplotlib.pyplot figure.
    '''
    
    if np.min(labels)!=0:
        labels-=np.min(labels)
    
    # Number of clusters
    K=int(np.max(labels))+1
    
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    plt.figure()
    plt.title("Graphe de silhouette "+method)
    y_spacing=int(labels.size/15)
    y_lower = y_spacing
    for k in range(K):
        # Aggregate the silhouette scores for samples belonging to
        # cluster k, and sort them
        kth_cluster_silhouette_values = silhouette_values[labels == k]
        
        kth_cluster_silhouette_values.sort()
        
        size_cluster_k = kth_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_k
        
        color = cm.nipy_spectral(float(k) / K)
        plt.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            kth_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7
        )
        
        # Label the silhouette plots with their cluster numbers at the middle
        plt.text(-0.05, y_lower + 0.5 * size_cluster_k, str(k))
        
        # Compute the new y_lower for next plot
        y_lower = y_upper + y_spacing  # 10 for the 0 samples
        
    plt.xlabel("The silhouette coefficient values")
    plt.ylabel("Cluster label")
    plt.show(block=False)
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
