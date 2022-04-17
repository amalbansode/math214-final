import numpy as np
import matplotlib.pyplot as plt

# construct attenuation signal in frequency domain (maybe even dBFs?) <- constant across [20, 20k] Hz
# per octave, reduce loudness by x dB (attenuation)
# non-dbfs algo. if it is dbfs, attenuation is negative already
#   cutoff frequency (lowcut/highpass) <- f_curr
#   window_idx = 1
#   work backwards from f_curr. everything from [f_curr / 2, f_curr] is -(attenuation * window_idx)
#   f_curr = f_curr / 2
#   window_idx++
#   repeat until f_curr <= 20 Hz

CUTOFF_FREQ = 500 # Hz, exclusive
ATTENUATION_AMP = 6 # dBs??? idx

AUDIBLE_FREQS = np.arange(start=20,stop=20000,step=1)
attenuation_amp = np.zeros(AUDIBLE_FREQS.shape)

backwards_octave_idx = 1 # counter as we traverse octaves
f_curr = CUTOFF_FREQ

while f_curr > 20:
    attenuation_this_octave = -ATTENUATION_AMP * backwards_octave_idx
    for i in range(int(f_curr / 2), int(f_curr)):
        attenuation_amp[i] = attenuation_this_octave

    # for next octave
    f_curr = f_curr / 2
    backwards_octave_idx = backwards_octave_idx + 1

plt.plot(AUDIBLE_FREQS,attenuation_amp)
plt.show()

# read in signal in time domain (window)
# dft(window) to get window in freq domain
# add attenuation to window_f to get window_f'
#   - since signal read in is "binned", need to read frequency domain value, find the appropriate amplitude attenuation
#     from const AS, and add those two values

# inverse of window_f' to get window'
# concatenate window's to get signal'

