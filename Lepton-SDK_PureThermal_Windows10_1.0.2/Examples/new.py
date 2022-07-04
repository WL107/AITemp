import clr # needs the "pythonnet" package
import sys
import os
import time

# check whether python is running as 64bit or 32bit
# to import the right .NET dll
import platform
bits, name = platform.architecture()

if bits == "64bit":
	folder = ["x64"]
else:
	folder = ["x86"]

sys.path.append(os.path.join("..", *folder))

clr.AddReference("ManagedIR16Filters")
from IR16Filters import IR16Capture, NewIR16FrameEvent, NewBytesFrameEvent

import numpy
from matplotlib import pyplot as plt
# %matplotlib inline is Jupyter magic to display plot results inline in the 
# notebook
%matplotlib inline

capture = None

from collections import deque

# change maxlen to control the number of frames of history we want to keep
incoming_frames = deque(maxlen=10)
def got_a_frame(short_array, width, height):
    incoming_frames.append((height, width, short_array))

if capture != None:
    # don't recreate capture if we already made one
    capture.RunGraph()
else:
    capture = IR16Capture()
    capture.SetupGraphWithBytesCallback(NewBytesFrameEvent(got_a_frame))
    capture.RunGraph()
	
capture.StopGraph()

def short_array_to_numpy(height, width, frame):
    return numpy.fromiter(frame, dtype="uint16").reshape(height, width)

from matplotlib import cm

height, width, net_array = incoming_frames[-1]
arr = short_array_to_numpy(height, width, net_array)
plt.imshow(arr, cmap=cm.plasma)

#arr.set_printoptions(threshold=arr.inf)
#arr.set_printoptions((threshold=arr.inf, suppress= True)
#arr.set_printoptions(threshold=19200)
#numpy.set_printoptions(threshold=sys.maxsize)
numpy.set_printoptions(threshold=10)
print(arr)
#f = open ('python.txt' , 'w')
#f.write(arr)
#f.close()

height, width, net_array = incoming_frames[-1]
arr = short_array_to_numpy(height, width, net_array)
print(net_array)
def centikelvin_to_celsius(t):
    return (t - 27315) / 100

def to_fahrenheit(ck):
    c = centikelvin_to_celsius(ck)
    return c * 9 / 5 + 32

# get the max image temp
print("maximum temp {:.2f} ºF / {:.2f} ºC".format(
    to_fahrenheit(arr.max()), centikelvin_to_celsius(arr.max())))
# get the average image temp
print("average temp {:.2f} ºF / {:.2f} ºC".format(
    to_fahrenheit(arr.mean()), centikelvin_to_celsius(arr.mean())))