import mediapipe as mp
import itertools
import numpy as np
import matplotlib.pyplot as plt

contours = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_CONTOURS)))
face_oval = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_FACE_OVAL)))
irises = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_IRISES)))
left_eye = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_LEFT_EYE)))
left_eyebrow = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_LEFT_EYEBROW)))
left_iris = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_LEFT_IRIS)))
lips = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_LIPS)))
right_eye = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_RIGHT_EYE)))
right_eyebrow = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_RIGHT_EYEBROW)))
right_iris = list(set(itertools.chain(*mp.solutions.face_mesh.FACEMESH_RIGHT_IRIS)))

locations = {
			'contours': contours, 
	         'face_oval': face_oval, 
	         'irises': irises, 
	         'left_eye': left_eye, 
	         'left_eyebrow': left_eyebrow, 
	         'left_iris':left_iris,
			 'lips': lips, 
			 'right_eye': right_eye, 
			 'right_eyebrow': right_eyebrow, 
			 'right_iris': right_iris}

named_locs = []	
for x in locations.values():
	named_locs.extend(x)
all_locs = np.arange(478)
other_locs = list(set(all_locs) - set(named_locs))

locations['other'] = other_locs

#dict of location name (eg. 'lips' to a new location number eg. 7 for lips)
locname_to_locno = {locname:i  for i, locname in enumerate(locations.keys())}
locno_to_locname = {i: locname  for i, locname in enumerate(locations.keys())}
#dict of loc (actual landmark number) to the name of the location category (eg 'lips')
loc_to_locname = {}
locname_to_loc = {}
#dict of loc (landmark) to location number defined above in locname_to_locno
loc_to_locno = {}
locno_to_loc = {}

for i, loc in enumerate(locations):
	locname_to_loc[loc] = []
	locno_to_loc[loc] = i
	for x in locations[loc]:
		loc_to_locname[x] = loc
		locname_to_loc[loc].append(x)
		loc_to_locno[x] = i
		locno_to_loc[i] = x

def length_check(array1, array2):
	if len(array1) != len(array2):
		print('warning length mismatch! trunkating...')
		min_len = min(len(array1), len(array2))
		array1 = array1[:min_len]
		array2 = array2[:min_len]
	return array1, array2
	
def plot_landmarks(frame_lm):
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
	graph = ax.scatter(frame_lm[:,0],frame_lm[:,1],frame_lm[:,2])
	plt.show()
	# return graph
