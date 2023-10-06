import cv2
import numpy as np


vagas = [
    {'x': 1, 'y': 89, 'width': 108, 'height': 213},
    {'x': 115, 'y': 87, 'width': 152, 'height': 211},
    {'x': 289, 'y': 89, 'width': 138, 'height': 212},
    {'x': 439, 'y': 87, 'width': 135, 'height': 212},
    {'x': 591, 'y': 90, 'width': 132, 'height': 206},
    {'x': 738, 'y': 93, 'width': 139, 'height': 204},
    {'x': 881, 'y': 93, 'width': 138, 'height': 201},
    {'x': 1027, 'y': 94, 'width': 147, 'height': 202}
]

video = cv2.VideoCapture('video.mp4')

GREEN = (0, 255, 0)
RED = (0, 8, 255)
WHITE = (255, 255, 255)

def process_image(img):
    img_cinza = cv2.cvtColor(
        src=img,
        code=cv2.COLOR_BGR2GRAY
    )
    
    img_threshold = cv2.adaptiveThreshold(
        src=img_cinza,
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
    
    for vaga in vagas:
        x, y, w, h = vaga['x'], vaga['y'], vaga['width'], vaga['height']

        recorte = img_process[y:y+h, x:x+w]
        qtd_pixels_brancos = cv2.countNonZero(recorte)
        
        cv2.putText(
            img=img, 
            text=f'{qtd_pixels_brancos}',
            org=(x,y+h-10),
            fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            fontScale=0.5,
            color=WHITE,
            thickness=1
        )
        
        pt1, pt2 = (x, y), (x + w, y + h)

        if qtd_pixels_brancos > 3000:
            cv2.rectangle(img, pt1, pt2, RED, thickness=3)
        else:
            cv2.rectangle(img, pt1, pt2, GREEN, thickness=3)
    
    cv2.imshow('video', img)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()