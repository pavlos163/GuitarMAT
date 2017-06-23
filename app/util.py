import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import itertools
import essentia
import essentia.standard as ess
from librosa.core import hz_to_note, time_to_frames

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

def flatten(l):
  return list(itertools.chain.from_iterable(l))

def nmf_component_to_note(component_number):
  components = {0: "E2",
                1: "F2",
                2: "F#2",
                3: "G2",
                4: "G#2",
                5: "A2",
                6: "A#2",
                7: "B2",
                8: "C3",
                9: "C#3",
                10: "D3",
                11: "D#3",
                12: "E3",
                13: "F3",
                14: "F#3",
                15: "G3",
                16: "G#3",
                17: "A3",
                18: "A#3",
                19: "B3",
                20: "C4",
                21: "C#4",
                22: "D4",
                23: "D#4",
                24: "E4",
                25: "F4",
                26: "F#4",
                27: "G4",
                28: "G#4",
                29: "A4"
  }

  return components[component_number]

def plot_h_matrix(activations):
  n_components = activations.shape[0]

  for n in range(n_components):
    plt.subplot(np.ceil(n_components/2.0), 2, n+1)
    plt.plot(activations[n])
    plt.ylim(0, activations.max())
    plt.xlim(0, activations.shape[1])
    plt.ylabel(nmf_component_to_note(n))
    plt.xticks([])
    plt.yticks([])

  plt.show()

def plot_w_matrix(templates):
  n_components = templates.shape[1]

  for n in range(n_components):
    plt.subplot(np.ceil(n_components/2.0), 2, n+1)
    plt.plot(templates[n])
    plt.ylim(0, templates.max())
    plt.xlim(0, templates.shape[0])
    plt.ylabel(nmf_component_to_note(n))
    plt.xticks([])
    plt.yticks([])

  plt.show()

def get_tempo(y):
  tempo_estimator = ess.PercivalBpmEstimator()
  bpm = tempo_estimator(y)
  bpm = round_to_base(bpm, 5)
  if bpm < 60:
    bpm = bpm * 2
  elif bpm > 220:
    bpm = round_to_base(bpm / 2, 5)
  return bpm

def get_key(y):
  key_extractor = ess.KeyExtractor()
  key = key_extractor(essentia.array(y))
  return key

def get_tuning(spectrum):
    speaks = ess.SpectralPeaks()
    frequencies, magnitudes = speaks(essentia.array(spectrum))

    tuning = ess.TuningFrequency()
    freq, cents = tuning(frequencies, magnitudes)

def madmom_frames_to_librosa_frames(onset_frames, sr):
  onset_times = [float(x)/200. for x in onset_frames]
  return time_to_frames(onset_times, sr)