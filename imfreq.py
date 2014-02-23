 #!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'

def main(source=False):
    from skimage import io
    from os import path
    from chr_helpers import get_config_file
    
    config = get_config_file(localpath=path.dirname(path.realpath(__file__))+"/")
    
    #IMPORT VARIABLES
    if not source:
	    source = config.get('Source', 'source')
    data_path = config.get('Addresses', source)
    compare_files = config.get("Data", "compare_files")
    #END IMPORT VARIABLES
    
    data_path = path.expanduser(data_path)
    
    compare_files = compare_files.split('; ')
    compare_files = [location_pair.split(', ') for location_pair in compare_files]

    for location_pair in compare_files:
	if location_pair[0][-1] != "/":
	    location_pair[0] = location_pair[0] + "/" #fixes trailing slashes for file-pair directories in case the user forgot to specify them under gen.cfg
	for data_file in location_pair[1:]:
	    file_path = data_path + location_pair[0] + data_file
	    
	    image = io.imread(file_path, as_grey=True)
	
def plot_dots(dataframe, image=None):
    import matplotlib.pyplot as plt
    from matplotlib import axis
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 9))  
    ax[0].imshow(image, interpolation = "none")
    ax[1].scatter(dataframe.index, dataframe["amplitude"], s=5, alpha=0.2, linewidths=0)
    ax[1].set_yscale('symlog')
    ax[1].set_ylim(ymin=0)
    ax[1].set_xlim(xmin=0)
    


	
    
def freq_extraction(image):
    import numpy as np
    F = np.fft.fft2(image)
    F_norm = np.abs(F)
    freq_values_y = np.fft.fftfreq(np.shape(F)[0])
    freq_values_x = np.fft.fftfreq(np.shape(F)[1])
    freq_spectrum = np.zeros((2,np.shape(F)[0]*np.shape(F)[1]))
    for iy, row in enumerate(F_norm):
	for ix, amplitude in enumerate(row):
	    iteration = iy*np.shape(F)[1]+ix
	    freq_spectrum[0,iteration] = np.sqrt(freq_values_y[iy]**2+freq_values_x[ix]**2)
	    freq_spectrum[1,iteration] = amplitude
    return freq_spectrum

def freq_sort(freq_spectrum):
    import pandas as pd
    freq_spectrum = freq_spectrum.T
    freq_spectrum = pd.DataFrame(freq_spectrum,columns=["frequency", "amplitude"])
    freq_spectrum = freq_spectrum.groupby(["frequency"]).sum()
    #~freq_spectrum = freq_spectrum.sort("frequency")
    return freq_spectrum

if __name__ == '__main__':
    main()
    #~show()
