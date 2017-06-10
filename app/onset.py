import librosa
import numpy as np
import madmom.audio.signal as ms
import madmom.features.onsets as mo
from librosa.core import hz_to_note, frames_to_time, time_to_frames
from madmom.audio.filters import LogarithmicFilterbank

def get_onset_frames(data, sr):

  sig = ms.Signal(data, sample_rate=sr, num_channels=1,
    norm=True)

  # BEST! Avg. error: 0.009
  sodf = mo.SpectralOnsetProcessor(onset_method='superflux',
    filterbank=LogarithmicFilterbank, num_bands=30, log=np.log10, norm=True)(sig)

  onset_frames = mo.peak_picking(sodf, threshold=20, pre_max=15, post_max=15,
    pre_avg=20, post_avg=20, smooth=15)

  # Onset detection in hard songs will require more bands?
  # proc = madmom.OnsetPeakPickingProcessor(threshold=17)
  # sodf = madmom.SpectralOnsetProcessor(onset_method='superflux',
  #   filterbank=LogarithmicFilterbank, num_bands=250, log=np.log10, norm=True)(filename)

  # proc = madmom.OnsetPeakPickingProcessor(threshold=8, pre_max=1. / 200., post_max=1./ 200)
  # sodf = madmom.SpectralOnsetProcessor(onset_method='complex_flux',
  #   filterbank=LogarithmicFilterbank, num_bands=48, log=np.log10, norm=True)(filename)

  # proc = madmom.OnsetPeakPickingProcessor(threshold=5, pre_max=1. / 300., post_max=0.5)
  # sodf = madmom.SpectralOnsetProcessor(onset_method='spectral_diff',
  #   filterbank=LogarithmicFilterbank, num_bands=100, log=np.log10, norm=True)(filename)

  # Good average error but only for studio-recorded samples.
  # Average error in general is 0.095 but error for recorded samples is often more than 50%.
  # proc = madmom.OnsetPeakPickingProcessor(threshold=0.85, pre_max=1. / 200., 
  # post_max=1. / 200, pre_avg = 0.1, post_avg = 0.1)
  # sodf = madmom.CNNOnsetProcessor(filterbank=LogarithmicFilterbank, 
  #   log=np.log10, norm=True)(filename)

  return frames_to_librosa_frames(onset_frames, sr)

def frames_to_librosa_frames(onset_frames, sr):
  onset_times = [float(x)/100. for x in onset_frames]
  return time_to_frames(onset_times, sr)

# This is not used anymore, as superflux proved to be more accurate.
def detect_onset_frames(y, sr, pitches, magnitudes):
  onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
  return filter_onset_frames(pitches, magnitudes, onset_frames)

# THIS NEEDS TESTING AND COMMENTS.
def filter_onset_frames(pitches, magnitudes, onset_frames, ampl_thresh=8):
  print "Before STEP 1:"
  print librosa.frames_to_time(onset_frames, 44100)
  # STEP 1: Apply threshold:
  onset_frames = filter_amplitude_threshold(onset_frames, magnitudes)

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

def filter_amplitude_threshold(onset_frames, magnitudes, ampl_thresh=1):
  onset_frames = [onset for onset in onset_frames
    if magnitudes[:, onset].max() > ampl_thresh]

  return onset_frames

def remove_dense_onsets(onset_frames):
  indices_to_remove = []

  # Remove onsets that are too close together.
  for i in range(1, len(onset_frames)):
    if onset_frames[i] - onset_frames[i - 1] <= 5:
      indices_to_remove.append(i)

  return np.delete(onset_frames, indices_to_remove)