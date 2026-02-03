import torch

class PixelColorPicker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "x": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 8192,
                    "step": 1
                }),
                "y": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 8192,
                    "step": 1
                }),
            }
        }

    RETURN_TYPES = ("COLORCODE",)
    RETURN_NAMES = ("color",)

    FUNCTION = "pick"
    CATEGORY = "Image/Utils"

    def pick(self, image, x, y):
        # image shape: [B, H, W, C], range: 0.0–1.0
        img = image[0]

        h, w, _ = img.shape

        # clamp coordinates
        x = max(0, min(x, w - 1))
        y = max(0, min(y, h - 1))

        pixel = img[y, x]

        r = int(pixel[0].item() * 255)
        g = int(pixel[1].item() * 255)
        b = int(pixel[2].item() * 255)

        hex_color = f"#{r:02X}{g:02X}{b:02X}"

        return (hex_color,)
