from dataclasses import dataclass
import json
import cv2

GREEN = (0, 255, 0)
RED = (0, 8, 255)
WHITE = (255, 255, 255)

def dump_vagas():
    vagas_dict = [vaga.to_dict() for vaga in vagas]
    with open('vagas.json', 'w') as file:
        json.dump(vagas_dict, file)
        
def load_vagas():
    try:
        with open('vagas.json', 'r') as file:
            vagas_dict = json.load(file)
        vagas = [Rect.from_dict(vaga) for vaga in vagas_dict]
        return vagas
    except:
        return []
    
@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int
    
    @property
    def pt1(self):
        return (self.x, self.y)
    
    @property
    def pt2(self):
        return (self.width, self.height)
    
    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

width, height = 108, 213

vagas = load_vagas()

def click_event(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        vaga = Rect(x=x,y=y,width=x+width,height=y+height)
        vagas.append(vaga)
    if events == cv2.EVENT_RBUTTONDOWN:
        for index, vaga in enumerate(vagas):
            if vaga.x < x < vaga.x + width and vaga.y < y < vaga.y + height:
                vagas.pop(index)

if __name__ == '__main__':
    while True:
        img = cv2.imread('vagas.png')
        
        for vaga in vagas:
            cv2.rectangle(img, vaga.pt1, vaga.pt2, GREEN, 2)
        
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', click_event)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            dump_vagas()
            break