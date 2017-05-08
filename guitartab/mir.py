import librosa
import plot as plt
from numpy import mean, diff
from matplotlib.mlab import find

def save_plot(filename):
  y, sr = librosa.load(filename, sr=40000)
  
  D = librosa.stft(y)

  onset_frames = librosa.onset.onset_detect(y=y, sr=sr)

  print("ONSET:")
  print(librosa.frames_to_time(onset_frames, sr=sr))

  print(freq_from_crossings(y, 40000))

  plt.plot_waveform(y)
  plt.plot_spectrogram(D)

def zero_crossings(audio, sr):
  indices = find((audio[1:] >= 0) & (audio[:-1] < 0))
  crossings = [i - audio[i] / (audio[i+1] - audio[i]) for i in indices]
  return sr / mean(diff(crossings))