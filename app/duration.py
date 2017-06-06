from librosa.core import frames_to_time

def get_durations(onset_frames, tempo):
  abs_durations = get_diff_succesive_onsets(onset_frames)

  # print frames_to_time(abs_durations, 44100)

  if len(onset_frames) == 1:
    return [4.]

  rel_durations_min = normalize(abs_durations, min(abs_durations))

  n = 0
  sum = 0

  for i in range(0, len(abs_durations)):
    if rel_durations_min[i] == 1.:
      sum += abs_durations[i]
      n += 1
  
  min_avg = sum / float(n)

  # print "Min_Avg: {}".format(frames_to_time(min_avg, 44100))

  rel_durations_min_avg = normalize(abs_durations, min_avg)

  quarter = 60 / float(tempo)
  # print "Quarter: {}".format(quarter)

  ratio = round(quarter / float(frames_to_time(min_avg, 44100)))
  # print "Ratio: {}".format(ratio)

  durations = [dur / float(ratio) for dur in rel_durations_min_avg]

  # print durations

  return durations

def get_diff_succesive_onsets(onset_frames):
  abs_durations = []

  for i in range(0, len(onset_frames) - 1):
    abs_durations.append(onset_frames[i + 1] - onset_frames[i])
  abs_durations.append(max(abs_durations))

  return abs_durations

def normalize(durations, refnote):
  durations = [round(float(x) / float(refnote)) for x in durations]
  return durations