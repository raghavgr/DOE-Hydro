import math 

import xarray as xr
import numpy as np
import pandas as pd
from pandas import Series

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.geoaxes import GeoAxes

"""
 Helper function to setup clim for colorbar
 Get max and min and setup ceiling:
   - by next fifth multiple if number 
       has more than two digits
   - else by 1
"""
def setup_clim(ls):
    if(max(ls) < 0):
        return (math.floor(min(ls)), math.ceil(max(ls)))
    if(min(ls) < 0):
        if(abs(min(ls)) < max(ls)):
            if (len(str(abs(max(ls))).split('.')[0]) < 2):
                return (math.ceil(-max(ls)), math.ceil(max(ls)))
            else:
                return (math.floor(-max(ls)/5)*5, math.ceil(max(ls)/5)*5)
        else:
            if (len(str(abs(min(ls))).split('.')[0]) < 2):
                return (math.floor(min(ls)), math.ceil(-min(ls)))
            else:
                return (math.floor(min(ls)/5)*5, math.ceil(-min(ls)/5)*5)
    else:
        if (len(str(abs(max(ls))).split('.')[0]) < 2):
            return (math.floor(min(ls)), math.ceil(max(ls)))
        else:
            return (math.floor(min(ls)/5)*5, math.ceil(max(ls)/5)*5)

"""
Develop the range for the colorbar
"""
def add_to_cbar(ds, clim_var, cbar_set):
    get_df = ds.to_dataframe()
    cbar_set.add(get_df[clim_var].min())
    cbar_set.add(get_df[clim_var].max())

"""
Calculate mean difference between two datasets,
historic and future.
Pass historic_start/historic_end in the format: 'yyyy-mm-dd'
"""
def mean_difference(historic, future, historic_start, historic_end, clim_var, season):
    historic_sliced = historic[clim_var].sel(time=slice(historic_start, historic_end))
    historic_mean = historic_sliced.groupby('time.season').mean('time')
    future_mean = future[clim_var].groupby('time.season').mean('time')
    if clim_var == 'pr':
        mean_difference = ((future_mean.sel(season=season) - historic_mean.sel(season=season)) / historic_mean.sel(season=season)) * 100
    elif clim_var == 'tas':
        mean_difference = future_mean.sel(season=season) - historic_mean.sel(season=season)

    return mean_difference

"""
Function to render the plot for mean difference
"""    
def render_plot(input_list, cbar_label_title, cbar_color, clim_var, season, models=['WRF', 'LOCA-WRF', 'LOCA-14', 'BCSD-14']):
    projection = ccrs.PlateCarree()
    axes_class = (GeoAxes, dict(map_projection=projection))
    fig = plt.figure(figsize=(15, 15))
    axgr = AxesGrid(fig, 
                111, 
                axes_class=axes_class,
                nrows_ncols=(1, 4),
                axes_pad=0.2,
                share_all=True,
                label_mode="",
                cbar_location="right",
                cbar_mode="single",
                cbar_pad=0.5
               )
    cbar_range = set()
    {add_to_cbar(i, clim_var, cbar_range) for i in input_list}
    for i, ax in enumerate(axgr):
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.STATES)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.LAKES)
        ax.add_feature(cfeature.LAND)    
        ax.add_feature(cfeature.LAKES.with_scale('10m'), facecolor='none', edgecolor='tab:blue')
        ax.add_feature(cfeature.RIVERS.with_scale('10m'), edgecolor='tab:blue')   
        # setting the location t
        ax.set_extent([-125, -116, 43, 35])
        djf_plt = input_list[i].plot.pcolormesh(ax=axgr[i], transform=ccrs.PlateCarree(), x='longitude', y='latitude', cmap=plt.get_cmap(cbar_color), add_colorbar=False)
        #djf_plt.set_clim(min(cbar_range), max(cbar_range))
        djf_plt.set_clim(setup_clim(cbar_range))
    
    [axgr[i].set_title(models[i]) for i in range(len(models))]
    
    fig.subplots_adjust(left=0.14, top=1.64)
    fig.suptitle('Mean difference of forecast and actual {0} data over the Sierra Nevada range, {1} Season'.format(expand_clim_var(clim_var), season), fontsize=16, y=1.01)
    cb = axgr.cbar_axes[0].colorbar(djf_plt)
    cb.set_label_text(cbar_label_title)
    fig.savefig('{0} Mean Difference during {1} over Sierra Nevada range.png'.format(expand_clim_var(clim_var=clim_var), season), dpi=150, bbox_inches="tight")

"""
Used for expanding the climate variables. 
Essential when rendering plots with labels
"""
def expand_clim_var(clim_var):
    switcher = {
        "pr": "Precipitation",
        "tas": "Temperature",
        "scf": "Snow covered fraction",
        "swe": "Snow water equivalence"
    }
    #print(switcher.get(clim_var, "Invalid variable given: {0}".format(clim_var)))
    return switcher.get(clim_var, "Invalid variable given: {0}".format(clim_var))