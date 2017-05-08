import librosa.display
import numpy as np
import matplotlib.pylab as plt

def plot_waveform(vector):
  plt.figure()
  plt.plot(vector)
  plt.title('Waveform')
  plt.xlabel('Time')
  plt.ylabel('Amplitude')
  plt.tight_layout()
  plt.savefig('static/plots/' + 'audio.png')

def plot_spectrogram(stft_output, xlabel='Time', ylabel='Hz'):
  plt.figure()
  librosa.display.specshow(librosa.amplitude_to_db(stft_output, 
    ref=np.max), y_axis='log', x_axis='time')
  plt.title('Power Spectrogram')
  plt.colorbar(format='%+2.0f dB')
  plt.tight_layout()
  plt.savefig('static/plots/' + 'spectrogram.png')