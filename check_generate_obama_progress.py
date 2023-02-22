import os
import re
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument(
    "path", type=str, help=""
)
args = parser.parse_args()

lrs_dir = args.path

lrs_vids = []
obama_vids = []

for d in os.walk(lrs_dir):
	dirpath, dirdirs, dirfiles = d
	for file in dirfiles:
		x = re.match('.+/(.+/\d+)_obama\.mp4', f'{dirpath}/{file}')
		if x:
			obama_vids.append(x.group(1))
		y = re.match('.+/(.+/\d+)\.mp4', f'{dirpath}/{file}')
		if y:
			lrs_vids.append(y.group(1))

diff = set(lrs_vids) - set(obama_vids)
print(f'n lrs_vids: {len(lrs_vids)}')
print(f'n obama_vids: {len(obama_vids)}')
print(f'diff:{len(diff)}, diff vids:')
print(diff)
