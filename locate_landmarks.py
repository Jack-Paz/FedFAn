import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import mediapipe as mp
import matplotlib.cm as cm

OBAMA_LM = '/home/paz/data/obama_landmark_test.pkl' 

TEST_OUT = '/home/paz/data/locate_landmarks.mp4'

obama_lm = pickle.load(open(OBAMA_LM, 'rb'))

import itertools

from utils import locations, locname_to_locno, locno_to_locname, loc_to_locname, locname_to_loc, loc_to_locno, locno_to_loc

del(locations['contours'])
del(locations['irises'])

print('total unique points:')
print(sum([len(x) for x in locations.values()]))


# print(loc_to_locno.keys())

# breakpoint()

colors = cm.rainbow(np.linspace(0.0, 1, len(locations)))
def make_location_video(lm):
	numlocs = lm.shape[1]

	def update_plot(i):
		# ax.set_title(f'location: {i}')
		graph._offsets3d = ([lm[0, i, 0]], [lm[0, i, 1]], [lm[0, i, 2]])
		return graph

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	elev, azim, roll = -90, -90, 0
	ax.view_init(elev, azim, roll)
	ax.axes.set_xlim3d(left=0, right=1) 
	ax.axes.set_ylim3d(bottom=0, top=1) 
	ax.axes.set_zlim3d(bottom=0, top=1)
	ax.axes.set_xticklabels('')
	ax.axes.set_yticklabels('')
	ax.axes.set_zticklabels('')
	frame_lms = lm[0, :, :]

	for location in locations:
		loc_list = locname_to_loc[location]
		c = colors[locname_to_locno[location]]
		graph = ax.scatter(lm[0, loc_list, 0], lm[0, loc_list, 1], lm[0, loc_list, 2], color=c)	
		# for i in locations[location]:
		# 	ax.text(lm[0, i, 0], lm[0, i, 1], lm[0, i, 2], location, size='x-small')

		location = loc_to_locname[i]
		c = colors[locname_to_locno[location]]

	plt.show()
	ani=None
	return ani

ani = make_location_video(obama_lm)

# writervideo = animation.FFMpegWriter(fps=5) 
# ani.save(TEST_OUT, writer=writervideo)


