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
      print('x={}, y={}'. format(x,y))

def QIM_encode_twobit(sensor_data):
  #for now we assume that the watermark is sequence 0,1,2,3
  message = 0
  modified_sensor_data = []
  for sens_data in sensor_data:
    if sens_data.get_name() == "radar":
      x,y,vx,vy = sens_data.get()
      print('initial',x,y)
      pc_in = np.array([x,y])
      quant_two_bit_value = qim_quantize_twobit(pc_in, message)
      # print('embedded quantized value x={},y={}'. format(quant_two_bit_value[0], quant_two_bit_value[1]) )
      qim_encoded_pointcloud = getPointCloud_from_quantizedValues( quant_two_bit_value)
      sens_data.set_raw_radar(qim_encoded_pointcloud[0], qim_encoded_pointcloud[1])
      x,y,vx,vy = sens_data.get()
      modified_sensor_data.append([x,y,vx,vy])
      # print('final', x,y)
      message += 1
      message %= 4
  return modified_sensor_data

if __name__ == '__main__':
 
    #get the ground truths and the measurement data from input file data-1.txt
    all_sensor_data, all_ground_truths = parse_data("data/data_radargt.txt")
    #print('before*************)
    debug_print_sensordata(all_sensor_data)
    new_sensor_data = QIM_encode_twobit(all_sensor_data)
    print('After*************')
    for x in new_sensor_data:
      print('x={},y={}'. format(x[0], x[1]))

    # modify the px, py using two bit QIM


    # #get the predictions from the EKF class
    # all_state_estimations = get_state_estimations(EKF1, all_sensor_data)
    # #calculate the RMSE between the estimations and ground truths
    # px, py, vx, vy = get_RMSE(all_state_estimations, all_ground_truths)
    # #print the EKF data
    # print_EKF_data(all_sensor_data, all_ground_truths, all_state_estimations, 
    #            RMSE = [px, py, vx, vy])