import json
from typing import List
from src.classes_template import Rect


def dump_parking_lots(parking_lots) -> None:
    parking_lots_to_dict = [parking_space.to_dict() for parking_space in parking_lots]
    with open('vagas.json', 'w') as file:
        json.dump(parking_lots_to_dict, file)
        
        
def load_parking_lots() -> List[Rect]:
    try:
        with open('vagas.json', 'r') as file:
            parking_lots_from_dict = json.load(file)
        parking_lots = [Rect.from_dict(parking_space) for parking_space in parking_lots_from_dict]
        return parking_lots
    except:
        return []