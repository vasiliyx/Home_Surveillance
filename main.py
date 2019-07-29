'''
This monitors the environment, and if motion is detected, start recording.
    - Perform MOG2 algorython (adaptive background subtraction)
    - Calculate the percent change of the scene
    - If the percent change threshold is hit, start recording for some time in a new file
By Vasiliy Baryshnikov
'''

from cv2 import *; import cv2; cv = cv2;
import numpy as np;
from general_defines import *;


import time;
import datetime;

myImagePath = 0;

#--------------------------------------------------------------------------------
## Timer class keeps track of the time and the timeout functionality.
class Timer:
    # How to use:
    # timer = Timer(); # instantiate outside the loop
    # timer.Start(1.00); # Start the timer tunning with the timeout variable set to 1.00 sec
    # timer.IsTimeout(); # Check whether the timeout has happened
    
    import time;
    t = 0; # init static vars
    t_old = 0; # init static vars
    timeout = 0;  # timeout timer
    diff = 0;
    #isTimeout = False;

    # Start the timer running.
    def Start(self, timeout):
        self.timeout = timeout; # in secods
        self.t = self.time.time(); # init static vars
        self.t_old = self.time.time(); # init static vars
        self.diff = 0;

        pass;
    
    def Stop(self):
        pass;

    # Check whether the timeout has happened.
    def IsTimeout(self):
        self.t = self.time.time(); # current time stamp
        self.diff = self.t - self.t_old;
        
        if self.diff > self.timeout:
            return True;
        return False;

    pass;
#--------------------------------------------------------------------------------



#--------------------------------------------------------------------------------
# Main
if __name__ == "__main__":

    cap = cv2.VideoCapture(myImagePath);
    ret, frame = cap.read(); # Load the color frame
    h, w = frame.shape[:2];   # Get the dimensions of the mat
    area_mat = h*w;         # Get the area of the mat in pixels

    # Init and config the background subtractor object
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False); # MOG2

    # define the kernel for the morphological filtering
    kernel = getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)); # Standard Rectangular Kernel


    fps = Fps();
    timer = Timer();

    # Init the Flags
    isRecording = False; # Indicates whether we are recording right now

    while(1):
        # Get the image from the camera
        ret, frame = cap.read(); # Load the color frame
        vis = frame.copy();

        # Get the Foreground mask
        fgmask = fgbg.apply(frame); # Get the foreground mask. 
        fgmask = morphologyEx(fgmask, MORPH_OPEN, kernel); # opening is eroding followed by the dilating. Kills the white spot noise
        
        # Get all contours of our foreground mask
        contours, hierarchy = findContours(fgmask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE);

        # Get the total area of the foreground mask in pixels
        area_mask_tot = 0; # total area in pixels of the foreground
        for contour in contours:
            area_mask_tot += contourArea(contour);  # Calculate the area of the contour in pixels
            pass;
    
        # Calculate the relative change of the image in percent
        relative_change = area_mask_tot / area_mat * 100; 

        # Get current time for the timestamp
        ts = time.time();
        time_str = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S');

        # Draw the status variables on the screen
        Draw_str(vis, (20, 20), 'change: %d %' % relative_change); # print the counter of tracks on the mat
        Draw_str(vis, (20, 40), 'fps: %d' % fps.Get()); # print the fps on the mat
        Draw_str(vis, (20, 60), time_str); # print the fps on the mat

        # Show!
        #cv2.imshow('fgmask', fgmask);
        cv2.imshow('vis', vis);
             
        # Output the frame to the file if necessary
        
        # Relative Change Threshold
        if relative_change >= 10:
      
            # If we are not already recording, start recording into a new file
            if not isRecording:
                ts = time.time();
                file_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S');
                
                # Define the codec and create VideoWriter object 
                fourcc = cv2.VideoWriter_fourcc(*'XVID');
                out = cv2.VideoWriter(file_timestamp + '.avi', fourcc, 14.0, (w, h)); # 14 fps
                pass;

            timer.Start(5.0); # Start timer with X sec timeout
            pass;

        # Record until the timer timeout
        if not timer.IsTimeout():
            isRecording = True;
            out.write(vis);
            pass;

        # Stop recording
        if timer.IsTimeout():
            isRecording = False;
            out.release();
            pass;

        # Key handler
        k = cv2.waitKey(30) & 0xff;
        if k == 27: 
            break;
        pass;

    cap.release();
    out.release();
    cv2.destroyAllWindows();

    pass
#--------------------------------------------------------------------------------


