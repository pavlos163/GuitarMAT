import essentia
import essentia.standard as ess
from scipy.signal import butter, sosfilt, firls, filtfilt, medfilt


def bandpass_filter(y, sr, lowcut, highcut, filter_order=3):
    # Setup parameters.
    nyquist_rate = sr / 2.
    normalized_low = lowcut / nyquist_rate
    normalized_high = highcut / nyquist_rate

    sos = butter(filter_order, [normalized_low, normalized_high],
                 btype='bandpass', output='sos')

    y = sosfilt(sos, y)
    return y


def highpass_filter(y, sr):
    filter_stop_freq = 60  # Hz
    filter_pass_freq = 80  # Hz
    filter_order = 1001

    # High-pass filter
    nyquist_rate = sr / 2.
    desired = (0, 0, 1, 1)
    bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
    filter_coefs = firls(filter_order, bands, desired, nyq=nyquist_rate)

    # Apply high-pass filter
    filtered_audio = filtfilt(filter_coefs, [1], y)

    return filtered_audio


def remove_noise(y):
    moving_average = ess.MovingAverage()
    ma_y = moving_average(essentia.array(y))

    filtered_y = y - ma_y
    return filtered_y


def medfilt_spectrogram(D):
    for frame in range(0, D.shape[1]):
        mf = medfilt(D[:, frame])
        vec = D[:, frame] - mf
        spectrum = vec.clip(min=0)
        D[:, frame] = spectrum

    return D
