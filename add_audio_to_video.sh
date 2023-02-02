add_audio_to_video

video=$1
audio=$2

ffmpeg -i $video -i $audio -c copy -map 0:v:0 -map 1:a:0 -c:a aac -b:a 192k ${video%.*}_a.mp4
