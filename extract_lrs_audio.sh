lrs_folder=$1


for file in $(find $lrs_folder -name '*.mp4'); do
	echo $file
	bash mp4_to_wav.sh $file
done