import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, rfftfreq, irfft
import math

# Plot setup
# plt.ylim([-1000, 0])
plt.xlim([0, 20000])

# construct attenuation signal in frequency domain (maybe even dBFs?) <- constant across [20, 20k] Hz
# per octave, reduce loudness by x dB (attenuation)
# non-dbfs algo. if it is dbfs, attenuation is negative already
#   cutoff frequency (lowcut/highpass) <- f_curr
#   window_idx = 1
#   work backwards from f_curr. everything from [f_curr / 2, f_curr] is -(attenuation * window_idx)
#   f_curr = f_curr / 2
#   window_idx++
#   repeat until f_curr <= 20 Hz

INFILE = "./.wav/Piano.wav"
OUTFILE = "./fancy.wav"
CUTOFF_FREQ = 10000  # Hz, exclusive
ATTENUATION_AMP = 12  # dBs??? idk

AUDIBLE_FREQS = np.arange(start=20, stop=20000, step=1)
attenuation_amp = np.zeros(AUDIBLE_FREQS.shape)

backwards_octave_idx = 1  # counter as we traverse octaves
f_curr = CUTOFF_FREQ

# <TODO>-----
# Convert everything to dB / dbFS?
# What are the units of rfft()?
# </TODO>-----

while f_curr > 20:
    num_octaves_from_cutoff = math.log(CUTOFF_FREQ / f_curr, 2)
    print("f_curr " + str(f_curr) + "; N_O " + str(num_octaves_from_cutoff))
    rise = -ATTENUATION_AMP
    run = f_curr / 2
    slope_this_octave = rise / run

    baseline_attenuation_this_octave = num_octaves_from_cutoff * (-ATTENUATION_AMP)

    for i in range(int(f_curr / 2), int(f_curr)):
        attenuation_this_freq = (f_curr - i) * slope_this_octave
        attenuation_amp[i] = attenuation_this_freq + baseline_attenuation_this_octave

    # for next octave
    f_curr = f_curr / 2  # <QUESTION> is this guaranteed to return an integer? </QUESTION>
    backwards_octave_idx = backwards_octave_idx + 1

plt.plot(AUDIBLE_FREQS, attenuation_amp, scaley=True)
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

# <TODO>-----
# Windowing function instead of these rectangular blocks. See:
# https://flothesof.github.io/FFT-window-properties-frequency-analysis.html For help with python implementation
# https://www.ap.com/technical-library/fft-windows/ For general knowledge
# </TODO>-----

# Iterate over the audio data in discrete 1024 sample "windows" and take the
# DFT of that, process it, then inverse DFT and push to end of new audio data
for block_idx in range(math.floor((max(indata.shape) / BLOCK_SIZE) + 1)):

    block = indata[block_idx * BLOCK_SIZE:(block_idx + 1) * BLOCK_SIZE]

    # Apply DFT
    yf = rfft(block)

    xf = rfftfreq(len(yf), d=1.0 / SAMPLE_RATE)

    # plot original freq domain
    # plt.plot(xf, yf, scaley=True)
    # plt.show()

    # Apply Audio Effect
    for i in range(max(xf.shape)):
        this_freq_floored = math.floor(xf[i])  # to index into attenuation vector
        if 20 < this_freq_floored < 20000:
            attenuated = yf[i] + attenuation_amp[
                this_freq_floored - 20]  # offset by 20 since attn starts at human hearing range
            yf[i] = attenuated

    # plot updated freq domain
    # plt.plot(xf, yf, scaley=True)
    # plt.show()

    # Inverse DFT
    yf = irfft(yf)

    break

    # Push the 1024 block window to output. Creates output one block at a time
    output = np.append(output, yf)

# write new audio data to output file
write(OUTFILE, SAMPLE_RATE, output)
