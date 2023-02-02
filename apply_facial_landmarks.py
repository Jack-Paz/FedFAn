#taken from the docs and ammended https://google.github.io/mediapipe/solutions/face_mesh#python-solution-api

import mediapipe as mp
import cv2
import pickle
import numpy as np
import argparse as ap

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# input_video='/home/paz/data/00004_obama_a.mp4'
# video_out='/home/paz/data/obama_landmark_test.mp4'
# landmarks_out='/home/paz/data/obama_landmark_test.pkl'

# input_video='/home/paz/data/00004.mp4'
# video_out='/home/paz/data/test.mp4'
# landmarks_out='/home/paz/data/test.pkl'


def convert_lm_frame_to_array(results):
	'''converts results to an np array of shape (n_landmarks, 3(xyz)). 
	only works for one face'''
	out_list = []
	landmark_list = list(results.multi_face_landmarks[0].landmark)
	for landmark in landmark_list:
		out_list.append([landmark.x, landmark.y, landmark.z])
	return np.asarray(out_list)

def get_lms(input_video, save_vid=False, save_landmarks=False, show_vid=False):
  # For webcam input:
  video_out = f"{input_video.split('.')[0]}_withlms.mp4"
  landmarks_out = f"{input_video.split('.')[0]}_lms.pkl"
  drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
  cap = cv2.VideoCapture(input_video)
  width = int(cap.get(3))
  height = int(cap.get(4))
  fps = int(cap.get(cv2.CAP_PROP_FPS))
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')

  if save_vid:
    out = cv2.VideoWriter(video_out, fourcc, fps, (width,height))

  frame_landmarks = []

  with mp_face_mesh.FaceMesh(
      max_num_faces=1,
      refine_landmarks=True,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        break
      
      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = face_mesh.process(image)
      frame_landmarks.append(convert_lm_frame_to_array(results))
      # # Draw the face mesh annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_TESSELATION,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_tesselation_style())
          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_CONTOURS,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_contours_style())
          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_IRISES,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_iris_connections_style())
      # # Flip the image horizontally for a selfie-view display.
      # cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
      #save new image with landmarks 
      if save_vid:
        out.write(image)
      if show_vid:  
        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break

  if save_landmarks:
    frame_landmarks = np.asarray(frame_landmarks)
    pickle.dump(frame_landmarks, open(landmarks_out, 'wb'))

  if save_vid:
    out.release()

  cap.release()
  return frame_landmarks

if __name__=='__main__':
  parser = ap.ArgumentParser()
  parser.add_argument("--input_video", type=str, default='')
  parser.add_argument("--save_vid", action='store_true')
  parser.add_argument("--save_landmarks", action='store_true')
  args = parser.parse_args()

  input_video=args.input_video
  save_vid=args.save_vid
  save_landmarks=args.save_landmarks

  frame_landmarks = compute_landmark_results(input_video, save_vid, save_landmarks)