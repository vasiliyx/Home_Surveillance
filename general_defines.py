## @package general_defines
# This module includes general definitions of constants and functions and imports that will come handy across different modules.
# Version 1.2
# @author Vasiliy Baryshnikov

# Capture the pointer to the native python function
min_ = min; 
max_ = max;

# Import the packages
from cv2 import *;
import cv2 as cv; 
import numpy as np;

# Innumerate the camera device flags
WEBCAM = 0; INTEL = 1; 

# Default paths the the images
PATH = "./data/"; # path of all the pictures
IMG_PATH = PATH + "messi5.jpg";

# BGR Colour definitions for easy use
BLUE = (255, 0, 0); ## lala
GREEN = (0, 255, 0);
RED = (0, 0, 255);
YELLOW = (0,255,255);
CYAN = (255, 255, 0);
MAGENTA = (255, 0, 255);
WHITE = (255, 255, 255);
BLACK = (0, 0, 0);

# Drawing config flags
IS_CLOSED = True;
IS_OPEN = False;


#--------------------------------------------------------------------------------
## Update the screen with an image and wait for a keyboard hit.
# @param [in] output: The mat that will be displayed on the screen.
def Update_(output): # update the screen. Create a new one if mat is not provided
    cv.imshow("Output",output);
    cv.waitKey();
    pass
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Create an empty mat
# @param [in] rows:
# @param [in] cols:
# @param [in] channels: 3 channels for color image, 1 channel for black and white image.
# @return mat.
def EmptyMat(rows, cols, channels):
    return np.zeros((rows, cols,channels), np.uint8);
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
## Paint the mat entirely into one color.
# @param [out, in] mat: Mat (by ref).
# @param [in] color: Color of the blank. Default Black.
# @return mat.
def PaintMat(mat, color = BLACK):
    mat[:] = color; # Paint the mat into the specified color
    return mat;
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
## Prints the text on the mat.
# - if the text has multiple lines, start a new line.
# @param [out, in] mat: Mat (by ref). Text to be displayed
# @param [in] text: Text to be displayed on the mat
# @return The Output mat.
def PrintOnMat(mat, text):
    x0, y0, dy = 20, 50, 30;
    TEXT_FONT = FONT_HERSHEY_SIMPLEX;

    for i, line in enumerate(text.split('\n')):
        y = y0 + i*dy;
        putText(mat, line, (x0+1, y+1), TEXT_FONT, 0.7, BLACK, thickness = 4, lineType=cv.LINE_AA);
        putText(mat, line, (x0, y), TEXT_FONT, 0.7, WHITE, thickness = 2, lineType=cv.LINE_AA);
        
    return mat;
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
## Prints the small text label on the mat.
# @param [out, in] mat: Mat (by ref). Text to be displayed
# @param [in] loc: Location of the label.
# @param [in] text: Text to be displayed on the mat
def Draw_str(mat, loc, s):
    x, y = loc
    cv.putText(mat, s, (x+1, y+1), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv.LINE_AA)
    cv.putText(mat, s, (x, y), cv.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv.LINE_AA)
    pass;
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
## Performs the imshow command on a single final output window.
# @param [in] mat: mat that will be shared as a final window.
def imshow_Final(mat):
    cv.imshow("Output", mat);
    pass;
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
## Show the logo at the beggining for some time on the start-up.
# - image located on the disk
def StartupScreen():
    im = imread(PATH+".jpeg");
    imshow_Final(im);
    waitKey(2000);
    pass;
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
## Hold the value and perform the exponential moving avarage time filter (Low Pass)
# - The higher the coefficient, the more weight is allocated towards the older value
# - Think of this variable as a data type that allows to compute ema
class Ema: 
    def __init__(self, smooth_coef = 0.5):
        self.value = None; # There is no old value
        self.smooth_coef = smooth_coef; 
   
    def Update(self, valueNew):
        # If we just started, init the value
        if self.value is None: # If we just started...
            self.value = valueNew; # Update the value with the new value
            pass;
        
        # perform the smoothing on the value
        else: 
            c = self.smooth_coef;
            self.value = c * self.value + (1.0-c) * valueNew; # Update the value with after smoothing 
            pass;
        pass;
    
    def Get(self):
        return self.value;
    pass;
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
## Compute the fps of an operation in the loop. Display the result on the mat
class Fps:
    # How to use:
    # fps = Fps(); # instantiate outside the loop
    # fps.Get(); # get the fps, call only in the loop;
    # fps.Show(); # get and show the fps, call only in the loop;
    
    import time;
    t = 0.0; t_old = 0.0; # init static vars

    fps = Ema(smooth_coef = 0.6);
    mat_h, mat_w = 40, 100; # shape of the mat
    mat = EmptyMat(mat_h, mat_w, 1); # empty mat, for showing fps

    # Compute the fps and update the vars for future calls
    def Get(self):
        self.t_old = self.t; # time stamp since the last call
        self.t = self.time.time(); # current time stamp

        dt = self.t - self.t_old; # time it took to execute since the last call
        self.fps.Update(1/dt); # frequency 
        return round(self.fps.Get(), 2);

    # Computes the fps and shows it on the mat
    def Show(self):
        fps_str = str(self.Get()); # get a string value of the fps
        mat = putText(self.mat.copy(), fps_str, (10, self.mat_h - 10), FONT_HERSHEY_SIMPLEX, 0.7, WHITE, 1); # put it on the mat
        imshow("FPS Rate", mat); # show it
        pass;

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
## Get the size of the mat
# - Get the width and hight in pixels of the mat
# @param [in] mat: Mat, which size we will get
# @return w, h.
def Getsize(img):
    h, w = img.shape[:2];
    return h, w;
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# ## Convert and scale 1 channel image to uint8 size 
# - works well with converting float32 mats
# @param [in] mat: Mat, single channel, which has to be scale down and converted to uint8c1 
# @param [out] mat: Mat, the output mat in uint8c1
# @return mat.
def ScaleToUint8C1(input, output = None):

    # If output is not given as a destination, create the mat and return in
    if output is None:
        output = input.copy();
        
    normalize(input, output, 0, 255, NORM_MINMAX); # Normalize the image to the same level as original (result is still a float)
    output = output.astype(np.uint8); # convert the float (or whatever) to the uint8 for display in cv
    return output;
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
def ScaleToUint8C3(input, output = None):
    # Bring the distance image to uint8 format
    
    # If output is not given as a destination, make it
    if output is None:
        output = np.zeros_like(input);

    # TODO, look into CV_8UC3 and similar flags if error happens
    normalize(input, output, 0, 255, NORM_MINMAX); # Normalize the image to the same level as original (result is still a float)
    output = output.astype(np.uint8); # convert the float (or whatever) to the uint8 for display in cv
    return output;
#--------------------------------------------------------------------------------




#--------------------------------------------------------------------------------
## Draw the list of points on the mat
# @param [out, in] mat: Mat (by ref). Points to be displayed on.
# @param [in] points: List of points to be displayed on the mat.
# @param [in] color: Color of the points. Default Yellow.
def DrawKeypoints(vis, keypoints, color = YELLOW):
    for kp in keypoints:
        x, y = kp;
        cv.circle(vis, (int(x), int(y)), 2, color, 1);
    pass;
#--------------------------------------------------------------------------------

def Nothing(*arg, **kw):
    pass

def GetClock():
    return cv.getTickCount() / cv.getTickFrequency()



#--------------------------------------------------------------------------------
def ScaleDown(img, degree = 1):
    output = img.copy();
    for i in range(degree):
        output = cv.pyrDown(output, )
        pass;
    return output;
#--------------------------------------------------------------------------------



if __name__ == "__main__":
    points = [(0,0), (0,100), (100,0), (100,100)];
    mat = EmptyMat(500, 500, 3);
    PaintMat(mat, WHITE);
    h, w = Getsize(mat);
    print(h, w);
    a = "we are the people\nyes";


    DrawKeypoints(mat, points);
    #draw_str(mat, [10, 10], a);
    PrintOnMat(mat, a);
    Update_(mat);
     
    pass