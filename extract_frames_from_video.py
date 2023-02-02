import cv2
import argparse as ap


def extract_frames(input_video, output_folder=''):
	video = cv2.VideoCapture(input_video)
	frames = []
	nframes = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	for i in range(nframes):
		video.set(cv2.CAP_PROP_POS_FRAMES, i)
		ret, frame = video.read()
		# cv2.imshow('frame', frame); cv2.waitKey(0)
		frames.append(frame)
		if output_folder:
			cv2.imwrite(f'{output_folder}{i}.jpg', frame)
	return frames

if __name__=='__main__':
	parser = ap.ArgumentParser()
	parser.add_argument("--input_video", type=str, default='')
	parser.add_argument("--output_folder", type=str, default='')
	args = parser.parse_args()

	input_video = args.input_video
	output_folder = args.output_folder

	extract_frames(input_video, output_folder)
