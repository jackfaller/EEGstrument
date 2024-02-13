
#import UnicornPy
import neurolThesis
from neurolThesis import streams
from neurolThesis.connect_device import get_lsl_EEG_inlets
from neurolThesis.BCI import generic_BCI, automl_BCI
from neurolThesis import BCI_tools
from neurolThesis.models import classification_tools
from sys import exit
from pylsl import StreamInlet, resolve_stream
import numpy as np
import threading
import soundcard as sc
import wave
import time

#import UnicornPy
import neurolThesis
from neurolThesis import streams
from neurolThesis.connect_device import get_lsl_EEG_inlets
from neurolThesis.BCI import generic_BCI, automl_BCI
from neurolThesis import BCI_tools
from neurolThesis.models import classification_tools
from sys import exit
from pylsl import StreamInlet, resolve_stream
import numpy as np

def clf(clf_input, clb_info):
    #print("clf input" , clf_input)
    clf_input = clf_input[0:2,:clb_info.shape[0]]
    clb_info = clb_info[0:1,:clb_info.shape[0]]
    #print('clb_info.shape[0]', clb_info.shape[0])
    #print("clf input" , clf_input)
    #print('clb_info', clb_info)
    
    # Reshaping clb_info to match the shape of clf_input
    clb_info_reshaped = clb_info.reshape(clf_input.shape)

    # Element-wise comparison and summing
    greater_count = np.sum(clf_input > clb_info_reshaped)

    # Dividing the count by two and ensuring the result is between 0 and 7
    result = np.clip(greater_count // 2, 0, 7)

 
    return result


def clf2(clf_input, clb_info):
    print("clf input" , clf_input)
    print('clb_info', clb_info)
    clf_input = clf_input[0:2,:clb_info.shape[0]]
    #clb_info = clb_info[0:1,:clb_info.shape[0]]
    #print('clb_info.shape[0]', clb_info.shape[0])
    print("clf input" , clf_input)
    #print('clb_info', clb_info)
    
    # Extracting the 8th elements from clf_input
    clf_8th_elements = clf_input[:, 7]
    print('8th element',clf_8th_elements)

    # Reshaping clb_info for comparison
    clb_info_reshaped = clb_info.reshape(clf_input.shape)
    #clb_info_reshaped = clb_info[:,7]

    # Comparing the 8th elements of clf_input with each element of clb_info
    comparison_results = np.sum(clb_info < clf_8th_elements[:, np.newaxis, np.newaxis], axis=(1, 2))

    # Dividing the total count by two and ensuring the result is between 0 and 7
    result = np.clip(np.sum(comparison_results) // 2, 0, 7)


 
    return result


def generate_letter(note):
    print(note)


streams1 = resolve_stream("name='Unicorn'")
inlet = StreamInlet(streams1[0])
stream = streams.lsl_stream(inlet, buffer_length=1024)

clb = lambda stream:  BCI_tools.band_power_calibrator(stream, ['EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 'EEG 5', 'EEG 6', 'EEG 7', 'EEG 8'], 'unicorn', 
                                                        bands=['alpha_low','alpha_high'],
                                                        percentile=5, recording_length=10, epoch_len=1, inter_window_interval=0.25)


gen_tfrm = lambda buffer, clb_info: BCI_tools.band_power_transformer(buffer, 250, bands=['alpha_low','alpha_high'])
BCI = generic_BCI(clf2, transformer=gen_tfrm, action=generate_letter, calibrator=clb)

BCI.calibrate(stream)
BCI.run(stream)

#'EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 'EEG 5', 'EEG 6', 'EEG 7',