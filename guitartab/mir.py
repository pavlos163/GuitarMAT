import librosa
import numpy
import plot as plt

def save_plot(filename):
    y, sr = librosa.load(filename)
    plt.plot(y, 'audio', 'time', 'amplitude')