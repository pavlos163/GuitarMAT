import librosa
import numpy as np
import madmom.features.onsets as madmom
from librosa.core import hz_to_note, time_to_frames
from madmom.audio.filters import LogarithmicFilterbank

def get_onset_frames(filename, sr):
  proc = madmom.OnsetPeakPickingProcessor(fps=300, threshold=10, pre_max=1. / 300., post_max=1)

  sodf = madmom.SpectralOnsetProcessor(onset_method='superflux', fps=300,
    filterbank=LogarithmicFilterbank, num_bands=24, log=np.log10)(filename)

  return time_to_frames(proc(sodf), sr)

# This is not used anymore, as superflux proved to be more accurate.
def detect_onset_frames(y, sr, pitches, magnitudes):
  onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
  return filter_onset_frames(pitches, magnitudes, onset_frames)

# THIS NEEDS TESTING AND COMMENTS.
def filter_onset_frames(pitches, magnitudes, onset_frames, ampl_thresh=8):
  print "Before STEP 1:"
  print librosa.frames_to_time(onset_frames, 44100)
  # STEP 1: Apply threshold:
  onset_frames = [onset for onset in onset_frames
    if magnitudes[:, onset].max() > ampl_thresh]

  print "After STEP 1:"
  print librosa.frames_to_time(onset_frames, 44100)

  # STEP 2: Remove dense onsets:
  onset_frames = remove_dense_onsets(onset_frames)
  print "After STEP 2:"
  print librosa.frames_to_time(onset_frames, 44100)

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
    
    if magnitude < prev_magnitude and hz_to_note(pitch) == hz_to_note(prev_pitch):
      continue
    
    prev_pitch = pitch
    prev_magnitude = magnitude
    
    final_filtered_onset_frames.append(onset)

  print "After STEP 3:"
  print librosa.frames_to_time(final_filtered_onset_frames, 44100)
  return final_filtered_onset_frames

def remove_dense_onsets(onset_frames):
  indices_to_remove = []

  # Remove onsets that are too close together.
  for i in range(1, len(onset_frames)):
    if onset_frames[i] - onset_frames[i - 1] <= 5:
      indices_to_remove.append(i)

  return np.delete(onset_frames, indices_to_remove)