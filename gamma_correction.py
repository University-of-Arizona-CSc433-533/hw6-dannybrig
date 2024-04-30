import numpy as np
import imageio
from matplotlib import pyplot as plt

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file_name', type=str,
                    help='File path for HDR image.')
parser.add_argument('--gamma', type=float, default=0.2,
                    help='Gamma for gamma correction.')
args = parser.parse_args()

# Read HDR file
hdr_path = '/Users/dbrig/Documents/Python/csc-533/hw6-dannybrig/' + args.file_name
img = imageio.imread(hdr_path)
img = np.array(img)

# Normalize HDR image
img = img / img.max()

# Compute luminance
L = (1.0/61.0) * (20.0*img[:,:,0] + 40.0*img[:,:,1] + img[:,:,2])
L_prime = L**args.gamma

# Correct Image
scale = L_prime/L
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