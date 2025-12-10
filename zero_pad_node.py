# zero_pad_node.py
# ゼロ埋め + prefix / suffix 付きカスタムノード

class ZeroPadNode:
    """
    整数をゼロ埋めし、prefix / suffix を付与して返すノード
    例: value=30, digits=4, prefix="CUT_", suffix="_A"
        → "CUT_0030_A"
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 0}),
                "digits": ("INT", {"default": 4, "min": 1, "max": 16}),
                "prefix": ("STRING", {"default": ""}),
                "suffix": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "pad"
    CATEGORY = "utils"

    def pad(self, value, digits, prefix, suffix):
        zero = str(value).zfill(digits)
        text = f"{prefix}{zero}{suffix}"
        return (text,)