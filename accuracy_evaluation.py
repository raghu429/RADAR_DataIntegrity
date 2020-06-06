# -*- coding: utf-8 -*-
import numpy as np

# #** This piece of code contants methods to evaluate the 2D QIM embedding for the given Udacity data-set. We can further split this file into three different files if needed (most of the previously developed code could be re-used)
# First - read the data file and generate a separate binary file with just the radar data
# Add noise to the data if required (uniform or Gaussian with variable delta)
# simulate the attack vectors, like add, delete or modify the random line items in the above generated file
# get the detections out of the modified files and report the false alarms, error rate and accuracy (if the algorithm is able to detect the location of the modified data)
# **#

#these three fucntions check for the midding indices, added indices and modified indices assuming the input is a list of repeating pattens

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
    pass
    return added_indices


if __name__ == '__main__':
    #test missing
    print('******Deleted Elements Test******')
    list_orig = [1,2,3,1,2,3,1,2,3,1,2]
    list_mod = [1,1,2,1,1,2]
    missing_indices = findDeletedIndices(list_orig, list_mod)
    print('missing indices = {}'.format(missing_indices))
    print('\n')

    #test different
    print('*****Modified Elements Test******')
    list_orig = [1,2,3,1,2,3,1,2,3,1,2]
    list_mod = [1,2,2,1,2,3,1,2,3,1,3]
    different_indices = findModifiedIndices(list_orig, list_mod)
    print('different indices = {}'.format(different_indices))
    print('\n')

    #test addition
    print('*****Modified Elements Test******')
    list_orig = [1,2,3,1,2,3,1,2,3,1,2]
    list_mod = [1,5,2,3,1,2,3,0,1,2,3,1,2]
    added_indices = findAddedIndices(list_orig, list_mod)
    print('added indices = {}'.format(added_indices))
    print('\n')
