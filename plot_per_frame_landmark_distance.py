import matplotlib.pyplot as plt
import numpy as np
import pickle

import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument("lm1", type=str, default='')
parser.add_argument("lm2", type=str, default='')
args = parser.parse_args()

from utils import locations

lm1 = pickle.load(open(args.lm1, 'rb'))
lm2 = pickle.load(open(args.lm2, 'rb'))

from utils import locations, locname_to_locno, locno_to_locname, loc_to_locname, locname_to_loc, loc_to_locno, locno_to_loc

from utils import length_check
lm1, lm2 = length_check(lm1, lm2)

# assert len(lm1)==len(lm2), 'landmark files n frames mismatch!'
assert len(lm1[0])==len(lm2[0]), 'landmark files n landmarks mismatch!'

print(lm1.shape)
print(lm2.shape)

diff_lm = lm1 - lm2

print(diff_lm.shape)

per_frame_global_diff = np.sum(diff_lm, axis=(1))

lips_diff = diff_lm[:,locname_to_loc['lips'],:]
per_frame_lips_diff = np.sum(np.abs(lips_diff), axis=(1,2))

plt.plot(per_frame_lips_diff)
# plt.legend(['x','y','z'])
plt.show()

