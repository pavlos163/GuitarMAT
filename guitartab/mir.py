import librosa
import librosa.display
import matplotlib.pylab as plt
import numpy as np
from numpy.fft import rfft
from numpy import argmax, mean, diff, log, unravel_index, arange, copy
from scipy.signal import fftconvolve, kaiser, decimate
from matplotlib.mlab import find
from music21 import *

def transcribe(filename):
  y, sr = librosa.load(filename, sr=40000)

  pitches = detect_pitch(y, sr)

  notes = convert_to_notes(pitches)
  
  # plt.plot_waveform(y)
  # plt.plot_spectrogram(D)

def convert_to_notes(pitches):
  notes = []
  pitches = sum(pitches, [])
  for pitch in pitches:
    notes.append(note.Note(pitch))

  return notes

def detect_pitch(y, sr):
  onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
  pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

  notes = []

  for i in range(0, len(onset_frames)):
    # TODO: Check without +1
    onset = onset_frames[i] + 1
    index = magnitudes[:, onset].argmax()
    pitch = pitches[index, onset]
    notes.append(librosa.hz_to_note(pitch))

  return notes

# OTHER F0 DETECTION METHODS:
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