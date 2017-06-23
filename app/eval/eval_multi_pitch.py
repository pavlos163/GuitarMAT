## EVALUATION OF THE SINGLE PITCH DETECTION METHOD ##

import sys
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
  sys.path.insert(1, path)
del path

import app
import difflib
import librosa
from onset import get_onset_frames
from multi_pitch import get_poly_notes
from util import *

APP_ROOT = app.APP_ROOT
STATIC_FOLDER = app.STATIC_FOLDER
AUDIO_FOLDER = os.path.join(APP_ROOT, 'static/audio/dataset/multi/')

def eval():
  scores = []

  scores.append(get_score('C3G3.wav',
    [156],
    [['C3', 'G3']]))
  scores.append(get_score('C3A3.wav',
    [148],
    [['C3', 'A3']]))
  scores.append(get_score('C3B3.wav',
    [132],
    [['C3', 'B3']]))
  scores.append(get_score('C3E3.wav',
    [196],
    [['C3', 'E3']]))
  scores.append(get_score('C3Asharp3.wav',
    [184],
    [['C3', 'A#3']]))
  scores.append(get_score('C3D4.wav',
    [203],
    [['C3', 'D4']]))
  scores.append(get_score('C3F3.wav',
    [233],
    [['C3', 'F3']]))
  scores.append(get_score('C3C4.wav',
    [181],
    [['C3', 'C4']]))
  scores.append(get_score('C3Csharp4.wav',
    [209],
    [['C3', 'C#4']]))
  #scores.append(get_score(
  #  'fragkosiriani.mp3',
  #  [100, 116, 132, 155, 191, 210, 245, 263, 297, 317, 348, 367, 400, 420, 453,
  #   472, 503, 525, 558, 577, 610, 632, 667, 685, 717, 738, 770, 790, 842, 859,
  #   875, 896, 947, 964, 980, 1002, 1037, 1055, 1086, 1105, 1138, 1158, 1189,
  #   1208, 1241, 1260, 1290, 1310, 1343, 1362, 1395, 1414, 1446, 1468, 1499,
  #   1518, 1551, 1568, 1586, 1600, 1618, 1670, 1721]))
  #scores.append(get_score(
  #  '3dsCscale.wav',
  #  [135, 232, 327, 421, 510, 608, 696, 784, 870,
  #   953, 1041,1153, 1241, 1322, 1404]))

  print "Average score:"
  print sum(scores) / float(len(scores))

def get_score(filename, onset_frames, correct):
  print filename
  y, sr = librosa.load(AUDIO_FOLDER + filename, sr=44100)

  result = get_poly_notes(y, sr, onset_frames, STATIC_FOLDER)

  s = difflib.SequenceMatcher(None, flatten(result), flatten(correct))
  score = s.ratio()
  if score != 1.:
    print "Correct was:\n{} but found:\n{}".format(correct, result)
  print "Score: {}".format(score)
  return score

if __name__ == "__main__":
  eval()