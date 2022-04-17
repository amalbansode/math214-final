# Implement a simple "brick wall" frequency filter, i.e. suppress frequencies above or below a threshold.

import numpy as np
import soundfile as sf
from scipy.io.wavfile import write
from scipy.fftpack import rfft, rfftfreq, irfft

# Hard highpass filter beginning at cutoff. Values [0,cutoff] will be 0
def brickWallHP(data, cutoff):
    data[0:cutoff+1] = 0
        
    return data

# Hard lowpass filter beginning at cutoff. Values [cutoff, MAX_FREQ] will be 0
def brickWallLP(data, cutoff):
    data[cutoff:] = 0
    
    return data

def run(infile_name, outfile_name):
    # ile IO stuff
    BLOCK_SIZE = 1024
    _, SAMPLE_RATE = sf.read(infile_name)
    output = np.empty(0)
    
    # Iterate over the audio data in discrete 1024 sample "windows" and take the
    # DFT of that, process it, then inverse DFT and push to end of new audio data
    for block in sf.blocks(infile_name, blocksize = BLOCK_SIZE):
        # Apply DFT
        yf = rfft(block)
        
        xf = rfftfreq(len(yf),d=1.0/SAMPLE_RATE)

        # Apply Audio Effect
        cutoff = 300 # Hz
        cutoff_idx = -1
        for i in range(max(xf.shape)):
            if xf[i] > cutoff:
                cutoff_idx = i
                break
            
        # Apply Brickwall LP or HP as needed
        yf = brickWallLP(yf, cutoff_idx)
        # yf = brickWallHP(yf, cutoff_idx)

        # Inverse DFT
        yf = irfft(yf)

        # Push the 1024 block window to output. Creates output one block at a time
        output = np.append(output, yf)

    write(outfile_name, SAMPLE_RATE, output)
    
    
run(".wav/Piano.wav", "piano-brickwall.wav")
