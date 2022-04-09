import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [16,10]
plt.rcParams.update({'font.size':18})

#Create a simple signal with two frequencies
data_step   = 0.000125
t           = np.arange(start=0,stop=2,step=data_step)
f_clean     = 1 * (np.sin(2*np.pi*256*t) + np.sin(2*np.pi*554*t))
f_noise     = f_clean + 2.5*np.random.randn(len(t))

plt.plot(t,f_noise,color='c',label='Noisy')
plt.plot(t,f_clean,color='k',label='Clean')
plt.legend()
plt.show()

from scipy.fft import rfft,rfftfreq
n    = len(t)
yf   = rfft(f_noise)
xf   = rfftfreq(n,data_step)
plt.plot(xf,np.abs(yf))
plt.show()

yf_abs      = np.abs(yf)
indices     = yf_abs > 3000   # filter out those value under 300
yf_clean    = indices * yf # noise frequency will be set to 0
plt.plot(xf,np.abs(yf_clean))
plt.show()

from scipy.fft import irfft
new_f_clean = irfft(yf_clean)
plt.plot(t,new_f_clean)
plt.ylim(-6,8)
plt.show()

import IPython.display as ipd
### UNCOMMENT ONE OF THESE TO EXAMINE NOISY VS "CLEANED" SIGNAL
# ipd.Audio(f_noise, rate=1/data_step, autoplay=True)
ipd.Audio(new_f_clean, rate=1/data_step, autoplay=True)

# write out wav files
from scipy.io.wavfile import write

write("f_noise.wav", 8000, f_noise)
write("new_f_clean.wav", 8000, new_f_clean)
