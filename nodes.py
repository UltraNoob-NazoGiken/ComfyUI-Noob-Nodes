import os
import time
from typing import List, Tuple
import folder_paths
from nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
import numpy as np
from PIL import Image
import torch
import torchvision.transforms.functional as TF

# v5 PathClenerを追加
# v4 Sequential Directory Generator
# v3 Mask Fill with Color

class TaggerMix:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Base_Prompt": (
                    "STRING",
                    {"forceInput": True, "multilyne": True},
                ),
                "Tagger_Prompt": (
                    "STRING",
                    {"forceInput": True, "multilyne": True},
                ),
                "Extract_Prompt": (
                    "STRING",
                    {"forceInput": True, "multilyne": True},
                ),
            },
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("New Prompt",)
    FUNCTION = "go"
    CATEGORY = "test"

    def go(self, Base_Prompt, Tagger_Prompt, Extract_Prompt):
        # カンマで区切られた文字列を配列に変換
        Base_Prompt = [item.strip() for item in Base_Prompt.split(',')]
        Tagger_Prompt = [item.strip() for item in Tagger_Prompt.split(',')]
        Extract_Prompt = [item.strip() for item in Extract_Prompt.split(',')]

        # Tagger_Promptの中にExtract_Promptと一致する要素があるか検索
        for item in Tagger_Prompt:
            if item in Extract_Prompt:
                # 一致する要素をBase_Promptに追加
                Base_Prompt.append(item)

        # 結果を表示
        print("Base_Prompt:", Base_Prompt)
        # Base_Promptをカンマ区切りの文字列に変換
        newPrompt = ', '.join(map(str, Base_Prompt))
        print("newPrompt:",newPrompt)

        ## 重要:returnは必ずカンマを入れる
        return(newPrompt,)
    
class ListImagesNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"directory_path": ("STRING", {"default": ""})}}
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_list",)
    FUNCTION = "list_images"
    CATEGORY = "Custom Nodes"
    
    def list_images(self, directory_path: str) -> Tuple[str]:
        if not os.path.isdir(directory_path):
            return ("Error: Invalid directory path",)
        
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
        files = [f for f in os.listdir(directory_path) if os.path.splitext(f)[1].lower() in image_extensions]
        files.sort()  # 昇順ソート
        
        file_list = "\n".join([f"{i}: {filename}" for i, filename in enumerate(files)])
        
        return (file_list,)


class MaskFillNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "hex_code": ("STRING", {
                    "default": "#FF0000",
                    "ui": "color",  # カラーピッカーUI
                }),
                "red": ("INT", {
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                }),
                "green": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                }),
                "blue": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1,
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
        # テンソルをnumpy配列に変換
        if len(image.shape) == 4:  # バッチ次元がある場合
            img_np = image[0].cpu().numpy()
        else:
            img_np = image.cpu().numpy()
            
        if len(mask.shape) == 3:  # バッチ次元がある場合
            mask_np = mask[0].cpu().numpy()
        else:
            mask_np = mask.cpu().numpy()
        
        # 画像の形状を確認 (H, W, C)
        height, width, channels = img_np.shape
        
        # マスクの形状を画像に合わせる
        if len(mask_np.shape) == 2:
            mask_np = np.expand_dims(mask_np, axis=-1)
        
        # 色の取得（モードによって切り替え）
        if color_mode == "hex_code":
            color_rgb = self.parse_color(hex_code)
        else:  # rgb_values
            color_rgb = [red, green, blue]
        
        # 結果画像をコピー
        result_img = img_np.copy()
        
        # マスクが1（白）の部分を指定色で塗りつぶす
        for c in range(channels):
            result_img[:, :, c] = np.where(
                mask_np.squeeze() > 0.5,  # マスク値が0.5より大きい部分
                color_rgb[c] / 255.0,     # 指定色（0-1の範囲に正規化）
                result_img[:, :, c]       # 元の色
            )
        
        # テンソルに変換して返す
        result_tensor = torch.from_numpy(result_img).unsqueeze(0)  # バッチ次元を追加
        
        return (result_tensor,)
    
    def parse_color(self, color_str):
        """色文字列をRGB値に変換"""
        color_str = color_str.strip()
        
        # 色名の辞書
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
        
        # 色名で指定された場合
        if color_str.lower() in color_names:
            return color_names[color_str.lower()]
        
        # 16進数で指定された場合 (#FF0000形式)
        if color_str.startswith('#'):
            hex_color = color_str[1:]
            if len(hex_color) == 6:
                try:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    return [r, g, b]
                except ValueError:
                    pass
            elif len(hex_color) == 3:
                try:
                    r = int(hex_color[0], 16) * 17
                    g = int(hex_color[1], 16) * 17
                    b = int(hex_color[2], 16) * 17
                    return [r, g, b]
                except ValueError:
                    pass
        
        # RGB(r,g,b)形式の場合
        if color_str.startswith('rgb(') and color_str.endswith(')'):
            try:
                rgb_values = color_str[4:-1].split(',')
                if len(rgb_values) == 3:
                    r = int(rgb_values[0].strip())
                    g = int(rgb_values[1].strip())
                    b = int(rgb_values[2].strip())
                    return [r, g, b]
            except ValueError:
                pass
        
        # デフォルトは赤色
        print(f"警告: 色 '{color_str}' を解析できませんでした。赤色を使用します。")
        return [255, 0, 0]
    
class SequentialDirectoryNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_directory": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "prefix": ("STRING", {
                    "multiline": False,
                    "default": ""
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "get_next_directory"
    CATEGORY = "utilities"

    @classmethod
    def IS_CHANGED(cls, input_directory, prefix):
        """
        毎回実行させるために、常に変化があると認識させる
        """
        return time.time()  # 現在時刻を返すことで常に変化があると判定

    def get_next_directory(self, input_directory, prefix):
        """
        指定されたディレクトリ内でprefixを持つ連番フォルダの次の番号を見つける
        """
        # 入力チェック
        if not input_directory:
            return ("エラー: ディレクトリパスが指定されていません",)
        
        # prefixが空の場合はデフォルトで空文字列として処理
        if prefix is None:
            prefix = ""
        
        # ディレクトリが存在するかチェック
        if not os.path.exists(input_directory):
            return (f"エラー: ディレクトリが存在しません: {input_directory}",)
        
        if not os.path.isdir(input_directory):
            return (f"エラー: 指定されたパスはディレクトリではありません: {input_directory}",)
        
        # 既存のフォルダをチェックして最大番号を見つける
        max_number = -1
        found_folders = []
        
        try:
            # ディレクトリ内のすべてのアイテムを取得
            items = os.listdir(input_directory)
            
            for item in items:
                item_path = os.path.join(input_directory, item)
                # フォルダのみを対象とする
                if os.path.isdir(item_path):
                    # prefixが空の場合と空でない場合で処理を分ける
                    if prefix == "":
                        # prefixが空の場合：4桁の数字のみのフォルダを探す
                        if len(item) == 4 and item.isdigit():
                            number = int(item)
                            max_number = max(max_number, number)
                            found_folders.append(f"{item} (番号: {number})")
                    else:
                        # prefixがある場合：prefix_ で始まるかチェック
                        expected_prefix = f"{prefix}_"
                        if item.startswith(expected_prefix):
                            # 番号部分を抽出
                            number_part = item[len(expected_prefix):]
                            # 4桁の数字かチェック
                            if len(number_part) == 4 and number_part.isdigit():
                                number = int(number_part)
                                max_number = max(max_number, number)
                                found_folders.append(f"{item} (番号: {number})")
        
        except Exception as e:
            return (f"エラー: ディレクトリの読み取りに失敗しました: {str(e)}",)
        
        # デバッグ情報を追加
        debug_info = f"[デバッグ] 見つかったフォルダ: {found_folders}, 最大番号: {max_number}"
        print(debug_info)  # コンソールに出力
        
        # 次の番号を決定
        next_number = max_number + 1
        
        # 4桁の0埋め形式で番号をフォーマット
        next_number_str = f"{next_number:04d}"
        
        # 新しいディレクトリ名を作成
        if prefix == "":
            # prefixが空の場合：番号のみ
            new_folder_name = next_number_str
        else:
            # prefixがある場合：prefix_番号
            new_folder_name = f"{prefix}_{next_number_str}"
        
        # 完全なパスを作成
        output_path = os.path.join(input_directory, new_folder_name)
        
        return (output_path,)

class PathCleaner:
    """
    Windowsの「パスをコピー」で得られるダブルクォーテーション付きパスをクリーンにする
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("clean_path",)
    FUNCTION = "clean_path"
    CATEGORY = "utils"

    def clean_path(self, path):
        """
        パスからダブルクォーテーションを除去する
        """
        # 前後のダブルクォーテーションを除去
        clean = path.strip().strip('"').strip("'")
        
        print(f"入力パス: {path}")
        print(f"クリーン後: {clean}")
        
        return (clean,)
    
NODE_CLASS_MAPPINGS = {
    "TaggerMix": TaggerMix,
    "ListImagesNode": ListImagesNode,
    "MaskFillNode": MaskFillNode,
    "SequentialDirectoryNode": SequentialDirectoryNode,
    "PathCleaner": PathCleaner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TaggerMix": "Tagger Extract and Mix",
    "ListImagesNode": "List Images from Directory",
    "MaskFillNode": "Mask Fill with Color",
    "SequentialDirectoryNode": "Sequential Directory Generator",
    "PathCleaner": "Path Cleaner",
}

