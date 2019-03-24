from lib.unreal_collector import UnrealCollector
from lib.misc import Color

if __name__ == "__main__":
    color = Color("(R=0,G=0,B=0,A=255)")
    uc = UnrealCollector("modular_neighborhood")
    obj_id = uc.get_obj_from_color(color)
    print(obj_id)