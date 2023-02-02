import os
import re
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument(
    "path", type=str, help=""
)
args = parser.parse_args()

lrs_dir = args.path

lrs_vids = 0
obama_vids = 0

for d in os.walk(lrs_dir):
	dirpath, dirdirs, dirfiles = d
	for file in dirfiles:		
		if re.match('.+_obama\.mp4', file):
			obama_vids +=1
		elif re.match('.+\.mp4', file):
			lrs_vids +=1

print(f'lrs_vids: {lrs_vids}')

print(f'obama_vids: {obama_vids}')

