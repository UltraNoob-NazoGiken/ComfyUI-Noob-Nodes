import torch
import numpy as np

class MaskFillNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "hex_code": ("STRING", {
                    "default": "#FFFFFF",
                    "ui": "color",
                }),
                "red": ("INT", {
                    "default": 255, "min": 0, "max": 255, "step": 1,
                }),
                "green": ("INT", {
                    "default": 0, "min": 0, "max": 255, "step": 1,
                }),
                "blue": ("INT", {
                    "default": 0, "min": 0, "max": 255, "step": 1,
                }),
                "color_mode": (["hex_code", "rgb_values"], {
                    "default": "hex_code"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("filled_image",)
    FUNCTION = "fill_mask"
    CATEGORY = "image/postprocessing"

    def fill_mask(self, image, mask, hex_code, red, green, blue, color_mode):

        # === バッチ次元取得 ===
        batch_img = image.shape[0]
        batch_msk = mask.shape[0]
        batch = min(batch_img, batch_msk)   # どちらか小さい方に合わせる

        # === numpy に変換 ===
        img_np = image[:batch].cpu().numpy()  # (B,H,W,C)
        mask_np = mask[:batch].cpu().numpy()  # (B,H,W) or (B,H,W,1)

        # === マスクの次元調整 (B,H,W,1) に統一 ===
        if mask_np.ndim == 3:
            mask_np = np.expand_dims(mask_np, axis=-1)

        # === 色の決定 ===
        if color_mode == "hex_code":
            color_rgb = self.parse_color(hex_code)
        else:
            color_rgb = [red, green, blue]

        # 0-1に正規化
        color_rgb = np.array(color_rgb) / 255.0

        # === ブロードキャストで一括処理 ===
        # mask_np: (B,H,W,1)
        # color_rgb: (3,) → (1,1,1,3) に拡張してブロードキャスト
        color_broadcast = color_rgb.reshape(1, 1, 1, 3)

        # 結果格納バッファ
        result_np = img_np.copy()

        # マスク部分だけ色置き換え（ベクトル化）
        result_np = np.where(
            mask_np > 0.5,
            color_broadcast,
            result_np
        )

        # テンソルに戻す
        result_tensor = torch.from_numpy(result_np).float()

        return (result_tensor,)


    def parse_color(self, color_str):
        color_str = color_str.strip()

        color_names = {
            'red': [255, 0, 0],
            'green': [0, 255, 0],
            'blue': [0, 0, 255],
            'white': [255, 255, 255],
            'black': [0, 0, 0],
            'yellow': [255, 255, 0],
            'cyan': [0, 255, 255],
            'magenta': [255, 0, 255],
            'orange': [255, 165, 0],
            'purple': [128, 0, 128],
            'pink': [255, 192, 203],
            'gray': [128, 128, 128],
            'grey': [128, 128, 128],
        }

        if color_str.lower() in color_names:
            return color_names[color_str.lower()]

        if color_str.startswith('#'):
            hex_color = color_str[1:]
            try:
                if len(hex_color) == 6:
                    return [
                        int(hex_color[0:2], 16),
                        int(hex_color[2:4], 16),
                        int(hex_color[4:6], 16)
                    ]
                elif len(hex_color) == 3:
                    return [
                        int(hex_color[0], 16) * 17,
                        int(hex_color[1], 16) * 17,
                        int(hex_color[2], 16) * 17
                    ]
            except ValueError:
                pass

        # rgb(r,g,b)
        if color_str.startswith('rgb(') and color_str.endswith(')'):
            try:
                r, g, b = color_str[4:-1].split(',')
                return [int(r), int(g), int(b)]
            except:
                pass

        print(f"警告: 色 '{color_str}' を解析できませんでした。赤色を使用します。")
        return [255, 0, 0]
