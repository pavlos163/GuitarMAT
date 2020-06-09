import librosa
import numpy as np
import peakutils
from filter import medfilt_spectrogram
from single_pitch import get_mono_notes
from sklearn.decomposition import non_negative_factorization
from util import *


def get_poly_notes(y, sr, onset_frames, static_folder=None):
    newW = np.loadtxt(static_folder + "W.txt")

    # Get filtered, transposed spectrogram.
    D = get_nmf_spectrogram(y)
    # D = np.abs(librosa.core.stft(y)).T

    n_components = newW.shape[1]

    # Decompose spectrogram.
    W, H, n_iter = non_negative_factorization(D, n_components=n_components,
                                              init='custom', random_state=0, update_H=False, H=newW.T)

    activations = W.T

    notes_at_onsets = get_notes_at_onsets(activations, onset_frames)

    for key in sorted(notes_at_onsets):
        print("At {}: {}".format(key, notes_at_onsets[key]))

    # If there are onsets without a pitch in the dict, get single pitch.
    for key, value in notes_at_onsets.iteritems():
        if len(value) == 0:
            note = get_mono_notes(y, sr, [key], 'autocorr')[0][0]
            notes_at_onsets[key].append(note)

    # Get the sorted (with respect to time) list of notes played.
    notes = get_sorted_notes(notes_at_onsets)

    return notes


def get_notes_at_onsets(activations, onset_frames):
    n_components = activations.shape[0]

    # Initialize list for onsets in onset_frames.
    notes_at_onsets = dict()
    for o in onset_frames:
        notes_at_onsets[o] = []

    # Combined: 0.6, 0.35, 15
    # Real: 0.7, 0.4, 15: 53.7

    for comp in range(n_components):
        print(nmf_component_to_note(comp))
        note = nmf_component_to_note(comp)
        # Get indices of peaks (onsets) based on relative threshold.
        indices = peakutils.indexes(activations[comp], thres=0.95, min_dist=0)
        print("Original: {}".format(indices))
        for i in indices:
            print("Strength: {}".format(activations[comp, i]))
            print("Strength in neighbours: {}".format(sum(activations[comp, i - 10:i + 10])))
        # Filter by absolute threshold as well.
        filtered_indices = [i for i in indices if activations[comp, i] > 0.05]
        print("Filtered: {}".format(filtered_indices))
        # For each found peak, find its closest onset based on the onset_frames.
        # If it close enough, then add it to our dict.
        for onset in filtered_indices:
            closest_onset = min(notes_at_onsets.keys(), key=lambda k: abs(k - onset))
            if abs(onset - closest_onset) < 15:
                notes_at_onsets[closest_onset].append(note)

    return notes_at_onsets


def get_sorted_notes(notes_at_onsets):
    notes = []
    print(sorted(notes_at_onsets))
    for key in sorted(notes_at_onsets):
        notes.append(notes_at_onsets[key])

    return notes


# Returns the transposed filtered spectogram of y.
def get_nmf_spectrogram(y):
    return medfilt_spectrogram(np.abs(librosa.core.stft(y))).T
