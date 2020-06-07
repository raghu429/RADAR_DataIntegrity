# -*- coding: utf-8 -*-
import numpy as np
import random

from tools import polar_to_cartesian, cartesian_to_polar
from twoD_QIM import qim_quantize_twobits, getPointCloud_from_quantizedValues, qim_decode, NUMBITS, qim_dummy_encoded_pc, get_tamperedindices_twobits


# #** This piece of code contants methods to evaluate the 2D QIM embedding for the given Udacity data-set. We can further split this file into three different files if needed (most of the previously developed code could be re-used)
# First - read the data file and generate a separate binary file with just the radar data
# Add noise to the data if required (uniform or Gaussian with variable delta)
# simulate the attack vectors, like add, delete or modify the random line items in the above generated file
# get the detections out of the modified files and report the false alarms, error rate and accuracy (if the algorithm is able to detect the location of the modified data)
# **#


def radarDataExtractor(filePath):
    with open(filePath) as read_file:
        # read_file = open(filePath, "R")
        radar_data = []
        count  = 0
        for line in read_file:
            data = line.split()
            if(data[0] == 'R'):
                [x, y, vx, vy] = polar_to_cartesian(float(data[1]),float(data[2]),float(data[3]))
                radar_data.append([x, y])
            count += 1 # restrict it to 100 elements
            # if (count == 50):
                # break
                
    return radar_data

def tamperRadarAddUniformNoise(noise_sigma, data_in):
    uniform_noise_added_data = data_in + np.random.uniform(-noise_sigma, noise_sigma, 2*len(data_in)).reshape(-1,2)
    return uniform_noise_added_data

def tamperRadarAddTracklets(data_in):
    data_out = data_in
    #this tell how many data element syou want to tamper
    data_corruption_range = 30
    #sorted non-duplicate list
    random_list = np.sort(random.sample(range(2, (np.shape(data_in)[0]-1)), data_corruption_range))
    # print('random list', random_list, len(random_list))
    add_location_list = []
    for rl in random_list:
        # print('data length ={}'.format(np.shape(data_in)[0]))
        #copy a previous row element from the data
        copy_row = data_out[rl-1]
        #paste it at a random location
        data_out = np.insert(data_out, rl, copy_row, axis = 0)
        add_location_list.append(rl)
    return add_location_list, data_out

def tamperRadarDeleteTracklets(data_in):
    data_out = data_in
    data_corruption_range = 30
    random_list = np.sort(random.sample(range(2, (np.shape(data_in)[0]-1)), data_corruption_range))
    data_out = np.delete(data_in, random_list, axis = 0)
    return random_list, data_out
    
def tamperRadarModifyTracklets(data_in):
    data_out = data_in
    mod_location_list = []
    data_corruption_range = 30
    random_list = np.sort(random.sample(range(2, (np.shape(data_in)[0]-1)), data_corruption_range))
    for rl in random_list:
        # r1 = random.randint(0, np.shape(data_in)[0]-2)
        #modify a rwo element in the data
        data_out[rl] =  data_out[rl+1]
        mod_location_list.append(rl)
    return mod_location_list, data_out


#these three functions check for the missing indices, added indices and modified indices assuming the input is a list of repeating pattens

def findDeletedIndices(gt_list, mod_list):
    #here the assumption is that the lenth of the mod_list < gt_list
    gt_index = 0
    mod_index = 0
    missing_indices = []
    while(mod_index < len(mod_list) or gt_index < len(gt_list)):
        if(gt_list[gt_index] ==  mod_list[mod_index]):
            mod_index += 1
            gt_index += 1
            continue
        print('missing index = {}, missing element = {}'. format((gt_index), gt_list[gt_index]))
        missing_indices.append(gt_index)
        gt_index += 1
    return missing_indices

def findModifiedIndices(gt_list, mod_list):
    #here both the lengths are same
    different_indices = []
    index = 0
    while(index < len(mod_list)):
        if(gt_list[index] ==  mod_list[index]):
            index += 1
            continue
        print('index = {}, different element = {}'. format((index), mod_list[index]))
        different_indices.append(index)
        index += 1

    return different_indices

def findAddedIndices(gt_list, mod_list):
    gt_index = 0
    mod_index = 0
    added_indices = []
    while(mod_index < len(mod_list) or gt_index < len(gt_list)):
        if(gt_list[gt_index] ==  mod_list[mod_index]):
            mod_index += 1
            gt_index += 1
            continue
        print('index = {}, added element = {}'. format((mod_index), mod_list[mod_index]))
        added_indices.append(mod_index)
        mod_index += 1
    return added_indices


if __name__ == '__main__':
    # #test missing
    # print('******Deleted Elements Test******')
    # list_orig = [1,2,3,4,1,2,3,4,1,2,3,4,1,2]
    # list_mod = [1,1,2,1,1,2]
    # missing_indices = findDeletedIndices(list_orig, list_mod)
    # print('missing indices = {}'.format(missing_indices))
    # print('\n')

    # #test different
    # print('*****Modified Elements Test******')
    # list_orig = [1,2,3,1,2,3,1,2,3,1,2]
    # list_mod = [1,2,2,1,2,3,1,2,3,1,3]
    # different_indices = findModifiedIndices(list_orig, list_mod)
    # print('different indices = {}'.format(different_indices))
    # print('\n')

    # #test addition
    # print('*****Modified Elements Test******')
    # list_orig = [1,2,3,1,2,3,1,2,3,1,2]
    # list_mod = [1,2,2,3,1,2,3,0,1,2,3,1,2]
    # added_indices = findAddedIndices(list_orig, list_mod)
    # print('added indices = {}'.format(added_indices))
    # print('\n')


    #extract radar data
    radar_data_predictions = radarDataExtractor("data/data-1.txt")
    # print('original data:', radar_data_predictions)
    radar_data_predictions = np.array([radar_data_predictions]).reshape(-1,2)
    #encode the data for a given step-size
    voxel_halfdelta = qim_quantize_twobits(radar_data_predictions)
    voxel_halfdelta_npy = np.array([voxel_halfdelta]).reshape(-1,2)
    # print('quant encoded shape', voxel_halfdelta_npy.shape, voxel_halfdelta_npy)
    
    qim_encoded_pointcloud = getPointCloud_from_quantizedValues(  np.copy(voxel_halfdelta_npy))
    print('encoded data', qim_encoded_pointcloud)

    pred_plusNoise = tamperRadarAddUniformNoise(0.0, qim_encoded_pointcloud)
    # print('noise added pc={}'.format(pred_plusNoise))
    
    #open the encoded data and tamper it by adding noise and attack vectors
    # added_indices, pred_plus_added = tamperRadarAddTracklets(pred_plusNoise)
    # added_indices, pred_plus_added = tamperRadarDeleteTracklets(pred_plusNoise)
    added_indices, pred_plus_added = tamperRadarModifyTracklets(pred_plusNoise)

    
    print('added indices:{}'.format(added_indices))
    print('modified data:{}'.format(pred_plus_added))
    #decode the tampered point cloud

    decoded_CB, decoded_quantized_values = qim_decode(np.copy(pred_plus_added))
    print('decoded codebook', decoded_CB)
    decoded_codebook = np.array([decoded_CB]).reshape(-1,NUMBITS)

    #calculate the BER
    encoded_cb = qim_dummy_encoded_pc(len(radar_data_predictions.reshape(-1,NUMBITS)))
    # print('encoded cb', encoded_cb)
    # uncomment below to test if the tamper index finder is working
    #encoded_cb[2] = [1,1]
    #encoded_cb[4] = [0,1]
    
    tampered_indices, b_errorRate = get_tamperedindices_twobits(decoded_codebook, encoded_cb)
    print('tampered indices', tampered_indices)

    #verify the accuracy
    modified_list = np.packbits(decoded_codebook, axis = 1)
    print('modified_list={}'.format(modified_list))
    groundtruth_list = np.packbits(encoded_cb, axis = 1)
    print('gt_list={}'.format(groundtruth_list))

    # added_indices_recovered = findAddedIndices(groundtruth_list, modified_list)
    added_indices_recovered = findModifiedIndices(groundtruth_list, modified_list)
    # added_indices_recovered = findDeletedIndices(groundtruth_list, modified_list)
    
  

    sorted_add_indices = np.sort(added_indices)
    sorted_recovered_indices = np.sort(added_indices_recovered)
    
    print('recovered indices:\t{}'.format(sorted_recovered_indices))
    print('added indices:\t\t{}'.format(sorted_add_indices))
    # sorted_add_indices[0] = 12
    # sorted_add_indices[2] = 12
    error_prediction =  np.where(sorted_recovered_indices != sorted_add_indices)
    if(len(error_prediction[0])):
        print('error n prediction, mismatch indices:{}'.format(error_prediction[0]))
    else:
        print('you got it buddy! finally..phew!!!!)')


