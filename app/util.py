import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import itertools
from librosa.core import hz_to_note

def plot_waveform(y):
  plt.figure()
  librosa.display.waveplot(y, sr=44100)
  plt.tight_layout()
  plt.savefig('static/plots/' + 'audio.png')
  plt.show()

def plot_spectrogram(stft_output, xlabel='Time', ylabel='Hz', sr=44100, fmin=None, fmax=None):
  plt.figure()
  librosa.display.specshow(librosa.amplitude_to_db(stft_output, 
    ref=np.max), y_axis='log', x_axis='time', sr=sr, fmin=fmin, fmax=fmax)
  plt.title('Power Spectrogram')
  plt.colorbar(format='%+2.0f dB')
  plt.tight_layout()
  plt.savefig('static/plots/' + 'spectrogram.png')
  plt.show()

def remove_values_from_list(l, val):
  return [value for value in l if value != val]

def round_to_base(val, base):
  return int(base * round(float(val)/base))

def pitches_to_notes(pitches):
  notes = []
  for pitch in pitches:
    notes.append(hz_to_note(pitch))
  return notes

def flatten(l):
  return list(itertools.chain.from_iterable(l))