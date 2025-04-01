from .bypasser import Bypasser
from .line_counter import LineCounter  #Esto es crucial

NODE_CLASS_MAPPINGS = {
    "TUZZI-Bypasser": Bypasser,
    "TUZZI-LineCounter": LineCounter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TUZZI-Bypasser": "Bypasser Switch",
    "TUZZI-LineCounter": "Count Lines in String",
}
