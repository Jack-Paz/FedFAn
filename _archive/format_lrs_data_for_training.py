import os
import argparse as ap
from pathlib import Path
import re
import shutil
import wave
import cv2
import torch



def setup_output_folder(output_folder):
	os.mkdir(output_folder)
	os.mkdir(output_folder/'gt_imgs/')
	os.mkdir(output_folder/'ori_imgs/')
	os.mkdir(output_folder/'parsing/')
	os.mkdir(output_folder/'torso_imgs/')

def combine_wavs(wavlist, outfile):
	data= []
	for infile in wavlist:
	    w = wave.open(infile, 'rb')
	    data.append( [w.getparams(), w.readframes(w.getnframes())] )
	    w.close()
	    
	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])
	for i in range(len(data)):
	    output.writeframes(data[i][1])
	output.close()

def combine_vids(vidlist, outfile):
	# Create a new video
	tempvid = cv2.VideoCapture(vidlist[0])
	fps = tempvid.get(cv2.CAP_PROP_FPS)
	width = tempvid.get(cv2.CAP_PROP_FRAME_WIDTH) 
	height = tempvid.get(cv2.CAP_PROP_FRAME_HEIGHT)
	tempvid.release()

	video = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*"MPEG"), fps, (width, height))

	# Write all the frames sequentially to the new video
	for v in vidlist:
	    curr_v = cv2.VideoCapture(v)
	    while curr_v.isOpened():
	        r, frame = curr_v.read()    # Get return value and curr frame of curr video
	        if not r:
	            break
	        video.write(frame)          # Write the frame

	video.release()                     # Save the video

def combine_track_params(trackparamslist, outfile):
	newdict = {'id': [], 'exp': [], 'euler': [], 'trans': [], 'focal': []}

def combine_transforms(transformslist):
	pass

def combine_features(featurelist):
	pass

def main(input_folder, combine=True):
	'''input folder format: 
	0af00UcTOSc/ 
	 -> 50001/, (...) 5000N/
	 -> 50001.mp4 
	 -> 50001.txt
	 -> 50001.wav
	 -> 50001_eo.npy
	output_folder format:
	 -> gt_imgs/
	 -> ori_imgs/
	 -> parsing/
	 -> torso_imgs/
	 -> aud.wav
	 -> aud_eo.npy
	 -> obama.mp4
	 -> track_params.pt
	 -> transforms_train.json
	 -> transofmrs_valid.json
	'''
	input_folder = Path(input_folder)
	output_folder = input_folder.with_name(f'{input_folder.name}_processed')
	setup_output_folder(output_folder)
	# imglist = []
	# lmlist = []
	vidlist = []
	wavlist = []
	featurelist = []
	trackparamslist = []
	transformslist = []
	for x in sorted(os.listdir(input_folder)):
		xpath = f'{input_folder}/{x}'
		if os.path.isdir(xpath):
			for y in os.listdir(xpath):
				ypath = f'{input_folder}/{x}/{y}'
				if re.match('.+\.jpg', ypath):
					# imglist.append(ypath)
					shutil.copy(ypath, f'{output_folder}/{x}_{y}')
				elif re.match('.+\.lms', fpath):
					# lmlist.append(ypath)
					shutil.copy(ypath, f'{output_folder}/{x}_{y}')		
				elif re.match('track_params.pt', fpath):
					trackparamslist.append(fpath)
				elif re.match('.+\.json', fpath):
					transformslist.append(fpath)
		else:
			if re.match('.+\.mp4', xpath):
				vidlist.append(xpath)
			elif re.match('.+\.wav', xpath):
				wavlist.append(xpath)
			elif re.match('.+_eo.npy', xpath):
				featurelist.append(xpath)
	combine_wavs(wavlist, f'{output_folder}/{input_folder.name}.wav')
	combine_vids(vidlist, f'{output_folder}/{input_folder.name}.mp4')
	combine_features(featurelist, f'{output_folder}/{input_folder.name}_eo.npy')
	combine_track_params(trackparamslist, f'{output_folder}/{input_folder.name}_track_params.pt')
	combine_transforms(transformslist, f'{output_folder}/{input_folder.name}.json')




if __name__=='__main__':
	parser = ap.ArgumentParser()
	parser.add_argument('input_folder', type=str, help='one speakers fully formatted folder')
	args = parser.parse_args()
	input_folder = args.input_folder
	main(input_folder)