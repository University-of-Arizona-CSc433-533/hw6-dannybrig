import numpy as np
from scipy.signal import convolve2d
import imageio
from matplotlib import pyplot as plt

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file_name', type=str,
                    help='File path for HDR image.')
parser.add_argument('--kernel_size', type=float, default=7,
                    help='Size of box filter for convolution.')
parser.add_argument('--c', type=int, default=100,
                    help='Value used for determining gamma.')
args = parser.parse_args()

# Read HDR file
hdr_path = '/Users/dbrig/Documents/Python/csc-533/hw6-dannybrig/' + args.file_name
img = imageio.imread(hdr_path)
img = np.array(img)

# Normalize HDR image
img = img / img.max()

# Compute luminance
L = (1.0/61.0) * (20.0*img[:,:,0] + 40.0*img[:,:,1] + img[:,:,2])

# Design Box Filter
g = (1/args.kernel_size**2) * np.ones((args.kernel_size, args.kernel_size))

# Procedure
# B = np.convolve(np.log(L), g)
B = convolve2d(np.log(L), g, mode='same')
gamma = np.log(args.c) / (np.max(B) - np.min(B))
S = np.log(L) - B
L_prime = np.exp(gamma*B + S)
scale = L_prime / L

# Correct Image
img_gamma = np.zeros_like(img)
img_gamma[:,:,0] = scale*img[:,:,0] 
img_gamma[:,:,1] = scale*img[:,:,1] 
img_gamma[:,:,2] = scale*img[:,:,2] 

# Clip values
img_gamma = np.clip(img_gamma, 0, 1)

# Display
fig, axs = plt.subplots(1,2)
axs[0].imshow(img)
axs[0].set_title('Unaltered HDR Image')
axs[1].imshow(img_gamma)
axs[1].set_title('Gamma Corrected Image')
plt.show()