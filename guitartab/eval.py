import app
import mir
import os

APP_ROOT = app.APP_ROOT
AUDIO_FOLDER = os.path.join(APP_ROOT, 'static/audio/')

def eval():
  scores = []

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.ff.sulA.C4E4.mp3')
  correct = [['C4'], ['C#4'], ['D4'], ['D#4'], ['E4']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.ff.sulB.B3.mp3')
  correct = [['B3']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.ff.sulB.C4B4.mp3')
  correct = [
    ['C4'], ['C#4'], ['D4'], ['D#4'], ['E4'], ['F4'], ['F#4'], ['G4'],
    ['G#4'], ['A4'], ['A#4'], ['B4']
  ]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.ff.sulB.C5Gb5.mp3')
  correct = [['C5'], ['C#5'], ['D5'], ['D#5'], ['E5'], ['F5'], ['F#5']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.ff.sulD.C4Ab4.mp3')
  correct = [['C4'], ['C#4'], ['D4'], ['D#4'], ['E4'], ['F4'], ['F#4'],
    ['G4'], ['G#4']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.ff.sulD.D3B3.mp3')
  correct = [['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'], 
    ['G3'], ['G#3'], ['A3'], ['A#3'], ['B3']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.ff.sul_E.E4B4.mp3')
  correct = [['E4'], ['F4'], ['F#4'], ['G4'], ['G#4'], ['A4'], ['A#4'], ['B4']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.pp.sulG.C5Db5.mp3')
  correct = [['C5'], ['C#5']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar.pp.sulG.G3B3.mp3')
  correct = [['G3'], ['G#3'], ['A3'], ['A#3'], ['B3']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar_ff_sul_E_C5Bb5.mp3')
  correct = [['C5'], ['C#5'], ['D5'], ['D#5'], ['E5'], ['F5'], ['F#5'], ['G5'],
    ['G#5'], ['A5'], ['A#5']]
  scores.append(compare_arrays(result, correct))

  result = mir.transcribe(AUDIO_FOLDER + 'Guitar_ff_sulE_C3B3.mp3')
  correct = [
    ['C3'], ['C#3'], ['D3'], ['D#3'], ['E3'], ['F3'], ['F#3'], ['G3'],
    ['G#3'], ['A3'], ['A#3'], ['B3']
  ]
  scores.append(compare_arrays(result, correct))

  print "Average score:"
  print sum(scores) / float(len(scores))


def compare_arrays(result, correct):
  # TODO: This could be way better.
  if len(result) != len(correct):
    print result
    print correct
    print "Fix onset algorithm"
    return 0
  else:
    sum = 0
    for i in range(0, len(result)):
      if result[i] == correct[i]:
        sum += 1
  return float(sum) / float(len(result))


if __name__ == "__main__":
  eval()

