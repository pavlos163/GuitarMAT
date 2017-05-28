import app
import onset
import os

APP_ROOT = app.APP_ROOT
AUDIO_FOLDER = os.path.join(APP_ROOT, 'static/audio/')

# Wrong results in onsets:
# [['C4'], ['C#4'], ['D4'], ['D#4'], ['E4']]
# [['A2'], ['A#2'], ['B2']]
# [['G3'], ['G#3'], ['A3'], ['A#3'], ['B3']]
# [['C5'], ['C#5']]
# [['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'], ['G3'], ['G#3'], ['A3'], ['A#3'], ['B3']]
# Giorgos recordings: 6 strings 100%

def eval():
  scores = []

  scores.append(get_score('Guitar.ff.sulA.C4E4.mp3', 5))
  scores.append(get_score('Guitar.ff.sulB.B3.mp3', 1))
  scores.append(get_score('Guitar.ff.sulB.C4B4.mp3', 12))
  scores.append(get_score('Guitar.ff.sulB.C5Gb5.mp3', 7))
  scores.append(get_score('Guitar.ff.sulD.C4Ab4.mp3', 9))
  scores.append(get_score('Guitar.ff.sulD.D3B3.mp3', 10))
  scores.append(get_score('Guitar.ff.sul_E.E4B4.mp3', 8))
  scores.append(get_score('Guitar.pp.sulG.C5Db5.mp3', 2))
  scores.append(get_score('Guitar.pp.sulG.G3B3.mp3', 5))
  scores.append(get_score('Guitar_ff_sul_E_C5Bb5.mp3', 11))
  scores.append(get_score('Guitar_ff_sulE_C3B3.mp3', 12))
  scores.append(get_score('Guitar.mf.sulA.A2B2.mp3', 3))
  scores.append(get_score('Guitar.mf.sulA.C4E4.mp3', 5))
  scores.append(get_score('Guitar.mf.sulB.B3.mp3', 1))
  scores.append(get_score('Guitar.ff.sulG.C4B4.mp3', 12))
  scores.append(get_score('Guitar.ff.sul_E.E4B4.mp3', 8))
  scores.append(get_score('Guitar.ff.sulG.G3B3.mp3', 5))
  scores.append(get_score('Guitar.ff.sulG.C5Db5.mp3', 2))
  scores.append(get_score('1stSTRING.wav', 23))
  scores.append(get_score('2ndSTRING.wav', 23))
  scores.append(get_score('3rdSTRING.wav', 22))
  scores.append(get_score('4thSTRING.wav', 23))
  scores.append(get_score('5thSTRING.wav', 24))
  scores.append(get_score('6thSTRING.wav', 23))

  print "Average error:"
  print sum(scores) / float(len(scores))

def get_score(filename, correct):
  result = len(onset.get_onset_frames(AUDIO_FOLDER + filename))
  error = abs(float(correct) - float(result)) / correct
  if error != 0:
    print "In {}:".format(filename)
    print "Correct was {} but found {}".format(correct, result)
    print "Error: {}".format(error)
  return error

# TODO: eval_onset

if __name__ == "__main__":
  eval()
