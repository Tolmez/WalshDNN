import pyaudio
import wave
import time
import numpy as np
import cv2
from   scipy import signal

FORMAT     = pyaudio.paFloat32					#paInt16		
CHANNEL    = 1
SAMPLEFREQ = 1000
pencere    = 3000		
ratio      = 3

#--------------------------------------------------------------------------------------
#---------- Maass-Weber Firter --------------------------------------------------------
high       = 70.0*2.0/SAMPLEFREQ	
bb, aa     = signal.butter(10, high, btype='high', analog=False)		
#--------------------------------------------------------------------------------------

p          = pyaudio.PyAudio()

data1      = np.zeros(pencere)
signal1    = np.zeros(pencere)
flag1      = 1

#----------- Acquaring sound data in real-time ----------------------------------------
def callback(in_data, frame_count, time_info, status):
    global flag1, signal1, bb, aa 

    signal0 = np.fromstring(in_data, dtype=np.float32)		#"Int16")
    #print(signal0.shape)
    signal1 = signal.lfilter(bb, aa, signal0)
    signal2 = signal1.astype(np.float32).tostring() 
    flag1 = 0
    
    return (signal2, pyaudio.paContinue)
#--------------------------------------------------------------------------------------

#stream = p.open(format=FORMAT,channels=1,rate=SAMPLEFREQ,input=True, frames_per_buffer= pencere, stream_callback=callback)
stream = p.open(format=FORMAT, channels=1, rate=SAMPLEFREQ, input=True, output=True, frames_per_buffer= pencere, stream_callback=callback)

stream.start_stream()

sounddata =[]
img       = np.zeros((256,1+int(pencere/ratio)))

while stream.is_active():

#--------------------------------------------------------------------------------------
#------------ Waiting new sound data --------------------------------------------------
    while(flag1):
        a = 0
    flag1 = 1

    data1 = signal1.copy()
    sounddata.append(data1.copy())
#--------------------------------------------------------------------------------------
#------------ Analysis must be here ---------------------------------------------------





#--------------------------------------------------------------------------------------
#------------ Plot the sound in real-time ---------------------------------------------
    mini  = np.min(data1)
    maksi = np.max(data1)
    data3 = 255.0*(data1[0:pencere:ratio]-mini)/(maksi-mini)
    
    for i in range(0, int(pencere/ratio)-1):
        cv2.line(img, (i, int(data3[i])), (i+1,int(data3[i+1])), (255,255,255), 1)

    img   = img.astype(np.uint8)
    cv2.imshow('Sounds',img)

    for i in range(0, int(pencere/ratio)-1):
        cv2.line(img, (i, int(data3[i])), (i+1,int(data3[i+1])), (0,0,0), 1)
    
#--------------------------------------------------------------------------------------
#------------ press the "Esc" button to break analysis of sound while cursor is on the image 
    k     = cv2.waitKey(int(pencere/3))
    if k == 27:
#------------ Save the heart sound data -----------------------------------------------
        sounddata = np.array(sounddata)
        np.save("SoundData", sounddata)
#--------------------------------------------------------------------------------------
        stream.close()

        break

    elif k==-1:
        continue
#--------------------------------------------------------------------------------------

