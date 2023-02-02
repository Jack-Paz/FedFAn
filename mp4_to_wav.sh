mp4_name=$1


#extract filename
arrIN=(${mp4_name//./ }) #split string on the dot
filename=${arrIN[0]} #index name only, add _eo.npy


ffmpeg -i ${filename}.mp4 -acodec pcm_s16le -ac 1 -ar 16000 ${filename}.wav