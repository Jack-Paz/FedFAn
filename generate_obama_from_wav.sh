wav=$1

workspace=trial_obama/ #videos are moved from here to other dir

echo "doing create feats"

#assign variable to feature 

filepath="$(dirname "${wav}")" ; file="$(basename "${wav}")"

filename="${file%.*}" #without extension

featname=${filepath}/${filename}_eo.npy #add _eo.npy, same folder

if [[ ! -f ${featname} ]]; then
#extract features from wav
    python RAD-NeRF/nerf/asr.py --wav ${wav} --save_feats
fi 

echo "done create feats: ${featname}"


echo "doing extract pose"
#infer video name
folder="$(dirname "${wav}")" ; file_w_ext="$(basename "${wav}")"
file_wo_ext="${file_w_ext%.*}"


vid=${folder}/${file_wo_ext}.mp4

pose=${folder}/${file_wo_ext}/transforms_train.json

if [[ ! -f ${pose} ]]; then
    bash make_pose_matrix.sh ${vid}
fi

echo "doing create video"
python RAD-NeRF/test.py \
    --pose ${pose} \
    --ckpt RAD-NeRF/data/pretrained/obama_eo.pth \
    --aud ${featname} \
    --workspace ${workspace} \
    --name ${filename}_obama \
    -O --torso

outfile=${workspace}results/${filename}_obama.mp4



mv $outfile $filepath #move it to the other dir - good idea?

# bash add_audio_to_video.sh ${filepath}/${filename}_obama.mp4 ${wav}

echo "done create video"




# python test.py \
#     --pose data/obama/transforms_train.json \
#     --ckpt trial_obama_eo_torso/checkpoints/ngp.pth \
#     --aud ${featname} \
#     --workspace trial_test \
#     --bg_img data/obama/bc.jpg \
#     -l 10 -m 10 -r 10 \
#     -O --torso --data_range 0 100 --gui --asr


