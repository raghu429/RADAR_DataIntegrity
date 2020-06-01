# -*- coding: utf-8 -*-
"""
Created on Sun May 31 09:17:44 2020

@author: rchangs
"""

from kalmanfilter import KalmanFilter
from datapoint import DataPoint
from fusionekf import FusionEKF
from tools import get_RMSE, cartesian_to_polar
from helpers import parse_data, print_EKF_data, get_state_estimations
import numpy as np

def get_all_differences(all_sensor_data, all_ground_truths):

  pxs, pys, vxs, vys, rhos, phis, drhos = [], [], [], [], [], [], []

  for s, t in zip(all_sensor_data, all_ground_truths):
        
    if s.get_name() == 'lidar':
    
      spx, spy, _, _ = s.get()
      tpx, tpy, _, _ = t.get()

      pxs += [spx - tpx]
      pys += [spy - tpy]
      
    else:
        
      spx, spy, svx, svy = s.get()
      tpx, tpy, tvx, tvy = t.get()

      srho, sphi, sdrho = s.get_raw()
      trho, tphi, tdrho = cartesian_to_polar(tpx, tpy, tvx, tvy)
        
      pxs += [spx - tpx]
      pys += [spy - tpy]        
      vxs += [svx - tvx]
      vys += [svy - tvy]
      rhos += [srho - trho]
      phis += [sphi - tphi]
      drhos += [sdrho - tdrho]

    
  return pxs, pys, vxs, vys, rhos, phis, drhos

def get_variance(x):
  return np.var(np.array(x))

def print_variances(pxs, pys, vxs, vys, rhos, phis, drhos):
  print("x:", get_variance(pxs))
  print("y:", get_variance(pys))
  print("vx:", get_variance(vxs))
  print("vy:", get_variance(vys))
  print("rho:", get_variance(rhos))
  print("phi:", get_variance(phis))
  print("drho:", get_variance(drhos))

if __name__ == '__main__':
    all_sensor_data1, all_ground_truths1 = parse_data("data/data-1.txt")
    pxs1, pys1, vxs1, vys1, rhos1, phis1, drhos1 = get_all_differences(all_sensor_data1, all_ground_truths1)
    print_variances(pxs1, pys1, vxs1, vys1, rhos1, phis1, drhos1)
    print_variances(pxs1 + pxs2, pys1 + pys2, vxs1 + vxs2, 
                vys1 + vys2, rhos1 + rhos2, phis1 + phis2, drhos1 + drhos2)