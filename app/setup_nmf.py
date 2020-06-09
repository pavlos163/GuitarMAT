import os
import app
import librosa
import numpy as np
from util import *

STATIC_FOLDER = app.STATIC_FOLDER
NMF_FOLDER = os.path.join(STATIC_FOLDER, 'audio/nmf/combined/')
NMF_TXT_FOLDER = os.path.join(STATIC_FOLDER, 'nmf_templates/')


def setup_components():
    audio_files = [os.path.join(dp, f) for dp, dn, filenames
                   in os.walk(NMF_FOLDER) for f in filenames]

    for file in audio_files:
        file_dir = file.split("/")
        filename = file_dir[len(file_dir) - 1]
        print(filename)
        create_text_template(file, filename)

    create_matrix()


def create_matrix():
    arrays = [np.loadtxt("static/nmf_templates/E2.txt"), np.loadtxt("static/nmf_templates/F2.txt"),
              np.loadtxt("static/nmf_templates/Fsharp2.txt"), np.loadtxt("static/nmf_templates/G2.txt"),
              np.loadtxt("static/nmf_templates/Gsharp2.txt"), np.loadtxt("static/nmf_templates/A2.txt"),
              np.loadtxt("static/nmf_templates/Asharp2.txt"), np.loadtxt("static/nmf_templates/B2.txt"),
              np.loadtxt("static/nmf_templates/C3.txt"), np.loadtxt("static/nmf_templates/Csharp3.txt"),
              np.loadtxt("static/nmf_templates/D3.txt"), np.loadtxt("static/nmf_templates/Dsharp3.txt"),
              np.loadtxt("static/nmf_templates/E3.txt"), np.loadtxt("static/nmf_templates/F3.txt"),
              np.loadtxt("static/nmf_templates/Fsharp3.txt"), np.loadtxt("static/nmf_templates/G3.txt"),
              np.loadtxt("static/nmf_templates/Gsharp3.txt"), np.loadtxt("static/nmf_templates/A3.txt"),
              np.loadtxt("static/nmf_templates/Asharp3.txt"), np.loadtxt("static/nmf_templates/B3.txt"),
              np.loadtxt("static/nmf_templates/C4.txt"), np.loadtxt("static/nmf_templates/Csharp4.txt"),
              np.loadtxt("static/nmf_templates/D4.txt"), np.loadtxt("static/nmf_templates/Dsharp4.txt"),
              np.loadtxt("static/nmf_templates/E4.txt"), np.loadtxt("static/nmf_templates/F4.txt"),
              np.loadtxt("static/nmf_templates/Fsharp4.txt"), np.loadtxt("static/nmf_templates/G4.txt"),
              np.loadtxt("static/nmf_templates/Gsharp4.txt"), np.loadtxt("static/nmf_templates/A4.txt"),
              np.loadtxt("static/nmf_templates/E2.txt"), np.loadtxt("static/nmf_templates/F2.txt"),
              np.loadtxt("static/nmf_templates/Fsharp2.txt"), np.loadtxt("static/nmf_templates/G2.txt"),
              np.loadtxt("static/nmf_templates/Gsharp2.txt"), np.loadtxt("static/nmf_templates/A2.txt"),
              np.loadtxt("static/nmf_templates/Asharp2.txt"), np.loadtxt("static/nmf_templates/B2.txt"),
              np.loadtxt("static/nmf_templates/C3.txt"), np.loadtxt("static/nmf_templates/Csharp3.txt"),
              np.loadtxt("static/nmf_templates/D3.txt"), np.loadtxt("static/nmf_templates/Dsharp3.txt"),
              np.loadtxt("static/nmf_templates/E3.txt"), np.loadtxt("static/nmf_templates/F3.txt"),
              np.loadtxt("static/nmf_templates/Fsharp3.txt"), np.loadtxt("static/nmf_templates/G3.txt"),
              np.loadtxt("static/nmf_templates/Gsharp3.txt"), np.loadtxt("static/nmf_templates/A3.txt"),
              np.loadtxt("static/nmf_templates/Asharp3.txt"), np.loadtxt("static/nmf_templates/B3.txt"),
              np.loadtxt("static/nmf_templates/C4.txt"), np.loadtxt("static/nmf_templates/Csharp4.txt"),
              np.loadtxt("static/nmf_templates/D4.txt"), np.loadtxt("static/nmf_templates/Dsharp4.txt"),
              np.loadtxt("static/nmf_templates/E4.txt"), np.loadtxt("static/nmf_templates/F4.txt"),
              np.loadtxt("static/nmf_templates/Fsharp4.txt"), np.loadtxt("static/nmf_templates/G4.txt"),
              np.loadtxt("static/nmf_templates/Gsharp4.txt"), np.loadtxt("static/nmf_templates/A4.txt")]

    newW = np.column_stack(arrays)

    np.savetxt(STATIC_FOLDER + "W.txt", newW)


def create_text_template(file_dir, filename):
    sr = 44100
    y, sr = librosa.load(file_dir, sr=sr)

    D = np.abs(librosa.core.stft(y))

    W, H = librosa.decompose.decompose(D, n_components=1)
    save_file = NMF_TXT_FOLDER + filename[:-4] + ".txt"
    print(save_file)
    np.savetxt(save_file, W[:, 0])


if __name__ == "__main__":
    setup_components()
