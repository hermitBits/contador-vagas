
import cv2
import numpy as np

from cv2.typing import MatLike

from src.colors import *
from src.settings import *

from src.persistence import load_parking_lots


parking_lots = load_parking_lots()
video = cv2.VideoCapture('video.mp4')


def process_image(img) -> MatLike:
    img_grey = cv2.cvtColor(
        src=img,
        code=cv2.COLOR_BGR2GRAY
    )
    
    img_threshold = cv2.adaptiveThreshold(
        src=img_grey,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=25,
        C=16
    )
    
    img_blur = cv2.medianBlur(
        src=img_threshold,
        ksize=5
    )
    
    kernel = np.ones((3, 3), np.int8)
    img_dilate = cv2.dilate(
        src=img_blur,
        kernel=kernel
    )
    
    return img_dilate


while True:
    ret, img = video.read()
    
    if not ret:
        break
    
    img_process = process_image(img)
    
    for parking_space in parking_lots:
        cropped_image = img_process[
            parking_space.y:parking_space.y+HEIGHT, 
            parking_space.x:parking_space.x+WIDTH
        ]
        
        total_white_pixels = cv2.countNonZero(cropped_image)

        cv2.putText(
            img=img, 
            text=f'{total_white_pixels}',
            org=(parking_space.x,parking_space.y+HEIGHT-10),
            fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            fontScale=0.5,
            color=WHITE,
            thickness=1
        )
        
        color = GREEN
        if total_white_pixels > 3000:
            color = RED
            
        cv2.rectangle(img, parking_space.pt1, parking_space.pt2, color, thickness=3)
    
    cv2.imshow('video', img)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
