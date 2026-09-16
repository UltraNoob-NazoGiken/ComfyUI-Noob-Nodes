import os
import re
import torch
import numpy as np
from PIL import Image, ImageOps

class LoadPreviousFrame:
    """
    指定されたパス内の画像リストから、index - 1 番目の画像を読み込むノード。
    インデックスがマイナスの場合や、画像が存在しない・読み込めない場合は
    入力された Dummy Image をそのまま出力します。
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "dummy_image": ("IMAGE",),
                "path": ("STRING", {"default": "", "multiline": False}),
                "index": ("INT", {"default": 0, "min": -100000, "max": 100000, "step": 1}),
            }
        }

    # 出力ピンの型定義を追加
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "full_path", "filename")
    FUNCTION = "load_frame"
    CATEGORY = "image/loading"

    def load_frame(self, dummy_image, path, index):
        # 対象となるインデックスを計算 (index - 1)
        target_index = index - 1

        # 1. target_index がマイナス値の場合はダミー画像を出力
        if target_index < 0:
            return (dummy_image, "", "")

        # 2. パスの存在確認
        if not path or not os.path.exists(path) or not os.path.isdir(path):
            return (dummy_image, "", "")

        # 対応する画像拡張子
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff')

        try:
            # ディレクトリ内の画像ファイルを取得
            image_files = [
                os.path.join(path, f) for f in os.listdir(path)
                if f.lower().endswith(valid_extensions)
            ]

            # 画像が1つもない場合
            if not image_files:
                return (dummy_image, "", "")

            # 自然順ソート（例: frame_2.png が frame_10.png より前に来るように整列）
            def natural_sort_key(s):
                return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]
            
            image_files.sort(key=natural_sort_key)

            # 3. target_index が取得した画像リストの範囲外（大きすぎる）場合
            if target_index >= len(image_files):
                return (dummy_image, "", "")

            # 画像パスとファイル名の取得
            img_path = image_files[target_index]
            filename = os.path.basename(img_path)

            # 画像の読み込み処理
            img = Image.open(img_path)
            img = ImageOps.exif_transpose(img)  # EXIF回転情報の自動補正
            img = img.convert("RGB")
            
            # ComfyUIの形式 (Tensor float32 BHWC [1, H, W, 3]) に変換
            image_np = np.array(img).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np).unsqueeze(0)

            return (image_tensor, img_path, filename)

        except Exception as e:
            # 4. その他あらゆるエラーハンドリング（読み込み失敗など）
            print(f"[LoadPreviousFrame] Warning: Failed to load image ({e}). Outputting dummy image.")
            return (dummy_image, "", "")