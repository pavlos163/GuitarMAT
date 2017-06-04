import app
import os
import itertools
import difflib
from transcription import transcribe
from util import remove_values_from_list

APP_ROOT = app.APP_ROOT
AUDIO_FOLDER = os.path.join(APP_ROOT, 'static/audio/')

def eval():
  scores = []

  scores.append(get_score('Guitar.ff.sulA.C4E4.mp3', 
    [['C4'], ['C#4'], ['D4'], ['D#4'], ['E4']]))
  scores.append(get_score('Guitar.ff.sulB.B3.mp3', 
    [['B3']]))
  scores.append(get_score('Guitar.ff.sulB.C4B4.mp3', 
    [['C4'], ['C#4'], ['D4'], ['D#4'], ['E4'], ['F4'], ['F#4'], ['G4'],
    ['G#4'], ['A4'], ['A#4'], ['B4']]))
  scores.append(get_score('Guitar.ff.sulB.C5Gb5.mp3', 
    [['C5'], ['C#5'], ['D5'], ['D#5'], ['E5'], ['F5'], ['F#5']]))
  scores.append(get_score('Guitar.ff.sulD.C4Ab4.mp3', 
    [['C4'], ['C#4'], ['D4'], ['D#4'], ['E4'], ['F4'], ['F#4'],
    ['G4'], ['G#4']]))
  scores.append(get_score('Guitar.ff.sulD.D3B3.mp3', 
    [['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'], 
    ['G3'], ['G#3'], ['A3'], ['A#3'], ['B3']]))
  scores.append(get_score('Guitar.ff.sul_E.E4B4.mp3', 
    [['E4'], ['F4'], ['F#4'], ['G4'], ['G#4'], ['A4'], ['A#4'], ['B4']]))
  scores.append(get_score('Guitar.pp.sulG.C5Db5.mp3', 
    [['C5'], ['C#5']]))
  scores.append(get_score('Guitar.pp.sulG.G3B3.mp3', 
    [['G3'], ['G#3'], ['A3'], ['A#3'], ['B3']]))
  scores.append(get_score('Guitar_ff_sul_E_C5Bb5.mp3', 
    [['C5'], ['C#5'], ['D5'], ['D#5'], ['E5'], ['F5'], ['F#5'], ['G5'],
    ['G#5'], ['A5'], ['A#5']]))
  scores.append(get_score('Guitar_ff_sulE_C3B3.mp3', 
    [['C3'], ['C#3'], ['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'], ['G3'],
    ['G#3'], ['A3'], ['A#3'], ['B3']]))
  scores.append(get_score('Guitar.mf.sulA.A2B2.mp3', 
    [['A2'], ['A#2'], ['B2']]))
  scores.append(get_score('Guitar.mf.sulA.C4E4.mp3', 
    [['C4'], ['C#4'], ['D4'], ['D#4'], ['E4']]))
  scores.append(get_score('Guitar.mf.sulB.B3.mp3', 
    [['B3']]))
  scores.append(get_score('Guitar.ff.sulG.C4B4.mp3', 
    [['C4'], ['C#4'], ['D4'], ['D#4'], ['E4'], ['F4'], ['F#4'], ['G4'],
    ['G#4'], ['A4'], ['A#4'], ['B4']]))
  scores.append(get_score('Guitar.ff.sul_E.E4B4.mp3', 
    [['E4'], ['F4'], ['F#4'], ['G4'],
    ['G#4'], ['A4'], ['A#4'], ['B4']]))
  scores.append(get_score('Guitar.ff.sulG.G3B3.mp3', 
    [['G3'], ['G#3'], ['A3'], ['A#3'], ['B3']]))
  scores.append(get_score('Guitar.ff.sulG.C5Db5.mp3', 
    [['C5'], ['C#5']]))
  scores.append(get_score('1stSTRING.wav', 
    [['E4'], ['F4'], ['F#4'], ['G4'], ['G#4'], 
    ['A4'], ['A#4'], ['B4'], ['C5'], ['C#5'],
    ['D5'], ['D#5'], ['E5'], ['F5'], ['F#5'],
    ['G5'], ['G#5'], ['A5'], ['A#5'], ['B5'],
    ['C6'], ['C#6'], ['E4']]))
  scores.append(get_score('2ndSTRING.wav', 
    [['B3'], ['C4'], ['C#4'], ['D4'], ['D#4'], 
    ['E4'], ['F4'], ['F#4'], ['G4'], ['G#4'],
    ['A4'], ['A#4'], ['B4'], ['C5'], ['C#5'],
    ['D5'], ['D#5'], ['E5'], ['F5'], ['F#5'],
    ['G5'], ['G#5'], ['B3']]))
  scores.append(get_score('3rdSTRING.wav',
    [['G3'], ['G#3'], ['A3'], ['A#3'], ['B3'], 
    ['C4'], ['C#4'], ['D4'], ['D#4'], ['E4'],
    ['F4'], ['F#4'], ['G4'], ['G#4'], ['A4'],
    ['A#4'], ['B4'], ['C5'], ['C#5'], ['D5'],
    ['D#5'], ['E5']]))
  scores.append(get_score('4thSTRING.wav',
    [['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'], 
    ['G3'], ['G#3'], ['A3'], ['A#3'], ['B3'],
    ['C4'], ['C#4'], ['D4'], ['D#4'], ['E4'],
    ['F4'], ['F#4'], ['G4'], ['G#4'], ['A4'],
    ['A#4'], ['B4'], ['D3']]))
  scores.append(get_score('5thSTRING.wav',
    [['A2'], ['A#2'], ['B2'], ['C3'], ['C#3'],
    ['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'],
    ['G3'], ['G#3'], ['A3'], ['A#3'], ['B3'],
    ['C4'], ['C#4'], ['D4'], ['D#4'], ['E4'],
    ['F4'], ['F#4'], ['A2']]))
  scores.append(get_score('6thSTRING.wav',
    [['E2'], ['F2'], ['F#2'], ['G2'], ['G#2'], 
    ['A2'], ['A#2'], ['B2'], ['C3'], ['C#3'],
    ['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'],
    ['G3'], ['G#3'], ['A3'], ['A#3'], ['B3'],
    ['C4'], ['C#4'], ['E2']]))
  scores.append(get_score('softkitty.mp3',
    [['D4'], ['B3'], ['B3'], ['C4'], ['A3'], ['A3'],
    ['G3'], ['A3'], ['B3'], ['C4'], ['D4'], ['D4'],
    ['D4'], ['B3'], ['B3'], ['C4'], ['C4'], ['A3'],
    ['A3'], ['G3'], ['A3'], ['G3']]))
  # scores.append(get_score('cmajor.wav',
  #   [['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'], 
  #   ['G3'], ['G#3'], ['A3'], ['A#3'], ['B3']]))

  print "Average score:"
  scores = remove_values_from_list(scores, -1)
  print sum(scores) / float(len(scores))

def get_score(filename, correct):
  print filename
  result = transcribe(AUDIO_FOLDER + filename)
  s = difflib.SequenceMatcher(None, flatten(result), flatten(correct))
  if len(result) != len(correct):
    print "Onset mistake, ignoring."
    return -1
  score = s.ratio()
  if score != 1.:
    print "Correct was:\n{} but found:\n{}".format(correct, result)
  print "Score: {}".format(score)
  return score

def flatten(l):
  return list(itertools.chain.from_iterable(l))

if __name__ == "__main__":
  eval()
