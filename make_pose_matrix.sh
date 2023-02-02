video=$1

folder="$(dirname "${video}")" ; file_w_ext="$(basename "${video}")"

file_wo_ext="${file_w_ext%.*}"

newfolder=${folder}/${file_wo_ext}/

if [[ ! -d $newfolder ]]; then
	mkdir ${newfolder}
	python extract_frames_from_video.py \
		--input_video ${video} \
		--output_folder ${newfolder}
	echo 'doing extract lms'
	python extract_2d_lms.py --img_dir ${newfolder}
fi

echo 'doing create track params dict'

#do create track params dict
python RAD-NeRF/data_utils/face_tracking/face_tracker.py \
	--path ${newfolder} \
	# --img_h 224 \
	# --img_w 224 \
	# --frame_num 38 \

echo 'doing create pose matrix'

python create_pose_matrix.py \
	--base_dir ${newfolder} \
	--ori_imgs_dir ${newfolder} \

echo 'done'
