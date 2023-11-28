#import UnicornPy
import neurolThesis
from neurolThesis import streams
from neurolThesis.connect_device import get_lsl_EEG_inlets
from neurolThesis.BCI import generic_BCI, automl_BCI
from neurolThesis import BCI_tools
from neurolThesis.models import classification_tools
from sys import exit
from pylsl import StreamInlet, resolve_stream

def clf(clf_input, clb_info):
    print("clf input" , clf_input)
    clf_input = clf_input[0:1,:clb_info.shape[0]]
    clb_info = clb_info[0:1,:clb_info.shape[0]]
    print('clb_info.shape[0]', clb_info.shape[0])
    print("clf input" , clf_input)
    print('cln_info', clb_info)
    note = 0
    for i in range(clb_info.shape[0]):
        if(clf_input[i] > clb_info[i]):
            note += 1
 
    return note

def generate_letter(note):
    print(note)
    # if all(position == 'normal' for position in box_positions.values()):
    #     letters = list(boxes.keys())
    #     selected_letter = letters[note]
    #     raise_box(selected_letter)
    #root.after(2000, generate_letter)

streams1 = resolve_stream("name='Unicorn'")
inlet = StreamInlet(streams1[0])
stream = streams.lsl_stream(inlet, buffer_length=1024)

clb = lambda stream:  BCI_tools.band_power_calibrator(stream, ['EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 
                                                               'EEG 5', 'EEG 6', 'EEG 7', 'EEG 8'], 'unicorn', 
                                                        bands=['alpha_low','alpha_high'],
                                                        percentile=5, recording_length=1, epoch_len=1, inter_window_interval=0.25)


gen_tfrm = lambda buffer, clb_info: BCI_tools.band_power_transformer(buffer, 250, bands=['alpha_low','alpha_high'])



BCI = generic_BCI(clf, transformer=gen_tfrm, action=generate_letter, calibrator=clb)
BCI.calibrate(stream)
BCI.run(stream)
