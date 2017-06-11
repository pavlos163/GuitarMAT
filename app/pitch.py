import librosa
import numpy as np
import peakutils
import essentia
import essentia.standard as ess
from librosa.core import frames_to_time
from scipy.signal import kaiser, fftconvolve
from util import remove_values_from_list

# Checking the pitch some frames the onset time increased precision.
def get_pitches(y, sr, onset_frames, method='autocorr', stft_offset=5, fmin=80, fmax=4000):
  result_pitches = []

  pitches, magnitudes = librosa.piptrack(y=y, 
    sr=sr, fmin=fmin, fmax=fmax)

  if method == 'stft':
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

  elif method == 'min_stft':

    # Getting the first N peaks. Choose the minimum one in terms of frequency.
    candidates = get_peaks(pitches, magnitudes, onset_frames, stft_offset)
    # print candidates
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

  elif method == 'klapuri':
    klap = ess.MultiPitchMelodia(hopSize=512)
    pitches = klap(essentia.array(y))
    print "Onset frames:"
    print onset_frames
    print "Length of pitches:"
    print len(pitches)
    print "Whole list of pitches:"
    print pitches
    for i in range(0, len(onset_frames)):
      onset = onset_frames[i]
      print onset
      pitches_at_onset = pitches[onset]
      #if (i < len(onset_frames) - 1):
      #  next_onset = onset_frames[i+1] * 4
      #else:
      #  next_onset = librosa.core.samples_to_frames(len(y) - 1) * 4 - 1


      #print "Onset at: {}".format(onset)
      #for j in range(onset, next_onset - 10):
      #  print "j: {}".format(j)
      #  print "len(pitches): {}".format(len(pitches))
      #  pitches_at_onset = pitches[j]
      #  print "at {}: {}".format(j, pitches_at_onset)
      result_pitches.append(pitches_at_onset[0])
      print pitches_at_onset
      print librosa.core.hz_to_note(pitches_at_onset)

  return result_pitches

# For each note played, get the n strongest peaks in the frequency spectrum.
def get_peaks(pitches, magnitudes, onset_frames, offset, n=4):
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

def segment_signal(y, sr, onset_frames, from_minima=False, offset_start=0.05,
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
    slice *= kaiser(N, 100)

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

    while i_peak.size == 0:
        thres -= 0.02
        i_peak = peakutils.indexes(corr, thres=thres, min_dist=5)

    i_peak = i_peak[0]

    # Is interpolation needed?

    return sr / i_peak