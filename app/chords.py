import librosa
import matplotlib.pyplot as plt
import numpy as np
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor, CNNChordFeatureProcessor, CRFChordRecognitionProcessor
from librosa.core import time_to_frames, frames_to_time

def get_chords(filename, y, sr):
  dcp = DeepChromaProcessor()
  decode = DeepChromaChordRecognitionProcessor()
  chroma = dcp(filename)
  chords = decode(chroma)

  # print chords

  chord_tuples = get_chord_tuples(chords, sr)
  # print chord_tuples

  # Very similar results with the CNN:
  # featproc = CNNChordFeatureProcessor()
  # decode = CRFChordRecognitionProcessor()
  # feats = featproc(filename)
  # print(decode(feats))

  chroma = librosa.feature.chroma_stft(y=y, sr=sr)

  # plt.figure(figsize=(10, 4))
  # librosa.display.specshow(chroma, y_axis='chroma', x_axis='frames')
  # plt.colorbar()
  # plt.title('Chromagram')
  # plt.tight_layout()
  # plt.show()

  D = librosa.stft(y)

  for c in chord_tuples:
    frame_start = c[0]
    frame_end = c[1]

    print D[:, frame_start:frame_end]

    print "VAR:"
    print np.var(D[:, frame_start:frame_end])
    print "MEAN:"
    print np.mean(chroma[:, frame_start:frame_end])

    # print chroma[:, frame_start:frame_end]
    #print "VAR:"
    #print np.var(chroma[:, frame_start:frame_end])
    #print "MEAN:"
    #print np.mean(chroma[:, frame_start:frame_end])




  return chords

def get_chord_tuples(chords, sr):
  chord_tuples = []
  for chord in chords:
    if chord[2] != 'N':
      chord_tuples.append((time_to_frames(chord[0], sr)[0], 
        time_to_frames(chord[1], sr)[0]))
  return chord_tuples