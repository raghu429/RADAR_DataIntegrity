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
    
#this code plots the difference in the encoded path and the clean path estimate using subplots
    fig, axs = plt.subplots(2, 2)
    axs[0,0].plot(gt_xs, gt_ys, label='Ground Truth', color = 'r')
    axs[0,0].set_title('Plain Estimate')
    axs[0,0].plot(clean_xs, clean_ys, label='Plain Predicted Path', color = 'c')
    axs[0,0].set(xlabel='position x (px)', ylabel='position y (py)')
    # axs[0,0].legend(loc="upper left")
    # axs[0, 0].set_title('Axis [0,0]')

    # fig, axs = plt.subplots(1, 2)
    axs[0,1].plot(gt_xs, gt_ys,  label='Ground Truth', color = 'r')
    axs[0,1].set_title('Encoded Estimate')
    axs[0,1].plot(encoded_xs, encoded_ys, label='Encoded Path', color='c')
    # axs[0,1].legend(loc="upper right")
    axs[0,1].set(xlabel='position x (px)', ylabel='position y (py)')
    axs[0,1].legend(bbox_to_anchor=(1, 1))
    

    axs[1,0].plot(gt_xs,  label='Ground Truth', color = 'r')
    axs[1,0].plot(clean_xs, label='Clean Path', color='k')
    axs[1,0].plot(encoded_xs, label='Encoded Path', color='c')
    axs[1,0].set_title('Plain Vs Encoded Estimate')
    axs[1,0].set(xlabel='time ')
    axs[1,0].set(ylabel='position x (px)')
    # axs[1,0].legend(bbox_to_anchor=(-1.05, -1))

    axs[1,1].plot(gt_ys,  label='Ground Truth', color = 'r')
    axs[1,1].plot(clean_ys, label='Clean Path', color='k')
    axs[1,1].plot(encoded_ys, label='Encoded Path', color='c')
    axs[1,1].set_title('Plain Vs Encoded Estimate')
    axs[1,1].legend(bbox_to_anchor=(1, 1))
    axs[1,1].set(ylabel='position y (py)')
    axs[1,1].set(xlabel='time')
    plt.show()

def visulalize_accuracy(delta_range, del_list, add_list, modify_list):
    plt.plot(delta_range, del_list, '*-b', label='Delete')
    plt.plot(delta_range, add_list, 'o-y', label='Add')
    plt.plot(delta_range, modify_list, '+-r', label='Modify')

    plt.title('Performance against different attack vectors')
    plt.xlabel('Step Size')
    plt.ylabel('Accuracy')
    plt.legend(loc='best')
    plt.show()

def visulalize_RMSE(variance_list, RMSE_x_en, RMSE_x_cl, RMSE_y_en, RMSE_y_cl):

    fig, axs = plt.subplots(1, 2)
    axs[0].set_title('Px at step-size 0.5')
    axs[0].plot(variance_list, RMSE_x_cl, label='clean', color = 'g')
    axs[0].plot(variance_list, RMSE_x_en, label='encoded', color = 'r')
    axs[0].set(xlabel='covarance', ylabel='RMSE')
    axs[0].legend(loc="upper left")

    axs[1].set_title('Py at step-size 0.5')
    axs[1].plot(variance_list, RMSE_y_cl, label='clean', color = 'g')
    axs[1].plot(variance_list, RMSE_y_en, label='encoded', color = 'r')
    axs[1].set(xlabel='covarance', ylabel='RMSE')
    axs[1].legend(loc="upper Right")
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

