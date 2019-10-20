# -*- coding: utf-8 -*-
from netCDF4 import Dataset
import numpy as np
dset1 = Dataset('pentad_20111227_v11l35flk.nc.gz.nc4')
dset2 = Dataset('world_oscar_vel_5d2019.nc.gz.nc4')

"""Read the `uf` data to numpy array."""

uAir = dset1.variables['uwnd'][0].data * 0.00152597204
vAir = dset1.variables['vwnd'][0].data * 0.00152597204

uWater = dset2.variables['uf'][0][0].data
vWater = dset2.variables['vf'][0][0].data

uAir[uAir < -50] = np.nan
uAir[uAir > 50] = np.nan

vAir[vAir < -50] = np.nan
vAir[vAir > 50] = np.nan

lonAir = dset1.variables['lon']
latAir = dset1.variables['lat']

lonWater = dset2.variables['longitude']
latWater = dset2.variables['latitude']

import matplotlib.pyplot as plt
import random as rd
import turtle as t

factor = 0.1 # 상수

def findNext(latitude, longitude): # 위도, 경도
    global factor, uAir, vAir, uWater, vWater, lonAir, latAir, lonWater, latWater
    
    latAir2 = gridAir(latitude, latAir[0])  % len(latAir)
    lonAir2 = gridAir(longitude, lonAir[0])  % len(lonAir)
    uAir2 = uAir[latAir2][lonAir2]
    vAir2 = vAir[latAir2][lonAir2]
    if np.isnan(uAir2) or np.isnan(vAir2):
        return False

    latWater2 = len(latWater) - 1 - gridWater(latitude, latWater[0]) % len(latWater)
    lonWater2 = gridWater(longitude, lonWater[0]) % len(lonWater)
    uWater2 = uWater[latWater2][lonWater2]
    vWater2 = vWater[latWater2][lonWater2]

    if np.isnan(uWater2) or np.isnan(vWater2):
        return False
    
    finPhi = latitude + factor * (vAir2 + vWater2)
    finTheta = longitude + factor * (uAir2 + uWater2)
    
    if finTheta < lonAir[0]:
        amount = lonAir[0] - finTheta
        finTheta = lonAir[-1] - amount
        
    if finTheta > lonAir[-1]:
        amount = finTheta - lonAir[-1]
        finTheta = lonAir[0] + amount
    
    return (finPhi, finTheta) # 위도, 경도

def gridAir(A, org):
    return 4 * int(round(4*(A % 1)) / 4 + np.floor(A) - org)

def gridWater(A, org):
    return int(round(A - 0.5) + 0.5 - org) 

def findStart():
    global uAir, vAir, uWater, vWater, lonAir, latAir, lonWater, latWater
    longitude = rd.uniform(lonAir[0], lonAir[-1])
    latitude = rd.uniform(latAir[0], latAir[-1])
    Theta = gridAir(latitude, latAir[0]) % len(latAir)
    Phi = gridAir(longitude, lonAir[0]) % len(lonAir)
    while np.isnan(uAir[Theta][Phi]):
        longitude = rd.uniform(lonAir[0], lonAir[-1])
        latitude = rd.uniform(latAir[0], latAir[-1])
        Theta = gridAir(latitude, latAir[0]) % len(latAir)
        Phi = gridAir(longitude, lonAir[0]) % len(lonAir)
    return latitude, longitude # 위도, 경도

def euclidD(A, B):
    return pow((A[0] - B[0])**2 + (A[1] - B[1])**2, 0.5)

creator = t.Turtle()
screen = t.Screen()

screen.setworldcoordinates(-180, -80, 180, 80)
screen.bgpic("Background.png")
screen.title("Route")
screen.setup(1.0, 1.0, 0.0, 0.0)

plt.figure(figsize=(12.8, 9.6))
plt.quiver(lonAir[::8], latAir[::8], uAir[::8, ::8], vAir[::8, ::8], color = "#000000", scale = 3, scale_units = 'x')
plt.quiver(lonWater[::2] - 20.5, latWater[::2], np.c_[uWater[::2, -20::2], uWater[::2, 0:340:2]], np.c_[vWater[::2, -20::2], vWater[::2, 0:340:2]], color = "#0000FF", scale = 3, scale_units = 'x')

prevposition = (int(input("Latitude: ")), int(input("Longitude: ")))  # lat & lon
routeX = [prevposition[1]] # lon
routeY = [prevposition[0]] # lat
print(f"Start Point : {prevposition}")

for i in range(1000) :
    position = findNext(prevposition[0], prevposition[1])
    if not position or euclidD(position, prevposition) <= 1e-5:
        break
    routeY.append(position[0]) # lat
    routeX.append(position[1]) # lon
    prevposition = position
    
plt.scatter(routeX, routeY, 0.1)
plt.show()
print("E")

