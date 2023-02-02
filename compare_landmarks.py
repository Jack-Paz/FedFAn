import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

OBAMA_LM = '/home/paz/data/obama_landmark_test.pkl' 
LRC_LM = '/home/paz/data/lrc_landmark_test.pkl' 
TEST_OUT = '/home/paz/data/animation.mp4'

obama_lm = pickle.load(open(OBAMA_LM, 'rb'))
lrc_lm = pickle.load(open(LRC_LM, 'rb'))

#shape:  (n_frames, n_landmarks, 3(xyz))

if len(obama_lm) != len(lrc_lm):
	print('warning length mismatch! trunkating...')
	min_len = min(len(obama_lm), len(lrc_lm))
	obama_lm = obama_lm[:min_len]
	lrc_lm = lrc_lm[:min_len]


# assert len(obama_lm)==len(lrc_lm), 'landmark files n frames mismatch!'
assert len(obama_lm[0])==len(lrc_lm[0]), 'landmark files n landmarks mismatch!'

print(obama_lm.shape)
print(lrc_lm.shape)

diff_lm = obama_lm - lrc_lm


#make video for landmarks

def make_video(lm):
	numframes = lm.shape[0]

	def update_plot(i):
		ax.set_title(f'frame: {i}')
		graph._offsets3d = (lm[i, :, 0], lm[i, :, 1], lm[i, :, 2])
		return graph

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	elev, azim, roll = -90, -90, 0
	ax.view_init(elev, azim, roll)
	ax.axes.set_xlim3d(left=-0.2, right=0.3) 
	ax.axes.set_ylim3d(bottom=-0.2, top=0.3) 
	ax.axes.set_zlim3d(bottom=-0.2, top=0.3) 
	graph = ax.scatter(lm[0,:,1], lm[0,:,1], lm[0,:,2])
	# dir(graph)
	# breakpoint()
	for i in range(numframes):
		ani = animation.FuncAnimation(fig, update_plot, frames=range(numframes))
		plt.show()
	return ani

ani = make_video(diff_lm)

writervideo = animation.FFMpegWriter(fps=5) 
ani.save(TEST_OUT, writer=writervideo)


# plt.plot(diff_lm[:,0,0])
# plt.plot(diff_lm[:,0,1])
# plt.plot(diff_lm[:,0,2])
# plt.show()

#