import matplotlib.pyplot as plt
import numpy as np
import argparse as ap
import mediapipe as mp
import cv2
import os
import re

parser = ap.ArgumentParser()
parser.add_argument('input_folder', type=str, help='experiment "workspace"')
args = parser.parse_args()
input_folder = args.input_folder

def main(input_folder):
	return None

fourcc = cv2.VideoWriter_fourcc(*'mp4v')


image_folder = os.path.join(input_folder, 'validation')
width, height = cv2.imread(os.path.join(image_folder, 'ngp_ep0001_0001_rgb.png')).shape[:2]
fps = 12
#ngp_ep0001_0001_rgb.png
outfolder = os.path.join(input_folder, 'valid_videos')
if not os.path.isdir(outfolder):
	os.mkdir(outfolder)
out_vids = [cv2.VideoWriter(f'{outfolder}/1.mp4', fourcc, fps, (width,height))]
for x in sorted(os.listdir(image_folder)):
	m = re.match('ngp_ep(\d+)_(\d+)_rgb\.png', x)
	if m:
		
		group = int(m.group(1))
		# idx = int(m.group(2))
		if len(out_vids)<group:
			out_vids[group-2].release()
			out_vids.append(cv2.VideoWriter(f'{outfolder}/{group}.mp4', fourcc, fps, (width,height)))
		vid = out_vids[group-1]
		image_path = os.path.join(image_folder, x)
		image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
		vid.write(image)









if __name__=='__main__':
	x = main(input_folder)
	print(x)