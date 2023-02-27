import matplotlib.pyplot as plt
import numpy as np
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument('input_folder', type=str, help='experiment "workspace"')
args = parser.parse_args()
input_folder = args.input_folder

def main(input_folder):
	return None

if __name__=='__main__':
	x = main(input_folder)
	print(x)