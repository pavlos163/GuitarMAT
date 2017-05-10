import librosa
import plot as plt
import numpy as np
from numpy.fft import rfft
from numpy import argmax, mean, diff, log
from scipy.signal import fftconvolve, kaiser
from matplotlib.mlab import find

def save_plot(filename):
  y, sr = librosa.load(filename, sr=40000)
  
  D = librosa.stft(y)

  pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr, fmin=75, fmax=1600)

  np.set_printoptions(threshold=np.nan)
  print pitches[np.nonzero(pitches)]

  print(freq_from_fft(y, 44000))
  print(freq_from_autocorr(y, 44000))

  plt.plot_waveform(y)
  plt.plot_spectrogram(D)

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