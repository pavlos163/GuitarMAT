def get_durations(onset_frames):
  if len(onset_frames) == 1:
    return [4.]

  abs_durations = []
  for i in range(0, len(onset_frames) - 1):
    abs_durations.append(onset_frames[i + 1] - onset_frames[i])
  abs_durations.append(max(abs_durations))

  rel_durations_min = normalize(abs_durations, min(abs_durations))

  n = 0
  sum = 0

  for i in range(0, len(abs_durations)):
    if rel_durations_min[i] == 1.:
      sum += abs_durations[i]
      n += 1
  
  min_avg = sum / float(n)

  rel_durations_min_avg = normalize(abs_durations, min_avg)

  durations = rel_time_to_durations(rel_durations_min_avg)

  return rel_durations_min_avg

def normalize(durations, refnote):
  durations = [round(float(x) / float(refnote)) for x in durations]
  return durations

def rel_time_to_durations(time_durations):
  durations = []
  for t in time_durations:
    if t == 1.:
      durations.append('quarter')
    elif t == 2.:
      durations.append('half')