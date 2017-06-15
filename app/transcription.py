import librosa
import librosa.display
import matplotlib.pyplot as plt
import essentia
import essentia.standard as ess
import numpy as np
import peakutils
from music21 import *
from librosa.core import hz_to_note, time_to_frames, frames_to_time
from onset import get_onset_frames
from pitch import get_pitches
from chords import get_chords
from duration import get_durations
from sklearn.decomposition import NMF, non_negative_factorization
from sklearn.preprocessing import normalize
from filter import *
from scipy.signal import medfilt
from util import *

def transcribe(filename):
  sr = 44100
  environment.set('musicxmlPath', '/usr/bin/musescore')

  y, sr = librosa.load(filename, sr=sr)

  onset_frames = get_onset_frames(filename)

  notes_at_onsets = nmf(y, sr, onset_frames)
  notes = []

  for tup in sorted(notes_at_onsets.items()):
    print tup
    print "New onset."

    tup_notes = []
    for comp in tup[1]:
      tup_notes.append(component_to_note(comp))

    notes.append(tup_notes)

  # Get tempo, key and durations.
  tempo = get_tempo(y)
  key = get_key(y)
  # durations = get_durations(onset_frames, tempo)

  # Filter the signal.
  filtered_y = bandpass_filter(y, sr, 80., 4000.)

  # Single pitch detection.
  #pitches = get_pitches(filtered_y, sr, onset_frames, 'autocorr')
  #notes = pitches_to_notes(pitches)

  # Convert to Music21 stream and export to MusicXML file.
  score = get_score(notes, tempo, multi=True)

  score.write("musicxml", "static/piece.mxl")

  # plot_waveform(filtered_y)
  # plot_spectrogram(librosa.stft(filtered_y), sr)
  plt.close('all')
  
  return notes

def get_score(notes, quarter_length, durations=None, multi=True):
  score = stream.Score()
  score.insert(0, clef.Treble8vbClef())
  # Time Signature
  # Key Signature
  score.insert(instrument.Guitar())
  score.insert(0, tempo.MetronomeMark(number=quarter_length))
  if multi:
    # TODO: Durations in multi-pitch.
    for i in range(0, len(notes)):
      if len(notes[i]) == 1:
        f = note.Note(notes[i][0])
        score.append(f)
      else:
        ch = chord.Chord(notes[i])
        score.append(ch)
  else:
    notes = sum(notes, [])
    for i in range(0, len(notes)):
      f = note.Note(notes[i])
      f.duration = duration.Duration(durations[i])
      score.append(f)

  return score

def get_tempo(y):
  tempo_estimator = ess.PercivalBpmEstimator()
  bpm = tempo_estimator(y)
  bpm = round_to_base(bpm, 5)
  if bpm < 60:
    bpm = bpm * 2
  elif bpm > 220:
    bpm = round_to_base(bpm / 2, 5)
  return bpm

def get_key(y):
  key_extractor = ess.KeyExtractor()
  key = key_extractor(essentia.array(y))
  return key

def nmf(y, sr, onset_frames):
  newW = np.loadtxt("newW.txt")

  fixed_H = newW.T

  D = np.abs(librosa.core.stft(y)).T

  for row in range(0, len(D)):
    mf = medfilt(D[row])
    vec = D[row] - mf
    spectrum = vec.clip(min=0)
    D[row] = spectrum

  n_components = newW.shape[1]

  W, H, n_iter = non_negative_factorization(D, n_components=n_components, 
    init='custom', random_state=0, update_H=False, H=fixed_H)

  activations = W.T

  print activations.shape

  print onset_frames

  notes_onsets = dict()
  for o in onset_frames:
    notes_onsets[o] = []

  for n in range(n_components):
    plt.subplot(np.ceil(n_components/2.0), 2, n+1)
    plt.plot(activations[n])
    plt.ylim(0, activations.max())
    plt.xlim(0, activations.shape[1])
    plt.ylabel(component_to_note(n))
    plt.xticks([])
    plt.yticks([])

  plt.show()

  for n in range(n_components):
    plt.subplot(np.ceil(n_components/2.0), 2, n+1)
    plt.plot(fixed_H[n])
    plt.ylim(0, fixed_H.max())
    plt.xlim(0, fixed_H.shape[1])
    plt.ylabel(component_to_note(n))
    plt.xticks([])
    plt.yticks([])

  plt.show()

  for n in range(n_components):
    indexes = peakutils.indexes(activations[n], thres=0.6, min_dist=20)
    print "Component {}: {}".format(n, component_to_note(n))
    print "Component {}: {}".format(n, [activations[n, i] for i in indexes])
    onsets = [i for i in indexes if activations[n, i] > 1]
    print "Onsets: {}".format(onsets)
    for o in onsets:
      for o2 in onset_frames:
        print "o: {}".format(o)
        print "o2: {}".format(o2)
        if np.abs(o - o2) <= 10:
          notes_onsets[o2].append(n)
          break

  return notes_onsets

def get_tuning(spectrum):
    speaks = ess.SpectralPeaks()
    frequencies, magnitudes = speaks(essentia.array(spectrum))

    tuning = ess.TuningFrequency()
    freq, cents = tuning(frequencies, magnitudes)
    print freq
    print cents

def component_to_note(component_number):
  components = {0: "E2",
                1: "F2",
                2: "F#2",
                3: "G2",
                4: "G#2",
                5: "A2",
                6: "A#2",
                7: "B2",
                8: "C3",
                9: "C#3",
                10: "D3",
                11: "D#3",
                12: "E3",
                13: "F3",
                14: "F#3",
                15: "G3",
                16: "G#3",
                17: "A3",
                18: "A#3",
                19: "B3",
                20: "C4",
                21: "C#4",
                22: "D4",
                23: "D#4",
                24: "E4",
                25: "F4",
                26: "F#4",
                27: "G4",
                28: "G#4",
                29: "A4"
  }

  return components[component_number]