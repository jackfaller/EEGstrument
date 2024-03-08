#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:03:26 2024

@author: jackfaller
"""

'''
Attempting to make a classifier for single, double, and triple bandpowers.
'''

#%%

clf_inputSingle = [8, 2.17385452e+00, 2.17385452e+00, 2.17385452e+00,
             2.17385452e+00, 2.17385452e+00, 2.17385452e+00, 2.17385452e+00,
             5.31729604e-09, 5.01874084e-09, 9.04829068e-09, 1.40117325e-05,
             5.59281111e-06, 1.04068849e-05, 3.86462961e-08, 6.35869215e-03,
             3.86462961e-12]
clb_infoSingle = [[78774.28691089, 78766.62744442, 78933.36418714, 78909.50054131,
             78830.74243173, 78941.38638077, 78921.38428819],
            [79593.78941484, 79586.96080892, 79753.44868787, 79732.00322643,
             79652.03087137, 79764.28553814, 79741.07566031],
            [80291.68471249, 80283.96658219, 80451.54908696, 80428.45866307,
             80348.46880208, 80460.18480258, 80439.75835059],
            [81173.96311654, 81165.53736003, 81335.08316257, 81312.03875944,
             81230.75393521, 81345.86922396, 81323.2366068],
            [82046.43818259, 82039.61277553, 82210.81837338, 82186.19785984,
             82107.04568381, 82219.08990806, 82198.30314673],
            [82972.55774622, 82962.50605028, 83136.94038783, 83111.78353999,
             83029.30807512, 83144.25665415, 83121.54864829],
            [83815.03871363, 83803.87492147, 83979.02863299, 83955.77873614,
             83870.49879267, 83988.20255848, 83964.66590897],
            [84619.61541992, 84611.35058289, 84786.90367554, 84764.28682903,
             84679.52747915, 84796.55118693, 84772.20706021]]



clf_inputDouble = [
    [1.31170585e+02, 1.31363302e+02, 1.31215342e+02, 1.31299338e+02,
     1.31115441e+02, 1.31260147e+02, 1.31376216e+02, 1.31421748e+02,
     3.36657617e-09, 2.90843035e-09, 7.70391797e-09, 4.32588669e-05,
     5.32831998e-05, 2.02826370e-05, 5.59791950e-09, 1.13370211e-04,
     5.59791950e-13],
    [2.51590099e+01, 2.51254426e+01, 2.51979812e+01, 2.51410314e+01,
     2.50794019e+01, 2.51582487e+01, 2.51666289e+01, 2.52175878e+01,
     4.52757780e-09, 2.11114041e-09, 6.70434345e-09, 1.22367831e-05,
     1.61871465e-05, 7.45394087e-06, 2.07955224e-09, 4.03800150e-05,
     2.07955224e-13]
]

clb_infoDouble = [
    [[78.44566669, 78.43698851, 79.08484453, 78.87467107, 78.90566531,
      79.2433042, 79.28648597],
     [18.56754709, 18.58783433, 18.72558801, 18.68244485, 18.67094795,
      18.75310664, 18.77579591]],
    
    [[119.00556827, 119.01538764, 119.57788722, 119.40366793, 119.45639858,
      119.81615291, 119.83649455],
     [28.48160808, 28.47092696, 28.592664, 28.58367893, 28.54905921,
      28.6525782, 28.63551905]],
    
    [[135.33941971, 135.41903245, 136.0970241, 135.96939883, 135.91066871,
      136.390767, 136.36024275],
     [33.13581118, 33.16088987, 33.3228004, 33.28349, 33.28895001,
      33.3838019, 33.3788298]],
    
    [[148.30280051, 148.34186603, 149.08203743, 148.85802894, 148.87230572,
      149.27332136, 149.32165149],
     [36.7042885, 36.69440097, 36.90532974, 36.8478059, 36.83430298,
      36.95327766, 36.95589617]],
    
    [[154.61792407, 154.55459838, 155.45131652, 155.20615784, 155.15479718,
      155.68615421, 155.65652636],
     [42.42921408, 42.40677108, 42.63590419, 42.57921924, 42.57774285,
      42.66556755, 42.67758164]],
    
    [[186.86623102, 186.90733929, 187.76169391, 187.6204003, 187.44892201,
      188.04617135, 188.05918632],
     [47.89727915, 47.86912388, 48.0628376, 48.04573544, 47.97445799,
      48.1419366, 48.15256079]],
    
    [[212.79962012, 212.74882257, 213.8280656, 213.46353415, 213.44604675,
      214.10252704, 214.04748982],
     [57.10050859, 57.10126998, 57.28245879, 57.20663373, 57.18758409,
      57.27092065, 57.30123743]],
    
    [[348.42407791, 348.29509617, 349.27387037, 349.25723353, 348.6637408,
      349.19900183, 349.12562611],
     [136.55653955, 136.43366802, 136.89987683, 136.89168938, 136.6021621,
      136.87395756, 136.7886749]]
]


#%%

import numpy as np



def clfSingle(clf_input, clb_info):
    # Convert inputs to numpy arrays
    clf_input_np = np.array(clf_input[:8])  # Only consider the first 8 elements
    clb_info_np = np.array(clb_info)[:, :7]  # Consider only the 7 percentiles
    #print('clf_input_np:', clf_input_np)
    #print('\n clb_info_np:',clb_info_np)
    # Compare clf_input_np with each percentile in clb_info_np and count how many percentiles it exceeds
    bin_indices = np.sum(clf_input_np[:, np.newaxis] > clb_info_np, axis=0) 
    #print('\nclf_input_np[:, np.newaxis] :', clf_input_np[:, np.newaxis] )
    #print('\nclb_info_np', clb_info_np)

    
    note = round(np.average(bin_indices))
    
    return note


def clfDouble(clf_input, clb_info):
    
    #convert into numpy arrays
    clf1 = np.array(clf_input[0][:8])
    clf2 = np.array(clf_input[1][:8])
    
    clb1 = np.array(clb_info)[:,0,:7]
    clb2 = np.array(clb_info)[:,1,:7]
    
    bin_indices1 = np.sum(clf1[:, np.newaxis] > clb1, axis=0) 
    bin_indices2 = np.sum(clf2[:, np.newaxis] > clb2, axis=0)
    
    note = round((np.average(bin_indices1) + np.average(bin_indices2))/2)
    
    return note


def clfTriple(clf_input, clb_info):
    
    #convert into numpy arrays
    clf1 = np.array(clf_input[0][:8])
    clf2 = np.array(clf_input[1][:8])
    clf3 = np.array(clf_input[2][:8])
    
    clb1 = np.array(clb_info)[:,0,:7]
    clb2 = np.array(clb_info)[:,1,:7]
    clb3 = np.array(clb_info)[:,2,:7]
    
    bin_indices1 = np.sum(clf1[:, np.newaxis] > clb1, axis=0) 
    bin_indices2 = np.sum(clf2[:, np.newaxis] > clb2, axis=0)
    bin_indices3 = np.sum(clf3[:, np.newaxis] > clb3, axis=0)
    
    note = round((np.average(bin_indices1) + np.average(bin_indices2) + np.average(bin_indices3) )/3)
    
    return note


def clfElectrode(clf_input, clb_info, electrode):
    
    n = electrode - 1
    # Convert inputs to numpy arrays
    clf_input_np = np.array(clf_input[n])  # Only consider the chosen electrode 
    clb_info_np = np.array(clb_info)[:7, n]  # Consider only the 7 percentiles
    
    print('clf_input_np:', clf_input_np)
    print('\n clb_info_np:',clb_info_np)
    

    bin_indices = np.sum(clf_input_np[np.newaxis] > clb_info_np, axis=0) 

    note = round(np.average(bin_indices))
    
    return note



#%%

'''
Lets define multiple different ways to generate a note
    1. A simple note = note
    2. Similar to alphalight, the higher a note the more it pushes the scales
    3. Possibly average notes over 1 second
'''

def generateNote(note):
    if all(position == 'normal' for position in box_positions.values()):
        letters = list(boxes.keys())
        selected_letter = letters[note]
        raise_box(selected_letter)
    


#%%

print(clfSingle(clf_inputSingle, clb_infoSingle), '\n')

print(clfDouble(clf_inputDouble, clb_infoDouble), '\n')

print(clfElectrode(clf_inputSingle, clb_infoSingle, 1))







