# -*- coding: utf-8 -*-
from kalmanfilter import KalmanFilter
from datapoint import DataPoint
from fusionekf import FusionEKF
from tools import get_RMSE
from helpers import parse_data, print_EKF_data, get_state_estimations
import numpy as np
from twoD_QIM import qim_quantize_twobit, getPointCloud_from_quantizedValues



lidar_R = np.matrix([[0.01, 0], 
                     [0, 0.01]])

radar_R = np.matrix([[0.01, 0, 0], 
                     [0, 0.000001, 0], 
                     [0, 0, 0.01]])

lidar_H = np.matrix([[1, 0, 0, 0],
                     [0, 1, 0, 0]])

P = np.matrix([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1000, 0], 
               [0, 0, 0, 1000]])

Q = np.matrix(np.zeros([4, 4]))
F = np.matrix(np.eye(4))

d = {
  'number_of_states': 4, 
  'initial_process_matrix': P,
  'radar_covariance_matrix': radar_R,
  'lidar_covariance_matrix': lidar_R, 
  'lidar_transition_matrix': lidar_H,
  'inital_state_transition_matrix': F,
  'initial_noise_matrix': Q, 
  'acceleration_noise_x': 5, 
  'acceleration_noise_y': 5
}

EKF1 = FusionEKF(d)
EKF2 = FusionEKF(d)

def debug_print_sensordata(sensor_data):
  for sens_data in sensor_data:
    if sens_data.get_name() == "radar":
      x,y,vx,vy = sens_data.get()
      print('x={}, y={}, vx={}, vy={}'. format(x,y,vx,vy))



if __name__ == '__main__':
 
    #get the ground truths and the measurement data from input file data-1.txt
    all_sensor_data = []
    all_ground_truths = []
    all_state_estimations = []
    all_sensor_data, all_ground_truths = parse_data("data/data-2.txt")
    print('plain radar sensor data\n')
    debug_print_sensordata(all_sensor_data)
    #get the predictions from the EKF class
    all_state_estimations = get_state_estimations(EKF1, all_sensor_data)
    
    
    
    #calculate the RMSE between the estimations and ground truths
    px, py, vx, vy = get_RMSE(all_state_estimations, all_ground_truths)
    #print RMSE
    print('\n')
    print('RMSE: px = {} | py = {} | vx = {} | vy = {}'. format(px, py, vx, vy))
    print('\n')
    print('\n')
    #print the EKF data
    # print_EKF_data(all_sensor_data, all_ground_truths, all_state_estimations, 
    #            RMSE = [px, py, vx, vy])


    all_sensor_data = []
    all_ground_truths = []
    all_state_estimations = []
    #get the ground truths and the measurement data from input file data-1.txt
    all_sensor_data, all_ground_truths = parse_data("data/data-2.txt", ENCODE= True)
    print('encoded radar sensor data\n')
    debug_print_sensordata(all_sensor_data)
    
    #get the predictions from the EKF class
    all_state_estimations = get_state_estimations(EKF1, all_sensor_data)
    #calculate the RMSE between the estimations and ground truths
    #print RMSE
    px, py, vx, vy = get_RMSE(all_state_estimations, all_ground_truths)
    print('\n')
    print('ENCODED RMSE: px = {} | py = {} | vx = {} | vy = {}'. format(px, py, vx, vy))
    print('\n')
    print('\n')

    # print the EKF data
    # print_EKF_data(all_sensor_data, all_ground_truths, all_state_estimations, 
    #            RMSE = [px, py, vx, vy])