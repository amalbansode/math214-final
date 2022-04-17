# Attenuate amplitude as a function of frequency (specifically, octave distance from cutoff)

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, rfftfreq, irfft
import math

INFILE = "./.wav/Piano.wav"
OUTFILE = "./fancy.wav"
CUTOFF_FREQ = 300  # Hz
ATTENUATION_AMP = 6

AUDIBLE_FREQS = np.arange(start=20, stop=20000, step=1)
attenuation_amp = np.zeros(AUDIBLE_FREQS.shape)

backwards_octave_idx = 1  # counter as we traverse octaves

# Actually start the filter half an octave before the cutoff
filter_start_freq = CUTOFF_FREQ + int(CUTOFF_FREQ / 2)
f_curr = filter_start_freq

while f_curr > 20:
    num_octaves_from_cutoff = math.log(filter_start_freq / f_curr, 2)
    rise = -ATTENUATION_AMP
    run = f_curr / 2
    slope_this_octave = rise / run

    baseline_attenuation_this_octave = num_octaves_from_cutoff * (-ATTENUATION_AMP)

    for i in range(int(f_curr / 2), int(f_curr)):
        attenuation_this_freq = (f_curr - i) * slope_this_octave
        attenuation_amp[i] = attenuation_this_freq + baseline_attenuation_this_octave

    # for next octave
    f_curr = f_curr / 2
    backwards_octave_idx = backwards_octave_idx + 1

# Plot the attenuation function
plt.plot(AUDIBLE_FREQS, attenuation_amp, scaley=True)
plt.xlim([0, 1000])
plt.title("Attenuation Signal in Frequency Domain (Cutoff = 300 Hz)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (unitless)")
plt.show()

# Now, actually process a file and apply this attenuation filter!
# read in signal in time domain (window)
# dft(window) to get window in freq domain
# add attenuation to window_f to get window_f'
#   - since signal read in is "binned", need to read frequency domain value, find the appropriate amplitude attenuation
#     from const AS, and add those two values

# File IO stuff
BLOCK_SIZE = 1024
SAMPLE_RATE, indata = read(INFILE)
output = np.empty(0)

# Iterate over the audio data in discrete 1024 sample "windows" and take the
# DFT of that, process it, then inverse DFT and push to end of new audio data
for block_idx in range(math.floor((max(indata.shape) / BLOCK_SIZE) + 1)):

    block = indata[block_idx * BLOCK_SIZE:(block_idx + 1) * BLOCK_SIZE]

    # Apply DFT
    yf = rfft(block)

    xf = rfftfreq(len(yf), d=1.0 / SAMPLE_RATE)

    # plot original freq domain
    # plt.plot(xf, yf, scaley=False)
    # plt.xlim([0, 20000])
    # plt.ylim([0, 70])
    # plt.title("Frequency Domain in 1st Time Window BEFORE Attenuation")
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("Amplitude (unitless)")
    # plt.show()

    # Apply Audio Effect
    for i in range(max(xf.shape)):
        this_freq_floored = math.floor(xf[i])  # to index into attenuation vector with binned frequencies
        if 20 < this_freq_floored < 20000:
            attenuated = yf[i] + attenuation_amp[
                this_freq_floored - 20]  # offset by 20 since attn starts at human hearing range
            yf[i] = attenuated

    # plot updated freq domain
    # plt.plot(xf, yf, scaley=False)
    # plt.xlim([0, 20000])
    # plt.ylim([0, 70])
    # plt.title("Frequency Domain in 1st Time Window AFTER Attenuation")
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("Amplitude (unitless)")
    # plt.show()

    # Inverse DFT
    yf = irfft(yf)

    # break (use this when plotting a single window)

    # Push the 1024 block window to output. Creates output one block at a time
    output = np.append(output, yf)

# write new audio data to output file
write(OUTFILE, SAMPLE_RATE, output)
