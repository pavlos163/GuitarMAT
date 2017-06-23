import librosa
import numpy as np
import peakutils
import essentia
import essentia.standard as ess
from librosa.core import frames_to_time
from scipy.signal import kaiser, fftconvolve, hanning
from util import *

# Checking the pitch some frames the onset time increased precision.
def get_mono_notes(y, sr, onset_frames, method='autocorr',
  stft_offset=25, fmin=80, fmax=4000):
  result_pitches = []

  pitches, magnitudes = librosa.piptrack(y=y, 
    sr=sr, fmin=fmin, fmax=fmax)

  if method == 'stqifft':
    for i in range(0, len(onset_frames)):
      onset = onset_frames[i] + stft_offset
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

  elif method == 'min_stqifft':
    # Getting the first N peaks. Choose the minimum one in terms of frequency.
    candidates = get_peaks(pitches, magnitudes, onset_frames, stft_offset)
    for c in candidates:
      # chord = is_chord(c)
      pitch = min(c)
      result_pitches.append(pitch)

  elif method == 'yin':
    yin = ess.PitchYin()
    slices = segment_signal(y, sr, onset_frames)
    for slice in slices:
      pitch = yin(essentia.array(slice))
      result_pitches.append(pitch[0])

  return pitches_to_notes(result_pitches)

# For each note played, get the n strongest peaks in the frequency spectrum.
def get_peaks(pitches, magnitudes, onset_frames, offset, n=4):
    print "OFFSET: {}".format(offset)
    candidate_list = []

    for i in range(0, len(onset_frames)):
      candidates = []
      onset = onset_frames[i] + offset
      indices = np.argpartition(magnitudes[:, onset], 0-n)[0-n:]

      for j in indices:
        # print "{} at frame {}: {}".format(pitches[j, onset], onset, magnitudes[j, onset])
        candidates.append(pitches[j, onset])

      candidates = remove_values_from_list(candidates, 0)

      candidate_list.append(candidates)

    return candidate_list

def segment_signal(y, sr, onset_frames, from_minima=False, offset_start=0,
  offset_end=0.2):

  if from_minima:
    # We split the signal into slices that sum up to the whole signal
    # according to onset_bt (from local minima to the next local minima).
    oenv = librosa.onset.onset_strength(y=y, sr=sr)
    onset_bt = librosa.onset.onset_backtrack(onset_frames, oenv)
    new_onset_bt = librosa.frames_to_samples(onset_bt)

    slices = np.split(y, new_onset_bt[1:])

  else:
    # We split the signal into slices that span from peak p + offset_start
    # to p + offset_end.
    offset_start_samples = int(librosa.time_to_samples(offset_start, sr))
    offset_end_samples = int(librosa.time_to_samples(offset_end, sr))

    slices = np.array([y[i + offset_start_samples : i + offset_start_samples +
      offset_end_samples] for i in librosa.frames_to_samples(onset_frames)])

  for slice in slices:
    N = len(slice)
    slice *= kaiser(N, 80)

  return slices

def is_chord(candidate):
  candidate.sort()
  # print candidate

  if len(candidate) == 1:
    return False
  else:
    mid = candidate[1]
    min = candidate[0]
    
    div = mid / min
    inharmonicity_factor = abs(round(div) - div)

    print "MID WITH MIN:"
    print inharmonicity_factor

    if len(candidate) == 3:
      max = candidate[2]
      div = max / min
      print div
      inharmonicity_factor = abs(round(div) - div)

      print "MAX WITH MIN:"
      print inharmonicity_factor

def freq_from_autocorr(y, sr):
  y -= np.mean(y)
  corr = fftconvolve(y, y[::-1], mode='full')
  corr = corr[len(corr)//2:]

  thres = 1.2

  i_peak = peakutils.indexes(corr, thres=thres, min_dist=5)

  # Check for peaks until some greater than 76 and less than 1600 is found.
  while i_peak.size == 0 or all(sr / i <= 78 or sr / i > 1600 for i in i_peak):
    thres -= 0.02
  
    i_peak = peakutils.indexes(corr, thres=thres, min_dist=5)

    if thres < 0:
      return 0
  
  i_peak = [i for i in i_peak if sr / i > 78 and sr / i <= 1600][0]

  # Is interpolation needed?

  return sr / i_peak

def pitches_to_notes(pitches):
  notes = []
  for pitch in pitches:
    if pitch > 1320 or pitch < 75:
      notes.append(['INV'])
    else:
      notes.append(hz_to_note(pitch))
  return notes