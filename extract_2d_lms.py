#edited function from process.py in rad-nerf

import torch
import cv2
import numpy as np
import glob
import os 
import tqdm
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument("--img_dir", type=str, default='')
args = parser.parse_args()


# ori_imgs_dir = '/home/paz/data/lrs3/trackingtest/1PNX6MSdVsk/00001'

ori_imgs_dir = args.img_dir

def extract_landmarks(ori_imgs_dir):

    print(f'[INFO] ===== extract face landmarks from {ori_imgs_dir} =====')

    import face_alignment
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False)
    image_paths = glob.glob(os.path.join(ori_imgs_dir, '*.jpg'))
    for image_path in tqdm.tqdm(image_paths):
        input = cv2.imread(image_path, cv2.IMREAD_UNCHANGED) # [H, W, 3]
        input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
        preds = fa.get_landmarks(input)
        if len(preds) > 0:
            lands = preds[0].reshape(-1, 2)[:,:2]
            np.savetxt(image_path.replace('jpg', 'lms'), lands, '%f')
    del fa
    print(f'[INFO] ===== extracted face landmarks =====')

if __name__=='__main__':
    extract_landmarks(ori_imgs_dir)

# def get_pose(base_dir, video_path):
#     params_dict = torch.load(os.path.join(base_dir, 'track_params.pt'))

#     focal_len = params_dict['focal']
#     euler_angle = params_dict['euler']
#     trans = params_dict['trans'] / 10.0
#     valid_num = euler_angle.shape[0]

#     def euler2rot(euler_angle):
#         batch_size = euler_angle.shape[0]
#         theta = euler_angle[:, 0].reshape(-1, 1, 1)
#         phi = euler_angle[:, 1].reshape(-1, 1, 1)
#         psi = euler_angle[:, 2].reshape(-1, 1, 1)
#         one = torch.ones((batch_size, 1, 1), dtype=torch.float32, device=euler_angle.device)
#         zero = torch.zeros((batch_size, 1, 1), dtype=torch.float32, device=euler_angle.device)
#         rot_x = torch.cat((
#             torch.cat((one, zero, zero), 1),
#             torch.cat((zero, theta.cos(), theta.sin()), 1),
#             torch.cat((zero, -theta.sin(), theta.cos()), 1),
#         ), 2)
#         rot_y = torch.cat((
#             torch.cat((phi.cos(), zero, -phi.sin()), 1),
#             torch.cat((zero, one, zero), 1),
#             torch.cat((phi.sin(), zero, phi.cos()), 1),
#         ), 2)
#         rot_z = torch.cat((
#             torch.cat((psi.cos(), -psi.sin(), zero), 1),
#             torch.cat((psi.sin(), psi.cos(), zero), 1),
#             torch.cat((zero, zero, one), 1)
#         ), 2)
#         return torch.bmm(rot_x, torch.bmm(rot_y, rot_z))




# def save_transforms(base_dir, ori_imgs_dir):
#     print(f'[INFO] ===== save transforms =====')


#     image_paths = glob.glob(os.path.join(ori_imgs_dir, '*.jpg'))
    
#     # read one image to get H/W
#     tmp_image = cv2.imread(image_paths[0], cv2.IMREAD_UNCHANGED) # [H, W, 3]
#     h, w = tmp_image.shape[:2]

#     params_dict = torch.load(os.path.join(base_dir, 'track_params.pt'))
#     focal_len = params_dict['focal']
#     euler_angle = params_dict['euler']
#     trans = params_dict['trans'] / 10.0
#     valid_num = euler_angle.shape[0]

#     def euler2rot(euler_angle):
#         batch_size = euler_angle.shape[0]
#         theta = euler_angle[:, 0].reshape(-1, 1, 1)
#         phi = euler_angle[:, 1].reshape(-1, 1, 1)
#         psi = euler_angle[:, 2].reshape(-1, 1, 1)
#         one = torch.ones((batch_size, 1, 1), dtype=torch.float32, device=euler_angle.device)
#         zero = torch.zeros((batch_size, 1, 1), dtype=torch.float32, device=euler_angle.device)
#         rot_x = torch.cat((
#             torch.cat((one, zero, zero), 1),
#             torch.cat((zero, theta.cos(), theta.sin()), 1),
#             torch.cat((zero, -theta.sin(), theta.cos()), 1),
#         ), 2)
#         rot_y = torch.cat((
#             torch.cat((phi.cos(), zero, -phi.sin()), 1),
#             torch.cat((zero, one, zero), 1),
#             torch.cat((phi.sin(), zero, phi.cos()), 1),
#         ), 2)
#         rot_z = torch.cat((
#             torch.cat((psi.cos(), -psi.sin(), zero), 1),
#             torch.cat((psi.sin(), psi.cos(), zero), 1),
#             torch.cat((zero, zero, one), 1)
#         ), 2)
#         return torch.bmm(rot_x, torch.bmm(rot_y, rot_z))


#     # train_val_split = int(valid_num*0.5)
#     # train_val_split = valid_num - 25 * 20 # take the last 20s as valid set.
#     train_val_split = int(valid_num * 10 / 11)

#     train_ids = torch.arange(0, train_val_split)
#     val_ids = torch.arange(train_val_split, valid_num)

#     rot = euler2rot(euler_angle)
#     rot_inv = rot.permute(0, 2, 1)
#     trans_inv = -torch.bmm(rot_inv, trans.unsqueeze(2))

#     pose = torch.eye(4, dtype=torch.float32)
#     save_ids = ['train', 'val']
#     train_val_ids = [train_ids, val_ids]
#     mean_z = -float(torch.mean(trans[:, 2]).item())

#     for split in range(2):
#         transform_dict = dict()
#         transform_dict['focal_len'] = float(focal_len[0])
#         transform_dict['cx'] = float(w/2.0)
#         transform_dict['cy'] = float(h/2.0)
#         transform_dict['frames'] = []
#         ids = train_val_ids[split]
#         save_id = save_ids[split]

#         for i in ids:
#             i = i.item()
#             frame_dict = dict()
#             frame_dict['img_id'] = i
#             frame_dict['aud_id'] = i

#             pose[:3, :3] = rot_inv[i]
#             pose[:3, 3] = trans_inv[i, :, 0]

#             frame_dict['transform_matrix'] = pose.numpy().tolist()

#             transform_dict['frames'].append(frame_dict)

#         with open(os.path.join(base_dir, 'transforms_' + save_id + '.json'), 'w') as fp:
#             json.dump(transform_dict, fp, indent=2, separators=(',', ': '))

#     print(f'[INFO] ===== finished saving transforms =====')

#    