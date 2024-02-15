import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from metpy.cbook import get_test_data
from metpy.interpolate import (interpolate_to_grid, remove_nan_observations,
                               remove_repeat_coordinates)
from metpy.plots import add_metpy_logo
from matplotlib.colors import BoundaryNorm, ListedColormap
import geopandas as gpd
from shapely.geometry import Point

def basic_map(proj, title):
    """Make our basic default map for plotting"""
    fig = plt.figure(figsize=(15, 10))
    add_metpy_logo(fig, 0, 80, size='large')
    view = fig.add_axes([0, 0, 1, 1], projection=proj)
    view.set_title(title)
    view.set_extent([20, 30, 55, 59])
    #view.add_feature(cfeature.STATES.with_scale('10m'))
    view.add_feature(cfeature.OCEAN)
    view.add_feature(cfeature.COASTLINE.with_scale('10m'))
    view.add_feature(cfeature.BORDERS, linestyle='solid')
    return fig, view

def station_test_data(file_path, variable_names, proj_from=None, proj_to=None):
    with open(file_path, 'r') as f:
        all_data = np.loadtxt(f, skiprows=1, delimiter=',',
                              usecols=(1, 2, 4),
                              dtype=np.dtype([('lat', 'f'), ('lon', 'f'), ('air_temperature', 'f')]))

    lat = all_data['lat']
    lon = all_data['lon']
    temp = all_data['air_temperature']

    if proj_from is not None and proj_to is not None:
        proj_points = proj_to.transform_points(proj_from, lon, lat)
        return proj_points[:, 0], proj_points[:, 1], temp

    return lon, lat, temp

from_proj = ccrs.Geodetic()
to_proj = ccrs.Mercator()

levels = list(range(-50, 50, 1))

# Define your custom colors
custom_colors = [
"rgb(255,255,255)",
                "rgb(255,245,255)",
                "rgb(255,230,255)",
                "rgb(255,220,255)",
                "rgb(255,205,255)",
                "rgb(255,190,255)",
                "rgb(255,175,255)",
                "rgb(255,160,255)",
                "rgb(255,145,255)",
                "rgb(255,135,255)",
                "rgb(255,120,255)",
                "rgb(255,110,255)",
                "rgb(255,100,255)",
                "rgb(255,90,255)",
                "rgb(255,80,255)",
                "rgb(255,70,255)",
                "rgb(255,60,255)",
                "rgb(255,50,255)",
                "rgb(255,35,255)",
                "rgb(255,15,255)",
                "rgb(255,0,255)",
                "rgb(240,0,240)",
                "rgb(230,0,230)",
                "rgb(220,0,220)",
                "rgb(200,0,200)",
                "rgb(190,0,180)",
                "rgb(175,0,165)",
                "rgb(160,0,150)",
                "rgb(145,0,140)",
                "rgb(135,0,130)",
                "rgb(115,0,125)",
                "rgb(90,0,115)",
                "rgb(65,0,115)",
                "rgb(35,0,115)",
                "rgb(10,0,120)",
                "rgb(0,0,128)",
                "rgb(0,0,160)",
                "rgb(0,0,190)",
                "rgb(0,0,225)",
                "rgb(0,0,255)",
                "rgb(0,35,255)",
                "rgb(0,65,255)",
                "rgb(0,85,255)",
                "rgb(0,110,255)",
                "rgb(0,128,255)",
                "rgb(0,145,255)",
                "rgb(0,170,255)",
                "rgb(0,195,255)",
                "rgb(0,215,255)",
                "rgb(0,230,255)",
                "rgb(0,255,255)",
                "rgb(0,255,128)",
                "rgb(0,255,95)",
                "rgb(0,255,70)",
                "rgb(0,255,40)",
                "rgb(0,255,0)",
                "rgb(70,255,0)",
                "rgb(110,255,0)",
                "rgb(140,255,0)",
                "rgb(165,255,0)",
                "rgb(185,255,0)",
                "rgb(205,255,0)",
                "rgb(220,255,0)",
                "rgb(235,255,0)",
                "rgb(255,255,0)",
                "rgb(255,240,0)",
                "rgb(255,220,0)",
                "rgb(255,195,0)",
                "rgb(255,165,0)",
                "rgb(255,140,0)",
                "rgb(255,120,0)",
                "rgb(255,100,0)",
                "rgb(255,80,0)",
                "rgb(255,60,0)",
                "rgb(255,30,0)",
                "rgb(255,0,0)",
                "rgb(245,0,0)",
                "rgb(235,0,0)",
                "rgb(220,0,0)",
                "rgb(205,0,0)",
                "rgb(195,0,0)",
                "rgb(180,0,0)",
                "rgb(165,0,0)",
                "rgb(150,0,0)",
                "rgb(135,0,0)",
                "rgb(120,0,0)",
                "rgb(110,0,0)",
                "rgb(100,0,0)",
                "rgb(90,0,0)",
                "rgb(75,0,0)",
                "rgb(60,0,0)",
                "rgb(60,20,20)",
                "rgb(60,40,40)",
                "rgb(60,60,60)",
                "rgb(80,80,80)",
                "rgb(100,100,100)",
                "rgb(120,120,120)",
                "rgb(140,140,140)",
                "rgb(160,160,160)",
                "rgb(180,180,180)",
]

# Convert custom colors to RGB tuples
custom_rgb_colors = [(int(color.split('(')[1].split(',')[0]) / 255,
                      int(color.split(',')[1]) / 255,
                      int(color.split(',')[2].split(')')[0]) / 255) for color in custom_colors]

# Create a ListedColormap
custom_cmap = ListedColormap(custom_rgb_colors)

norm = BoundaryNorm(levels, ncolors=custom_cmap.N, clip=True)

file_path = r'C:\MeteoLatvia\Coding\MetPy\Observations\LVGMC-Temperature.txt'
x, y, temp = station_test_data(file_path, 'air_temperature', from_proj, to_proj)

x, y, temp = remove_nan_observations(x, y, temp)
x, y, temp = remove_repeat_coordinates(x, y, temp)

gx, gy, img = interpolate_to_grid(x, y, temp, interp_type='rbf', hres=60000, rbf_func='linear',
                                  rbf_smooth=60000)
img = np.ma.masked_where(np.isnan(img), img)

fig, view = basic_map(to_proj, 'Gaisa temperatūra plkst. 10:00')
contourf = view.contourf(gx, gy, img, levels=levels, cmap=custom_cmap, extend='both')
#fig.colorbar(contourf, shrink=.4, pad=0, boundaries=levels)

# Add contour lines without labels and specify line style for all levels
contour = view.contour(gx, gy, img, levels=levels, colors='k', linestyles='-', linewidths=0.5)
plt.clabel(contour, inline=True, fontsize=12)

# Plot points
#view.scatter(x, y, color='black', marker='o', s=10)

# Annotate points with temperature values
#for i, txt in enumerate(temp):
    #view.annotate(f'{txt:.1f}', (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=12)

#plt.show()
plt.savefig('15.02.2024.1701.png', dpi=600, bbox_inches='tight')
