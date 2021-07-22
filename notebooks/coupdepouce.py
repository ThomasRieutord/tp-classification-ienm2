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
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
from meteonet_toolbox.constant import DOMAINS
# Bugfix (13/07/2021): impossible de télécharger tuiles Cartopy
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def plot_clusters_on_map(labels, lats, lons, colormap="nipy_spectral"):
    """Positionne les stations sur une carte et les colore en fonction de leur
    cluster.
    
    
    Parameters
    ----------
    labels: ndarray of shape (N,)
        Numéro du cluster auquel appartient chaque point
    
    lats: ndarray of shape (N,)
        Latitude de toutes les stations
    
    lons: ndarray of shape (N,)
        Longitude de toutes les stations
    
    colormap: {str, list of 3-tuple}
        Jeu de couleur pour les clusters. Si ce paramètre est de type `str`, il
        doit être un nom de colormap connu de matplotlib. Sinon, il doit 
        contenir une list de couleurs au format RGB (3-tuple).
    
    
    Returns
    -------
    matplotlib.pyplot figure
    """
    
    if np.min(labels)!=0:
        labels-=np.min(labels)
    
    # Number of clusters
    K=int(np.max(labels))+1
    
    stamen_terrain = cimgt.Stamen('terrain-background')
    # Coordinates of studied area boundaries
    zone = "SE"
    lllat = DOMAINS[zone]['lry']  #lower left latitude
    urlat = DOMAINS[zone]['uly']  #upper right latitude
    lllon = DOMAINS[zone]['ulx']  #lower left longitude
    urlon = DOMAINS[zone]['lrx']  #upper right longitude
    extent = [lllon, urlon, lllat, urlat]
    
    fig = plt.figure(figsize=(10,10))
    
    # Create a GeoAxes in the tile's projection.
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    
    # Limit the extent of the map to a small loextent[minlon,maxlon,minlat,maxlat], crs=ccrs.Geodetic())
    ax.set_extent(extent)
    
    # Add the Stamen data. Start at zoom level 3, then try 6.
    ax.add_image(stamen_terrain, 6)
    
    resolution = '50m'
    ax.add_feature(
        cfeature.NaturalEarthFeature(
            'cultural',
            'admin_0_countries',
            resolution,
            edgecolor='black',
            facecolor='none'
        )
    )
    
    for k in range(K):
        dex = labels==k
        
        if isinstance(colormap,str):
            color = eval("cm."+colormap+"(float(k)/K)")
        else:
            color = colormap[k]
            
        ax.scatter(
            lons[dex],
            lats[dex],
            marker='o',
            color=color,
            s=60,
            alpha=1,
            transform=ccrs.Geodetic(),
            label='Cluster '+str(k)
        )
    plt.legend(loc='upper right')
    plt.show(block=False)


def plot_silhouette(silhouette_values,labels,method="", colormap="nipy_spectral"):
    '''Trace le profil de silhouette d'une classification.
    
    Le profil de silhouette représente le score de silhouette de tous les points,
    regroupés par clusters et classés par ordre croissant. Un score de silhouette
    négatif indique des points mal classifiés et donc une potentielle mauvaise
    classification.
    
    
    Parameters
    ----------
    silhouette_values: ndarray of shape (N,)
        Coefficients de silhouette en chaque point de l'échantillon.
    
    labels: ndarray of shape (N,)
        Numéro du cluster auquel appartient chaque point.
    
    method: str, optional
        Nom de la méthode utilisée pour le clustering (pour titre)
    
    colormap: {str, list of 3-tuple}
        Jeu de couleur pour les clusters. Si ce paramètre est de type `str`, il
        doit être un nom de colormap connu de matplotlib. Sinon, il doit 
        contenir une list de couleurs au format RGB (3-tuple).
    
    Returns
    -------
    matplotlib.pyplot figure
    '''
    
    if np.min(labels)!=0:
        labels-=np.min(labels)
    
    # Number of clusters
    K=int(np.max(labels))+1
    
    plt.figure()
    plt.title("Profil de silhouette "+method)
    y_spacing=int(labels.size/15)
    y_lower = y_spacing
    for k in range(K):
        # Aggregate the silhouette scores for samples belonging to
        # cluster k, and sort them
        kth_cluster_silhouette_values = silhouette_values[labels == k]
        
        kth_cluster_silhouette_values.sort()
        
        size_cluster_k = kth_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_k
        
        if isinstance(colormap,str):
            color = eval("cm."+colormap+"(float(k)/K)")
        else:
            color = colormap[k]
        
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
