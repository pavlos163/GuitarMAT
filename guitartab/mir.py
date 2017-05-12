import librosa
import librosa.display
import matplotlib.pylab as plt
import numpy as np
from numpy.fft import rfft
from numpy import argmax, mean, diff, log, unravel_index, arange, copy
from scipy.signal import fftconvolve, kaiser, decimate
from matplotlib.mlab import find

def save_plot(filename):
  y, sr = librosa.load(filename, sr=40000)

  D = librosa.stft(y)

  onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
  oenv = librosa.onset.onset_strength(y=y, sr=sr)

  onset_bt = librosa.onset.onset_backtrack(onset_frames, oenv)

  new_onset_bt = librosa.frames_to_samples(onset_bt)

  print new_onset_bt[1:]

  slices = np.split(y, new_onset_bt[1:])
  for i in range(0, len(slices)):
    print freq_from_hps(slices[i], 40000)

  #for i in range(0, len(slices)):
  #  print "---------------"
  #  print ("Autocorr:")
  #  print freq_from_autocorr(slices[i], 40000)
  #  print ("FFT:")
  #  print freq_from_fft(slices[i], 40000)
  #  print ("HPS:")
  #  print freq_from_hps(slices[i], 40000)

  #for i in range(0, len(slices)):
  #  stft_output = librosa.stft(slices[i])
  #  plt.figure()
  #  librosa.display.specshow(librosa.amplitude_to_db(stft_output, 
  #    ref=np.max), y_axis='log', x_axis='time')
  #  plt.title('Power Spectrogram')
  #  plt.colorbar(format='%+2.0f dB')
  #  plt.tight_layout()
  #  plt.show()

  # Autocorrelation and HPS produce the best results for E2.
  #print freq_from_autocorr(y, 40000)
  #print freq_from_fft(y, 40000)
  #print freq_from_hps(y, 40000)

  notes = []

  #notes.append(librosa.hz_to_note(freq))
  #print notes

  #plt.plot_waveform(y)
  #plt.plot_spectrogram(D)

def freq_from_fft(signal, sr):
  N = len(signal)
  windowed = signal * kaiser(N, 100)
  f = rfft(windowed)
  i_peak = argmax(abs(f))
  i_interp = parabolic(log(abs(f)), i_peak)[0]

  return sr * i_interp / N

def parabolic(f, x):
  xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
  yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
  return (xv, yv)

def freq_from_autocorr(signal, sr):
  signal -= mean(signal)
  corr = fftconvolve(signal, signal[::-1], mode='full')
  corr = corr[len(corr)/2:]

  d = diff(corr)
  start = find(d > 0)[0]

  i_peak = argmax(corr[start:]) + start
  i_interp = parabolic(corr, i_peak)[0]

  return sr / i_interp

def freq_from_hps(signal, fs):
    """Estimate frequency using harmonic product spectrum
    Low frequency noise piles up and overwhelms the desired peaks
    """
    N = len(signal)
    signal -= mean(signal)  # Remove DC offset

    # Compute Fourier transform of windowed signal
    windowed = signal * kaiser(N, 100)

    # Get spectrum
    X = log(abs(rfft(windowed)))

    # Downsample sum logs of spectra instead of multiplying
    hps = copy(X)
    for h in arange(2, 9): # TODO: choose a smarter upper limit
        dec = decimate(X, h)
        hps[:len(dec)] += dec

    # Find the peak and interpolate to get a more accurate peak
    i_peak = argmax(hps[:len(dec)])
    i_interp = parabolic(hps, i_peak)[0]

    # Convert to equivalent frequency
    return fs * i_interp / N  # Hz