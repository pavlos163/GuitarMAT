import librosa
import plot as plt
import numpy as np
import heapq
from music21 import *

def transcribe(filename):
  y, sr = librosa.load(filename, sr=40000)

  # D = librosa.stft(y)

  pitches = detect_pitch(y, sr)

  # TODO: Create MusicXML file.
  notes = convert_to_notes(pitches)

  # plt.plot_waveform(y)
  # plt.plot_spectrogram(D)

  return pitches

def convert_to_notes(pitches):
  notes = []
  pitches = sum(pitches, [])
  for pitch in pitches:
    notes.append(note.Note(pitch))

  return notes

def detect_pitch(y, sr):
  onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
  pitches, magnitudes = librosa.piptrack(y=y, sr=sr, fmin=75)

  notes = []

  # Checking the pitch some frames the onset time increased precision.
  onset_offset = 5

  for i in range(0, len(onset_frames)):
    onset = onset_frames[i] + onset_offset
    index = magnitudes[:, onset].argmax()
    pitch = pitches[index, onset]
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