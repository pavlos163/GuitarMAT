import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import plot
import music21
from music21 import *
from librosa.core import hz_to_note
from onset import get_onset_frames
from scipy import signal
from frequency_estimator import freq_from_autocorr

def transcribe(filename):
  sr = 44100
  music21.environment.set('musicxmlPath', '/usr/bin/musescore')

  # proc = madmom.OnsetPeakPickingProcessor()

  # onset_detector = madmom.SpectralOnsetProcessor()(filename)
  # print proc(onset_detector)

  # onset_detector = madmom.SpectralOnsetProcessor(onset_method='superflux')(filename)
  # print proc(onset_detector)

  onset_frames = get_onset_frames(filename)

  y, sr = librosa.load(filename, sr=sr)

  filtered_y = filter(y, sr)

  D = librosa.stft(filtered_y)

  # stft_pitches = detect_pitch(filtered_y, sr, 'stft')
  autocorr_pitches = detect_pitch(filtered_y, sr, onset_frames, 'autocorr')

  pitches = autocorr_pitches

  notes = []
  for pitch in pitches:
    notes.append(hz_to_note(pitch))

  # Convert to Music21 stream and export to MusicXML file.
  note_stream = convert_to_notes(notes)

  note_stream.write("musicxml", "static/piece.mxl")

  # plot.plot_waveform(y)
  # plot.plot_spectrogram(D, sr)
  # plt.close('all')
  
  return notes

def convert_to_notes(pitches):
  notes = stream.Stream()
  pitches = sum(pitches, [])
  for pitch in pitches:
    f = note.Note(pitch)
    notes.append(f)

  return notes

# Checking the pitch some frames the onset time increased precision.
def detect_pitch(y, sr, onset_frames, method='stft', onset_offset=5, fmin=75, fmax=1400):
  result_pitches = []

  pitches, magnitudes = librosa.piptrack(y=y, 
    sr=sr, fmin=fmin, fmax=fmax)

  if method == 'stft':
      for i in range(0, len(onset_frames)):
        onset = onset_frames[i] + onset_offset
        index = magnitudes[:, onset].argmax()
        pitch = pitches[index, onset]
        # duration = detect_duration(magnitudes, index, onset)
        if (pitch != 0):
          result_pitches.append(pitch)

  elif method == 'autocorr':
    slices = segment_signal(y, sr, onset_frames)
    for segment in slices:
      pitch = freq_from_autocorr(segment, sr)
      result_pitches.append(pitch)

  return result_pitches

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

def filter(y, sr):
  # Removes frequencies lower than 60Hz and higher than 2000Hz.
  low_stop = 60  # Hz
  low_pass = 80
  high_pass = 1800
  high_stop = 2000
  filter_order = 1001

  # High-pass filter
  nyquist_rate = sr / 2.
  desired = (0, 0, 1, 1, 0, 0)
  bands = (0, low_stop, low_pass, high_pass, high_stop, nyquist_rate)
  filter_coefs = signal.firls(filter_order, bands, desired, nyq=nyquist_rate)

  # Apply high-pass filter
  filtered_audio = signal.filtfilt(filter_coefs, [1], y)

  return filtered_audio

def segment_signal(y, sr, onset_frames):

  # This splits the signal into slices that sum up to the whole signal according
  # to onset_bt.
  #oenv = librosa.onset.onset_strength(y=y, sr=sr)
  #onset_bt = librosa.onset.onset_backtrack(onset_frames, oenv)

  #new_onset_bt = librosa.frames_to_samples(onset_bt)

  #slices = np.split(y, new_onset_bt[1:])
  
  offset_start = int(librosa.time_to_samples(0.01, sr))
  offset_end = int(librosa.time_to_samples(0.099, sr))

  slices = np.array([y[i + offset_start : i + offset_end] for i
    in librosa.frames_to_samples(onset_frames)])

  return slices

def remove_values_from_list(l, val):
  return [value for value in l if value != val]

def detect_duration(magnitudes, bin, time_frame):
  # TODO: This is going to get messy if there is a new note played before
  # the last note has finished.
  duration = 0
  while magnitudes[bin, time_frame] > 1:
    duration += 1
    time_frame += 1

  return duration