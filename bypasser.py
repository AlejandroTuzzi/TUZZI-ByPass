class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")


class Bypasser:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_select": ("INT", {"default": 1, "min": 1, "max": 2}),
                "input1": (any_type, {"defaultInput": True, "lazy": True}),
                "input2": (any_type, {"defaultInput": True, "lazy": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)
    FUNCTION = "switch"
    CATEGORY = "TUZZI-ByPass"

    def check_lazy_status(self, input_select, input1=None, input2=None):
        needed = []
        if input_select == 1:
            needed.append("input1")
        elif input_select == 2:
            needed.append("input2")
        return needed

    def switch(self, input_select, input1=None, input2=None):
        if input_select == 1:
            return (input1,)
        elif input_select == 2:
            return (input2,)
        else:
            return (None,)