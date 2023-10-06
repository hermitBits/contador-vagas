import cv2

from colors import *
from settings import *

from classes_template import Rect
from persistence import load_parking_lots, dump_parking_lots


parking_lots = load_parking_lots()


def click_event(events, x, y, flags, params) -> None:
    if events == cv2.EVENT_LBUTTONDOWN:
        parking_space = Rect(x=x,y=y,width=x+WIDTH,height=y+HEIGHT)
        parking_lots.append(parking_space)
    
    if events == cv2.EVENT_RBUTTONDOWN:
        for index, parking_space in enumerate(parking_lots):
            valida_x = parking_space.x < x < parking_space.x + WIDTH
            valida_y = parking_space.y < y < parking_space.y + HEIGHT
            if valida_x and valida_y:
                parking_lots.pop(index)


if __name__ == '__main__':
    while True:
        img = cv2.imread('vagas.png')
        
        for parking_space in parking_lots:
            cv2.rectangle(img, parking_space.pt1, parking_space.pt2, GREEN, 2)
        
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', click_event)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            dump_parking_lots(parking_lots)
            break