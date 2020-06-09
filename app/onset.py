import librosa
import madmom.audio.signal as ms
import madmom.features.onsets as mo
import numpy as np
from librosa.core import hz_to_note
from madmom.audio.filters import LogarithmicFilterbank
from util import *


def get_onset_frames(filename):
    sr = 44100
    sig = ms.Signal(filename, sr=sr, num_channels=1,
                    norm=True)

    #######################################
    # SUPERFLUX:
    #######################################
    # Avg. score: 0.954
    # sodf = mo.SpectralOnsetProcessor(onset_method='superflux',
    #  filterbank=LogarithmicFilterbank, num_bands=24, fps=200, log=np.log10,
    #  norm=True)(sig)
    # onset_frames = mo.peak_picking(sodf, threshold=10, pre_max=4, post_max=10,
    #  pre_avg=15, post_avg=15)
    #######################################

    #######################################
    # COMPLEXFLUX:
    #######################################
    # Avg. score = 0.951
    # sodf = mo.SpectralOnsetProcessor(onset_method='complex_flux',
    #  filterbank=LogarithmicFilterbank, num_bands=24, fps=200, log=np.log10,
    #  norm=True)(sig)
    # onset_frames = mo.peak_picking(sodf, threshold=6, pre_max=2, post_max=5,
    #  pre_avg=8, post_avg=8, smooth=19)
    #######################################

    #######################################
    # SPECTRAL DIFF:
    #######################################
    # Avg. score = 0.956
    # sodf = mo.SpectralOnsetProcessor(onset_method='spectral_diff',
    #  filterbank=LogarithmicFilterbank, num_bands=24, fps=200, log=np.log10,
    #  norm=True)(sig)
    # onset_frames = mo.peak_picking(sodf, threshold=6, pre_max=2, post_max=2,
    #  pre_avg=8, post_avg=4, smooth=5)
    #######################################

    #######################################
    # SPECTRAL FLUX:
    #######################################
    # Avg.score = 0.972
    sodf = mo.SpectralOnsetProcessor(onset_method='spectral_flux',
                                     filterbank=LogarithmicFilterbank, num_bands=24, fps=200,
                                     log=np.log10, norm=True)(sig)
    onset_frames = mo.peak_picking(sodf, threshold=14, pre_max=2, post_max=8,
                                   pre_avg=30, post_avg=30, smooth=3)
    #######################################

    #######################################
    # CNN:
    #######################################
    # Avg. error: 0.956
    # sodf = mo.CNNOnsetProcessor(filterbank=LogarithmicFilterbank,
    #  num_bands=24, fps=200, log=np.log10, norm=False)(sig)
    # onset_frames = mo.peak_picking(sodf, threshold=0.999)
    #######################################

    #######################################
    # RNN:
    #######################################
    # Avg. error: 0.824
    # sodf = mo.RNNOnsetProcessor(filterbank=LogarithmicFilterbank, num_bands=24,
    #  fps=200, log=np.log10, norm=True)(sig)
    # onset_frames = mo.peak_picking(sodf, threshold=0.7, pre_max=4, post_max=10,
    #  pre_avg=15, post_avg=0, smooth=20)
    #######################################

    onset_frames = remove_dense_onsets(onset_frames)

    return madmom_frames_to_librosa_frames(onset_frames, sr)


# This is not used anymore, as superflux proved to be more accurate.
def detect_onset_frames(y, sr, pitches, magnitudes):
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    return filter_onset_frames(pitches, magnitudes, onset_frames)


# Deprecated:
def filter_onset_frames(pitches, magnitudes, onset_frames):
    print("Before STEP 1:")
    print(librosa.frames_to_time(onset_frames, 44100))
    # STEP 1: Apply threshold:
    onset_frames = filter_amplitude_threshold(onset_frames, magnitudes)

    print("After STEP 1:")
    print(librosa.frames_to_time(onset_frames, 44100))

    # STEP 2: Remove dense onsets:
    onset_frames = remove_dense_onsets(onset_frames)
    print("After STEP 2:")
    print(librosa.frames_to_time(onset_frames, 44100))

    # STEP 3: When an onset time is after an onset time of the same note with
    # a greater magnitude, then it is ignored.
    prev_pitch = 0
    prev_magnitude = 0

    final_filtered_onset_frames = []

    for i in range(0, len(onset_frames)):
        onset = onset_frames[i]
        index = magnitudes[:, onset].argmax()
        magnitude = magnitudes[index, onset]
        pitch = pitches[index, onset]

        if magnitude < prev_magnitude and hz_to_note(pitch) == hz_to_note(prev_pitch):
            continue

        prev_pitch = pitch
        prev_magnitude = magnitude

        final_filtered_onset_frames.append(onset)

    print("After STEP 3:")
    print(librosa.frames_to_time(final_filtered_onset_frames, 44100))
    return final_filtered_onset_frames


def filter_amplitude_threshold(onset_frames, magnitudes, ampl_thresh=1):
    onset_frames = [onset for onset in onset_frames
                    if magnitudes[:, onset].max() > ampl_thresh]

    return onset_frames


def remove_dense_onsets(onset_frames):
    indices_to_remove = []

    # Remove onsets that are too close together.
    for i in range(1, len(onset_frames)):
        if onset_frames[i] - onset_frames[i - 1] <= 20:
            indices_to_remove.append(i)

    return np.delete(onset_frames, indices_to_remove)
