import librosa
import plot as plt

def save_plot(filename):
  y, sr = librosa.load(filename, sr=16000)
  
  D = librosa.stft(y)

  plt.plot_spectrogram(D)