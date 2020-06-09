import essentia
import essentia.standard as ess
import librosa
from librosa.core import time_to_frames, frames_to_samples
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor


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
        # frame_start = (c[0] + c[1])//2
        frame_end = frame_start + 5

        print(frame_start)
        print(frame_end)

        sample_start = int(frames_to_samples(frame_start))
        sample_end = int(frames_to_samples(frame_end))

        print(sample_start)
        print(sample_end)

        essspectrum = ess.Spectrum()
        spectrum = essspectrum(essentia.array(y[sample_start:sample_end]))

        print("Salience:")
        sal = ess.PitchSalience()
        print(sal(spectrum))

        print("Spectral Complexity:")
        scompl = ess.SpectralComplexity(magnitudeThreshold=5)
        print(scompl(spectrum))

        # print("Spectral Contrast:")
        # sc = ess.SpectralContrast()
        # print(sc(spectrum))

        # print("VAR:")
        # print(np.var(D[:, frame_start:frame_end]))
        # print("MEAN:")
        # print(np.mean(chroma[:, frame_start:frame_end]))

        # print(chroma[:, frame_start:frame_end])
        # print("VAR:")
        # print(np.var(chroma[:, frame_start:frame_end]))
        # print("MEAN:")
        # print(np.mean(chroma[:, frame_start:frame_end]))

    return chords


def get_chord_tuples(chords, sr):
    chord_tuples = []
    for chord in chords:
        if chord[2] != 'N':
            chord_tuples.append((time_to_frames(chord[0], sr)[0],
                                 time_to_frames(chord[1], sr)[0]))
    return chord_tuples
