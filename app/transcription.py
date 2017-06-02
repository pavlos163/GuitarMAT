import librosa
import librosa.display
import matplotlib.pyplot as plt
import plot
from music21 import *
from librosa.core import hz_to_note, time_to_frames, frames_to_time
from onset import get_onset_frames
from pitch import detect_pitch
from chords import get_chords
from duration import get_durations
from scipy.signal import butter, sosfilt

def transcribe(filename):
  sr = 44100
  environment.set('musicxmlPath', '/usr/bin/musescore')

  y, sr = librosa.load(filename, sr=sr)

  # Get onset times.
  onset_frames = get_onset_frames(filename, sr)

  # print onset_frames

  durations = get_durations(onset_frames)

  # print durations

  # Filter the signal.
  filtered_y = bandpass_filter(y, sr, 80., 4000.)

  # chords = get_chords(filename, filtered_y, sr)

  # Detect pitch with different methods:
  # stft_pitches = detect_pitch(filtered_y, sr, onset_frames, 'min_stft')
  autocorr_pitches = detect_pitch(filtered_y, sr, onset_frames, 'autocorr')

  # Autocorr is good for low pitches: avg score: 0.7
  # Other_autocorr was best (windowed).
  # STFT good in general: avg score: 0.93
  pitches = autocorr_pitches

  notes = pitches_to_notes(pitches)

  # Convert to Music21 stream and export to MusicXML file.
  note_stream = notes_to_stream(notes, durations)

  note_stream.write("musicxml", "static/piece.mxl")

  # plot.plot_waveform(y)
  plot.plot_spectrogram(librosa.stft(y), sr)
  plt.close('all')
  
  return notes

def pitches_to_notes(pitches):
  notes = []
  for pitch in pitches:
    notes.append(hz_to_note(pitch))
  return notes

def notes_to_stream(notes, durations):
  note_stream = stream.Stream()
  note_stream.insert(0, clef.TrebleClef())
  note_stream.insert(0, tempo.MetronomeMark(number=120))
  notes = sum(notes, [])
  for i in range(0, len(notes)):
    f = note.Note(notes[i])
    f.duration = duration.Duration(durations[i])
    note_stream.append(f)

  return note_stream

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