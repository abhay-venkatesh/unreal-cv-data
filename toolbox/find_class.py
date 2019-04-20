from lib.unreal_collector import UnrealCollector
from lib.misc import Color


def find_class(rgba="(R=191,G=0,B=223,A=255)"):
    color = Color(rgba)
    uc = UnrealCollector("modular_neighborhood")
    obj_ids = uc.get_objs_from_color(color)
    print(obj_ids)