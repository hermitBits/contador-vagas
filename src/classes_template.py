from dataclasses import dataclass


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