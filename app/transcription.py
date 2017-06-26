import librosa
from music21 import *
from onset import get_onset_frames
from single_pitch import get_mono_notes
from multi_pitch import get_poly_notes
from duration import get_durations
from util import *
from filter import *

def transcribe(filename, static_folder):
  sr = 44100
  environment.set('musicxmlPath', '/usr/bin/musescore')

  y, sr = librosa.load(filename, sr=sr)

  onset_frames = get_onset_frames(filename)

  # Get tempo and durations.
  bpm = get_tempo(y)

  durations = get_durations(onset_frames, bpm)
  print durations

  # Monophonic transcription:
  notes = get_mono_notes(y, sr, onset_frames, 'autocorr')
  
  # Polyphonic transcription:
  # notes = get_poly_notes(y, sr, onset_frames, static_folder)

  # Convert to Music21 stream and export to MusicXML file.
  score = get_score(notes, durations, bpm)

  score.write("musicxml", "static/piece.mxl")
  
  return notes

def get_score(notes, durations, bpm):
  score = stream.Score()
  score.insert(0, clef.Treble8vbClef())
  score.insert(0, tempo.MetronomeMark(number=bpm))
  score.insert(instrument.Guitar())
  for i in range(0, len(notes)):
    if len(notes[i]) == 1:
      if notes[i][0] == 'INV':
        continue
      f = note.Note(notes[i][0])
      f.duration = duration.Duration(durations[i])
      score.append(f)
    else:
      # TODO: Do INV for here as well.
      ch = chord.Chord(notes[i])
      ch.duration = duration.Duration(durations[i])
      score.append(ch)

  return score