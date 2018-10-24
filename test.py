import cv2
import numpy as np
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
    
def preprocess(array):
    array = cv2.cvtColor(array,cv2.COLOR_BGR2HSV)
    array = cv2.resize(array, (0,0), fx=0.5, fy=0.5) 
    kernel = np.ones((7,7),np.uint8)
    #array[:,:,2] = cv2.equalizeHist(array[:,:,2])
    #array = cv2.blur(array, (3,3), 5)
    array = cv2.erode(array,kernel, 10)
    array = cv2.dilate(array,kernel, 15)
    return array
    
def get_mask(img):
    array = preprocess(img)
    mask  = np.ones_like(array[:,:,0])
    h = array[:,:,0]
    s = array[:,:,1]
    v = array[:,:,2]
    mask[(h > 30)] = 0
    mask[(h < 18)] = 0
    mask[(v < 90)] = 0
    mask[(s < 85)] = 0
    return mask
 
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    while 1:
        # Capture frame-by-frame
        brightness=50
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,  10000)


        ret, frame = cap.read()
            
        #get preprocessed image
        preprocessed = cv2.cvtColor(preprocess(frame),cv2.COLOR_HSV2BGR)
        # get the mask for areas that pass the color thresholds
        mask = get_mask(frame)
        
        #display RGB image
        cv2.imshow('RGB image',frame)
        #display the mask
        cv2.imshow('Mask', mask*255)
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
