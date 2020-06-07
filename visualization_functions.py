# # #** This piece of code contants methods to visualize the following
# RMSE plots for multiple values of the R matrix and radar data generator sigma
# A route display and the predicted value display for the original and encoded data
# List of plots for the paper
# 1. six plots: Three plots each for px, py: RMSE for clean and encoded frames at different variances of the R matrix (x axis) and generator data (y-axis) for a given step size
# 2. Localization accuracy box plots for multiple runs of same data at different noise sigmas on x-axis (step <threshold, ==threshold, > threshold)
# one for each (delete, add and modify)
# 3. BER box plots for different data frames at different stepsizes
# 4. False alaram rate of different frames at different step sizes
# 5. prediction sample: GT, prediction without encoding and with encoding)
# # **#

from datapoint import DataPoint
import numpy as np
import matplotlib.pyplot as plt

def path_plots(gt_xs, gt_ys, clean_xs, clean_ys, encoded_xs, encoded_ys):
    # print((gt_xs))
    plt.plot(gt_xs,gt_ys, 'b*', label='Ground truth path')
    plt.plot(clean_xs,clean_ys, 'go', label='Path prediction on clean frames')
    plt.plot(encoded_xs,encoded_ys, 'r*', label='Path prediction on encoded frames')
    
    plt.title('Path taken by the vehicle')
    plt.xlabel('position x (px)')
    plt.ylabel('position y (py)')
    plt.legend(loc='best')
    plt.show()

# path_visualize(all_ground_truths, clean_all_sensor_data, clean_all_state_estimations, encoded_all_sensor_data, encoded_all_state_estimations)

def path_visualize(all_ground_truths, clean_all_state_estimations, encoded_all_state_estimations):
    # lidar_xs, lidar_ys = [], []
    # radar_xs, radar_ys, radar_angles = [], [], []

    gt_xs, gt_ys, gt_angles = [], [], []
    clean_xs, clean_ys, clean_angles = [], [], []
    encoded_xs, encoded_ys, encoded_angles = [], [], []
    
    print('gt length', len(all_ground_truths))
    print('cp length', len(clean_all_state_estimations))
    print('ep length', len(encoded_all_state_estimations))

    #gt = groundtruth, cm - clean measurement, cp-clean prediction, em - encoded measurement, ep- encoded prediction
    for gt, cp, ep in zip(all_ground_truths, clean_all_state_estimations, encoded_all_state_estimations):
    
        x, y, vx, vy = gt.get()
        t_angle =  np.arctan2(vy, vy)
        gt_xs.append(x)
        gt_ys.append(y)
        gt_angles.append(t_angle)

        x, y, vx, vy = cp.get()
        p_angle =  np.arctan2(vy, vx)
        clean_xs.append(x)
        clean_ys.append(y)
        clean_angles.append(p_angle)

        x, y, vx, vy = ep.get()
        p_angle =  np.arctan2(vy, vx)
        encoded_xs.append(x)
        encoded_ys.append(y)
        encoded_angles.append(p_angle)

    path_plots(gt_xs, gt_ys, clean_xs, clean_ys, encoded_xs, encoded_ys)

