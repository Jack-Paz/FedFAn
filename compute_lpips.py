import lpips
import torch
from utils import length_check
import argparse as ap
import numpy as np
import cv2

def get_boundary_box_in_px(lips, res, padding=0):
	#padding is a percentage to scale min/max
	x, y = lips[:,0], lips[:,1]
	resx, resy = res
	#scaled by resolution
	points=[]
	scale_pad = (padding+100)/100
	minx = max(0, (min(x)*resx)/scale_pad)
	miny = max(0, (min(y)*resy)/scale_pad)
	maxx = min(resx, (max(x)*resx)*scale_pad)
	maxy = min(resy, (max(y)*resy)*scale_pad)
	points = np.round(np.asarray([minx, miny, maxx, maxy]))
	return points

def reconcile_boundary_boxes(box0, box1):
	return [min(box0[0], box1[0]), min(box0[1], box1[1]), max(box0[2], box1[2]), max(box0[3], box1[3])]

def norm_rgb(img):
	return ((img/255)*2)-1

def crop_image(img, minx, miny, maxx, maxy):
	return img[int(minx):int(maxx),int(miny):int(maxy)]

def display_image_w_boundary_box(img, minx, miny, maxx, maxy):
	cv2.rectangle(img, (int(minx), int(miny)), (int(maxx), int(maxy)), (255,0,0), 4)
	cv2.imshow('img', img)


def reshape_for_loss(img):
	return torch.FloatTensor(norm_rgb(img)).unsqueeze(0).transpose(1,3)

def lpips_loss(vid0, vid1):

	from extract_frames_from_video import extract_frames

	vid0_frames = extract_frames(vid0)
	vid1_frames = extract_frames(vid1)

	vid0_frames, vid1_frames = length_check(vid0_frames, vid1_frames)
	print(len(vid0_frames), len(vid1_frames))

	from apply_facial_landmarks import get_lms

	vid0_lms = get_lms(vid0)
	vid1_lms = get_lms(vid1)

	from utils import locations
	from utils import plot_landmarks
		
	# loss_fn = lpips.LPIPS(net='alex') # best forward scores
	loss_fn = lpips.LPIPS(net='vgg') # closer to "traditional" perceptual loss, when used for optimization
	#vgg works with smaller images

	losses = []

	for i in range(len(vid0_frames)):
		img0 = vid0_frames[i]
		img1 = vid1_frames[i]
		lms0 = vid0_lms[i]
		lms1 = vid1_lms[i]
		lips0 = lms0[locations['lips']]
		lips1 = lms1[locations['lips']]
		box0 = get_boundary_box_in_px(lips0, (img0.shape[0], img0.shape[1]))
		box1 = get_boundary_box_in_px(lips1, (img1.shape[0], img1.shape[1]))
		#what to do if these boxes are DIFFERENT?? make bigger
		cropbox = reconcile_boundary_boxes(box0, box1)
		img0_cut = reshape_for_loss(crop_image(img0, *cropbox))
		img1_cut = reshape_for_loss(crop_image(img1, *cropbox))
		display_image_w_boundary_box(img0, *cropbox)
		if cv2.waitKey(5) & 0xFF == 27:
			break
		d = loss_fn(img0_cut, img1_cut) #image should be RGB, IMPORTANT: normalized to [-1,1]
		losses.append(d.item())
		print('frame loss', d.item())
	mean_loss = np.sum(losses)/len(losses)
	print('mean loss', mean_loss)
	return mean_loss

if __name__=='__main__':
	parser = ap.ArgumentParser()
	parser.add_argument("--vid0", type=str, default='')
	parser.add_argument("--vid1", type=str, default='')
	args = parser.parse_args()
	vid0=args.vid0
	vid1=args.vid1
	lpips_loss(vid0, vid1)
