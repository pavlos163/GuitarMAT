import librosa
import plot as plt
import numpy as np
from music21 import *

def transcribe(filename):
  y, sr = librosa.load(filename, sr=40000)

  D = librosa.stft(y)

  pitches = detect_pitch(y, sr)

  # TODO: Create MusicXML file.
  notes = convert_to_notes(pitches)

  plt.plot_waveform(y)
  plt.plot_spectrogram(D)

  return pitches

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