# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 11:54:50 2022

@author: Tyler
"""

#import wave
import numpy as np
import soundfile as sf
from scipy.io.wavfile import write
from scipy.fftpack import rfft, rfftfreq, irfft
import matplotlib.pyplot as plt

#Sets all frequencies below a cutoff freq (integer) to 0.
#We can make other effects later, this just seemed easy for proof of concept
def brickWallHP(data, cutoff):
    data[0:cutoff+1] = 0
        
    return data

def run(infile_name, outfile_name):
    #File IO stuff
    BLOCK_SIZE = 1024
    _, SAMPLE_RATE = sf.read(infile_name)
    output = np.empty(0)
    
    #Plot setup
    plt.ylim([0, 15])
    plt.xlim([0, 20000])
    
    #Iterate over the audio data in discrete 1024 sample "windows" and take the
    #DFT of that, process it, then inverse DFT and push to end of new audio data
    for block in sf.blocks(infile_name, blocksize = BLOCK_SIZE):
        #Apply DFT
        yf = rfft(block)
        
        # This is really slow and looks awful, but is good to visualize what is happening
        #might crash on your pc tho
        xf = rfftfreq(len(yf),d=1.0/SAMPLE_RATE)
        # plt.plot(xf, yf, scaley=False)
        # plt.show()
        
        # Apply Audio Effect (not working)
        cutoff = 300 #Hz
        cutoff_idx = -1
        for i in range(max(xf.shape)):
            if xf[i] > cutoff:
                cutoff_idx = i
                break

        yf = brickWallHP(yf, cutoff_idx)
        # plt.plot(xf, yf, scaley=False)
        # plt.show()
        
        #Inverse DFT
        yf = irfft(yf)
        
        #<TODO>Push the 1024 block window to output. Creates output one block at a time
        output = np.append(output, yf)

    #<TODO> : Not Working, write new audio data to output file
    write(outfile_name, SAMPLE_RATE, output)
    
    
run(".wav/Piano.wav", "testing.wav")