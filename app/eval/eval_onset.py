## EVALUATION OF THE ONSET DETECTION METHOD (NON-NMF) ##

import sys
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
  sys.path.insert(1, path)
del path

import app
import librosa
from librosa.core import frames_to_time
from onset import get_onset_frames, detect_onset_frames
import filter
import madmom.evaluation.onsets as madeval

APP_ROOT = app.APP_ROOT
AUDIO_FOLDER = os.path.join(APP_ROOT, 'static/audio/dataset')

# TODO: This should be done with recall, precision and f-measure.

def eval():
  eval_objects = []

  eval_objects.append(get_eval(
    'Guitar.ff.sulA.C4E4.mp3',
    [5, 810, 1662, 2205, 2736]))
  eval_objects.append(get_eval(
    'Guitar.ff.sulB.B3.mp3',
    [1]))
  eval_objects.append(get_eval(
    'Guitar.ff.sulB.C4B4.mp3',
    [1, 662, 1206, 1778, 2513, 3175,
     3806, 4543, 5292, 5852, 6453, 6897]))
  eval_objects.append(get_eval(
    'Guitar.ff.sulB.C5Gb5.mp3',
    [2, 433, 941, 1414, 1958, 2413, 2809]))
  eval_objects.append(get_eval(
    'Guitar.ff.sulD.C4Ab4.mp3',
    [0, 708, 1410, 2295, 3074, 3984, 4588,
     5189, 5644]))
  eval_objects.append(get_eval(
    'Guitar.ff.sulD.D3B3.mp3',
    [1, 1720, 3088, 4237, 5190, 5837, 6557,
     7087, 7968, 8675]))
  eval_objects.append(get_eval(
    'Guitar.ff.sul_E.E4B4.mp3',
    [0, 574, 1191, 1810, 2501, 3074, 3737, 4295]))
  eval_objects.append(get_eval(
    'Guitar.pp.sulG.C5Db5.mp3',
    [3, 515]))
  eval_objects.append(get_eval(
    'Guitar.pp.sulG.G3B3.mp3',
    [2, 736, 1487, 2282, 3015]))
  eval_objects.append(get_eval(
    'Guitar_ff_sul_E_C5Bb5.mp3',
    [1, 561, 1120, 1677, 2178, 2781, 3339,
     3869, 4354, 4882, 5486]))
  eval_objects.append(get_eval(
    'Guitar_ff_sulE_C3B3.mp3',
    [2, 748, 1597, 2961, 3832, 4420, 4816, 5596,
     6241, 6809, 7701, 8631]))
  eval_objects.append(get_eval(
    'Guitar.mf.sulA.A2B2.mp3',
    [11, 1079, 2032]))
  eval_objects.append(get_eval(
    'Guitar.mf.sulA.C4E4.mp3',
    [3, 839, 1487, 2192, 2839]))
  eval_objects.append(get_eval(
    'Guitar.mf.sulB.B3.mp3',
    [0]))
  eval_objects.append(get_eval(
    'Guitar.ff.sulG.C4B4.mp3',
    [1, 736, 1646, 2427, 3155, 3947, 4594,
     5219, 5932, 6689, 7410, 8233]))
  eval_objects.append(get_eval(
    'Guitar.ff.sul_E.E4B4.mp3',
    [0, 574, 1191, 1810, 2501, 3074, 3737, 4295]))
  eval_objects.append(get_eval(
    'Guitar.ff.sulG.G3B3.mp3',
    [0, 794, 1485, 2132, 2823]))
  eval_objects.append(get_eval(
    'Guitar.ff.sulG.C5Db5.mp3',
    [0, 604]))
  eval_objects.append(get_eval(
    '1stSTRING.wav',
    [191, 468, 721, 957, 1197, 1433, 1669, 1941, 2189,
     2431, 2669, 2908, 3143, 3390, 3624, 3863, 4107,
     4347, 4588, 4822, 5064, 5295, 5526]))
  eval_objects.append(get_eval(
    '2ndSTRING.wav',
    [195, 409, 630, 841, 1053, 1263, 1475, 1690, 1909,
     2126, 2349, 2562, 2775, 2984, 3198, 3404, 3603,
     3816, 4008, 4208, 4411, 4610, 4816]))
  eval_objects.append(get_eval(
    '3rdSTRING.wav',
    [116, 314, 509, 705, 899, 1103, 1301, 1489, 1683,
     1874, 2070, 2265, 2456, 2650, 2848, 3042, 3231,
     3419, 3596, 3782, 3965, 4146]))
  eval_objects.append(get_eval(
    '4thSTRING.wav',
    [141, 333, 519, 699, 881, 1064, 1252, 1441, 1633,
     1820, 2003, 2183, 2370, 2546, 2732, 2913, 3102,
     3292, 3487, 3670, 3857, 4033, 4219]))
  eval_objects.append(get_eval(
    '5thSTRING.wav',
    [139, 313, 495, 673, 866, 1047, 1230, 1411, 1590,
     1767, 1944, 2125, 2310, 2497, 2686, 2867, 3046,
     3220, 3406, 3586, 3756, 3933, 4123, 4309]))
  eval_objects.append(get_eval(
    '6thSTRING.wav',
    [121, 298, 475, 661, 844, 1028, 1211, 1401, 1590,
     1779, 1965, 2149, 2333, 2515, 2695, 2878, 3060,
     3239, 3422, 3598, 3777, 3974, 4160]))
  eval_objects.append(get_eval(
    '3dsCscale.wav',
    [135, 232, 327, 421, 510, 608, 696, 784, 870,
     953, 1041,1153, 1241, 1322, 1404]))
  eval_objects.append(get_eval(
    'cmajor.wav',
    [188, 235, 279, 321, 363, 405, 449, 489, 531, 572, 612,
     653, 695, 734, 776, 816, 857, 897, 935, 977, 1017,
     1058, 1099, 1139, 1179, 1219, 1258, 1298, 1340, 1431]))
  eval_objects.append(get_eval(
    'echromatic.wav',
    [116, 160, 197, 236, 277, 320, 363, 404, 447, 486, 526,
     566, 605, 645, 684, 722, 762, 800, 842, 883, 923, 960,
     999, 1040, 1077, 1116, 1155, 1193, 1232, 1272, 1311, 1349,
     1386, 1421, 1459, 1496, 1534, 1573, 1609, 1648, 1685, 1722,
     1759, 1793, 1830, 1866, 1901, 1938, 1975, 2011, 2047, 2083,
     2118, 2151, 2186, 2222, 2260]))
  eval_objects.append(get_eval(
    'softkitty.mp3',
    [70, 137, 163, 201, 266, 298, 327, 361, 391, 421, 454, 586,
     618, 651, 676, 713, 745, 777, 809, 841, 912, 978]))
  eval_objects.append(get_eval(
    'unknown.mp3',
    [52, 68, 98, 114, 137, 158, 179, 270, 314, 354, 397, 443, 527,
     573, 596, 616, 634, 655, 677, 697, 785, 829, 871, 913, 959, 1046,
     1089, 1111, 1132, 1151, 1173, 1194, 1216, 1303, 1346, 1387, 1431,
     1474, 1564, 1606, 1627, 1647, 1666, 1686, 1705, 1728, 1770, 1816,
     1855, 1905, 1949, 1995, 2125]))
  eval_objects.append(get_eval(
    'unknown2.mp3',
    [67, 177, 274, 301, 324, 348, 374, 427, 480, 587, 687, 714, 736,
     760, 786, 840, 895, 920, 945, 968, 996, 1021, 1044, 1067, 1099,
     1151, 1204, 1258, 1308, 1334, 1359, 1385, 1409, 1434, 1459, 1484,
     1511, 1564, 1620]))
  eval_objects.append(get_eval(
    'frerejacques.mp3',
    [222, 265, 307, 349, 393, 437, 478, 523, 566, 609, 653, 740, 781,
     824, 910, 934, 953, 974, 995, 1037, 1080, 1105, 1123, 1142, 1165,
     1208, 1252, 1295, 1341, 1426, 1473, 1518]))
  eval_objects.append(get_eval(
    'astatamalakia.mp3',
    [221, 291, 331, 403, 443, 516, 554, 664, 736, 774, 811, 845, 884,
     997, 1109, 1179, 1216, 1290, 1329, 1400, 1440, 1549, 1622, 1661,
     1696, 1731, 1771, 1881, 1918, 1954, 1992, 2067, 2105, 2140, 2176,
     2214, 2288, 2325, 2432, 2510, 2548, 2585, 2618, 2657, 2767, 2880,
     2955, 2992, 3028, 3062, 3102, 3175, 3213, 3319, 3397, 3432, 3467,
     3503, 3540, 3580, 3618, 3655]))
  eval_objects.append(get_eval(
    'eam.mp3',
    [220, 284, 303, 365, 385, 405, 420, 441, 462, 503, 546, 613, 635, 690,
     712, 731, 749, 770, 789, 811, 832, 852, 877, 919, 961, 1003, 1018, 1043,
     1067, 1083, 1104, 1125, 1165, 1232, 1271, 1293, 1356, 1377, 1394, 1413,
     1434, 1453, 1475, 1495, 1515, 1537, 1579, 1621, 1663, 1683, 1703, 1728,
     1745, 1765, 1786, 1827, 1894, 1930, 1952, 2016, 2037, 2056, 2076, 2094,
     2117]))
  eval_objects.append(get_eval(
    'fragkosirianinobass.mp3',
    [114, 130, 146, 168, 202, 220, 256, 275, 308, 326, 358, 378, 409, 428,
     461, 482, 511, 531, 565, 585, 614, 635, 668, 687, 719, 739, 769, 791,
     841, 858, 874, 894, 944, 962, 978, 1000, 1032, 1051, 1083, 1103, 1134,
     1153, 1188, 1208, 1239, 1258, 1289, 1310, 1340, 1361, 1393, 1413, 1446,
     1465, 1496, 1516, 1548, 1566, 1584, 1599, 1621, 1668, 1719]))
  eval_objects.append(get_eval(
    'fragkosiriani.mp3',
    [100, 116, 132, 155, 191, 210, 245, 263, 297, 317, 348, 367, 400, 420, 453,
     472, 503, 525, 558, 577, 610, 632, 667, 685, 717, 738, 770, 790, 842, 859,
     875, 896, 947, 964, 980, 1002, 1037, 1055, 1086, 1105, 1138, 1158, 1189,
     1208, 1241, 1260, 1290, 1310, 1343, 1362, 1395, 1414, 1446, 1468, 1499,
     1518, 1551, 1568, 1586, 1600, 1618, 1670, 1721]))

  mean = madeval.OnsetMeanEvaluation(eval_objects)
  print mean

def get_eval(filename, annotations):
  detections = get_onset_frames(AUDIO_FOLDER + filename)
  
  # print "Onset Frames: {}".format(detections/200.)
  
  print filename

  ev = madeval.OnsetEvaluation(detections, annotations, window=20)
  
  # print [round(frames_to_time(det, 44100)[0], 2) for det in detections]
  # print [round(frames_to_time(ann, 44100)[0], 2) for ann in annotations]

  print ev
  return ev

if __name__ == "__main__":
  eval()
