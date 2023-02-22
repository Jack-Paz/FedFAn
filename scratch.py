import re
import os
from pathlib import Path

def get_lrs_pathlists(input_folder, combine=True):
    '''
    input is lrs folder (train or valid) with subfolders for speakers 
    '''
    input_folder = Path(input_folder)
    out_dict = {}
    for speaker in os.listdir(input_folder):
        speakerfolder = f'{input_folder}/{speaker}'
        out_dict[speaker] = {}
        vidnames = [x for x in os.listdir(speakerfolder) if os.path.isdir(f'{speakerfolder}/{x}')] 
        for vid in sorted(vidnames):
            out_dict[speaker][vid] = {}
            vidpath = f'{speakerfolder}/{vid}'
            imglist = []
            lmlist = []
            trackparamslist = []
            transformslist = []
            for y in os.listdir(vidpath):
                ypath = f'{vidpath}/{y}'
                if re.match('.+\.jpg', ypath):
                    imglist.append(ypath)
                elif re.match('.+\.lms', ypath):
                    lmlist.append(ypath)
                elif re.match('.+track_params.pt', ypath):
                    trackparamslist.append(ypath)
                elif re.match('.+\.json', ypath):
                    transformslist.append(ypath)
            out_dict[speaker][vid]['img']= imglist
            out_dict[speaker][vid]['lm'] = lmlist
            out_dict[speaker][vid]['trackparams'] = trackparamslist
            out_dict[speaker][vid]['transforms'] = transformslist
            out_dict[speaker][vid]['vid'] = f'{vidpath}.mp4'
            out_dict[speaker][vid]['wav'] = f'{vidpath}.wav'
            out_dict[speaker][vid]['feature'] = f'{vidpath}_eo.npy'
    return out_dict

if __name__=='__main__':
	import argparse as ap
	parser = ap.ArgumentParser()
	parser.add_argument('input_folder', type=str, default='')
	args = parser.parse_args()
	input_folder = args.input_folder 
	out_dict = get_lrs_pathlists(input_folder)