class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False

class TautologyStr(str):
    def __ne__(self, other):
        return False

class StringToLoraName:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "lora_name": ("STRING", {
                    "default": "my_lora.safetensors",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = (AlwaysEqualProxy('*'),)
    RETURN_NAMES = ("lora_name",)

    FUNCTION = "run"
    CATEGORY = "utils"

    def run(self, lora_name):
        return (lora_name,)


