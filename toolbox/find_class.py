from lib.unreal_collector import UnrealCollector
from lib.misc import Color


def find_class():
    color = Color("(R=78,G=78,B=111,A=255)")
    uc = UnrealCollector("modular_neighborhood")
    obj_id = uc.get_obj_from_color(color)
    print(obj_id)