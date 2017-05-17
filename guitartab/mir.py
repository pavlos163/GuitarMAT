import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import plot
from scipy import signal
from music21 import *
from frequency_estimator import freq_from_hps

def transcribe(filename):
  y, sr = librosa.load(filename, sr=40000)

  # High-pass filter to remove low frequency noise.
  y = highpass_filter(y, sr)

  D = librosa.stft(y)
  fmin = 75
  fmax = 1400

  pitches = detect_pitch(y, sr)

  print freq_from_hps(y, sr)

  # TODO: Create MusicXML file.
  notes = convert_to_notes(pitches)

  # plot.plot_waveform(y)
  # plot.plot_spectrogram(D, sr=sr, fmin=fmin, fmax=fmax)
  plt.close('all')

  return pitches

def convert_to_notes(pitches):
  notes = []
  pitches = sum(pitches, [])
  for pitch in pitches:
    notes.append(note.Note(pitch))

  return notes

# Checking the pitch some frames the onset time increased precision.
def detect_pitch(y, sr, onset_offset=5, fmin=75, fmax=1400):
  onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
  
  filtered_onset_frames = remove_dense_onsets(onset_frames)

  pitches, magnitudes = librosa.piptrack(y=y, sr=sr, fmin=fmin, fmax=fmax)

  notes = []

  for i in range(0, len(filtered_onset_frames)):
    onset = filtered_onset_frames[i] + onset_offset
    index = magnitudes[:, onset].argmax()
    pitch = pitches[index, onset]
    if (pitch != 0):
      notes.append(librosa.hz_to_note(pitch))

  return notes

# For each note played, get the n strongest peaks in the frequency spectrum.
def get_peaks(pitches, magnitudes, onset_frames, n=5):
    candidate_list = []

    for i in range(0, len(onset_frames)):
      candidates = []
      onset = onset_frames[i] + 1
      indices = np.argpartition(magnitudes[:, onset], 0-n)[0-n:]

      for j in indices:
        candidates.append(pitches[j, onset])

      candidate_list.append(candidates)

    return candidate_list

def highpass_filter(y, sr):
  # Parameters
  #time_start = 0  # seconds
  #time_end = 1  # seconds
  filter_stop_freq = 70  # Hz
  filter_pass_freq = 100  # Hz
  filter_order = 1001

  # High-pass filter
  nyquist_rate = sr / 2.
  desired = (0, 0, 1, 1)
  bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
  filter_coefs = signal.firls(filter_order, bands, desired, nyq=nyquist_rate)

  # Apply high-pass filter
  filtered_audio = signal.filtfilt(filter_coefs, [1], y)

  # Only analyze the audio between time_start and time_end
  #time_seconds = np.arange(filtered_audio.size, dtype=float) / sr
  #audio_to_analyze = filtered_audio[(time_seconds >= time_start) &
  #                                (time_seconds <= time_end)]

  return filtered_audio

def segment_sigal(y, sr, onset_frames=None):
  if (onset_frames == None):
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)

  oenv = librosa.onset.onset_strength(y=y, sr=sr)
  onset_bt = librosa.onset.onset_backtrack(onset_frames, oenv)

  new_onset_bt = librosa.frames_to_samples(onset_bt)

  slices = np.split(y, new_onset_bt[1:])
  
  return slices

def remove_dense_onsets(onset_frames):
  indices_to_remove = []

  # Remove onsets that are too close together.
  for i in range(1, len(onset_frames)):
    if onset_frames[i] - onset_frames[i - 1] <= 3:
      indices_to_remove.append(i)

  return np.delete(onset_frames, indices_to_remove)
