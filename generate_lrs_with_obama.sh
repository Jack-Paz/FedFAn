lrs_folder=$1


for file in $(find $lrs_folder -name '*.wav'); do
	echo $file
	bash generate_obama_from_wav.sh $file
done