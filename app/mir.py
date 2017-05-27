import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import plot
import music21
from music21 import *
from scipy import signal
from frequency_estimator import freq_from_autocorr

def transcribe(filename):
  sr = 44100
  music21.environment.set('musicxmlPath', '/usr/bin/musescore')

  y, sr = librosa.load(filename, sr=sr)

  # High-pass filter to remove low frequency noise.
  filtered_y = highpass_filter(y, sr)

  D = librosa.stft(filtered_y)

  # stft_pitches = detect_pitch(filtered_y, sr, 'stft')
  autocorr_pitches = detect_pitch(filtered_y, sr, 'autocorr')

  pitches = autocorr_pitches

  # print autocorr_pitches
  # print stft_pitches

  notes = []
  for pitch in pitches:
    notes.append(get_note(pitch))

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
def detect_pitch(y, sr, method='stft', onset_offset=5, fmin=75, fmax=1400):
  result_pitches = []

  pitches, magnitudes = librosa.piptrack(y=y, 
    sr=sr, fmin=fmin, fmax=fmax)

  if method == 'stft':
      filtered_onset_frames = get_onset_frames(y, sr, pitches, magnitudes)

      # print librosa.frames_to_time(filtered_onset_frames, sr)

      for i in range(0, len(filtered_onset_frames)):
        onset = filtered_onset_frames[i] + onset_offset
        index = magnitudes[:, onset].argmax()
        pitch = pitches[index, onset]
        # duration = detect_duration(magnitudes, index, onset)
        if (pitch != 0):
          result_pitches.append(pitch)

  elif method == 'autocorr':
    slices = segment_signal(y, sr, pitches, magnitudes)
    for segment in slices:
      pitch = freq_from_autocorr(segment, sr)
      result_pitches.append(pitch)

  return result_pitches

# THIS NEEDS TESTING AND COMMENTS.
def filter_onset_frames(pitches, magnitudes, onset_frames, ampl_thresh=8):

  # print "Before STEP 1:"
  # print librosa.frames_to_time(onset_frames, 40000)
  # STEP 1: Apply threshold:
  onset_frames = [onset for onset in onset_frames
    if magnitudes[:, onset].max() > ampl_thresh]

  # print "After STEP 1:"
  # print librosa.frames_to_time(onset_frames, 40000)

  # STEP 2: Remove dense onsets:
  onset_frames = remove_dense_onsets(onset_frames)
  # print "After STEP 2:"
  # print librosa.frames_to_time(onset_frames, 40000)

  # STEP 3: When an onset time is after an onset time of the same note with
  # a greater magnitude, then it is ignored.
  prev_pitch = 0
  prev_magnitude = 0

  final_filtered_onset_frames = []

  for i in range(0, len(onset_frames)):
    onset = onset_frames[i]
    index = magnitudes[:, onset].argmax()
    magnitude = magnitudes[index, onset]
    pitch = pitches[index, onset]
    # print "({}, {})".format(get_note(pitch), magnitude)
    
    if magnitude < prev_magnitude and get_note(pitch) == get_note(prev_pitch):
      # print "We deleted:"
      # print get_note(pitch)
      continue
    
    prev_pitch = pitch
    prev_magnitude = magnitude
    
    final_filtered_onset_frames.append(onset)

  # print "After STEP 3:"
  # print final_filtered_onset_frames
  return final_filtered_onset_frames

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
  # time_start = 0  # seconds
  # time_end = 1  # seconds
  filter_stop_freq = 60  # Hz
  filter_pass_freq = 80  # Hz
  filter_order = 1001

  # High-pass filter
  nyquist_rate = sr / 2.
  desired = (0, 0, 1, 1)
  bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
  filter_coefs = signal.firls(filter_order, bands, desired, nyq=nyquist_rate)

  # Apply high-pass filter
  filtered_audio = signal.filtfilt(filter_coefs, [1], y)

  # Only analyze the audio between time_start and time_end
  # time_seconds = np.arange(filtered_audio.size, dtype=float) / sr
  # audio_to_analyze = filtered_audio[(time_seconds >= time_start) &
  #                                 (time_seconds <= time_end)]

  return filtered_audio

def segment_signal(y, sr, pitches, magnitudes, onset_frames=None):
  if (onset_frames == None):
    onset_frames = get_onset_frames(y, sr, pitches, magnitudes)

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

def get_onset_frames(y, sr, pitches, magnitudes):
  onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
  return filter_onset_frames(pitches, magnitudes, onset_frames)

def remove_dense_onsets(onset_frames):
  indices_to_remove = []

  # Remove onsets that are too close together.
  for i in range(1, len(onset_frames)):
    if onset_frames[i] - onset_frames[i - 1] <= 5:
      # print librosa.frames_to_time(5, 40000)
      indices_to_remove.append(i)

  return np.delete(onset_frames, indices_to_remove)

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

def get_note(pitch):
  return librosa.hz_to_note(pitch)