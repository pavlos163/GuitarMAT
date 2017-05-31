import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import plot
import music21
from music21 import *
from librosa.core import hz_to_note, frames_to_time
from onset import get_onset_frames
from pitch import detect_pitch
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor, CNNChordFeatureProcessor, CRFChordRecognitionProcessor
from scipy.signal import butter, sosfilt, resample
from frequency_estimator import freq_from_autocorr, freq_from_hps

def transcribe(filename):
  sr = 44100
  music21.environment.set('musicxmlPath', '/usr/bin/musescore')

  y, sr = librosa.load(filename, sr=sr)

  # Finds all chords BUT also several false positives in monophonic samples.
  dcp = DeepChromaProcessor()
  decode = DeepChromaChordRecognitionProcessor()
  chroma = dcp(filename)
  print(decode(chroma))

  # Very similar results with the CNN:
  # featproc = CNNChordFeatureProcessor()
  # decode = CRFChordRecognitionProcessor()
  # feats = featproc(filename)
  # print(decode(feats))

  # Get onset times.
  onset_frames = get_onset_frames(filename, sr)

  print frames_to_time(onset_frames, sr)

  # Filter the signal.
  filtered_y = bandpass_filter(y, sr, 80., 4000.)

  chroma = librosa.feature.chroma_stft(y=filtered_y, sr=sr)
  plt.figure(figsize=(10, 4))
  librosa.display.specshow(chroma, y_axis='chroma', x_axis='time')
  plt.colorbar()
  plt.title('Chromagram')
  plt.tight_layout()
  plt.show()

  # D = librosa.stft(filtered_y)

  # Detect pitch with different methods:
  stft_pitches = detect_pitch(filtered_y, sr, onset_frames, 'min_stft')
  print hz_to_note(stft_pitches)

  hps_pitches = detect_pitch(filtered_y, sr, onset_frames, 'hps')
  # print hps_pitches

  pitches = stft_pitches

  # print hz_to_note([x - 10 for x in pitches])

  # This -10 is a bit arbitrary.
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

def bandpass_filter(y, sr, lowcut, highcut):
  # Setup parameters.
  nyquist_rate = sr / 2.
  filter_order = 3
  normalized_low = lowcut / nyquist_rate
  normalized_high = highcut / nyquist_rate

  sos = butter(filter_order, [normalized_low, normalized_high],
    btype='bandpass', output='sos')
  
  y = sosfilt(sos, y)
  return y

def detect_duration(magnitudes, bin, time_frame):
  # TODO: This is going to get messy if there is a new note played before
  # the last note has finished.
  duration = 0
  while magnitudes[bin, time_frame] > 1:
    duration += 1
    time_frame += 1

  return duration