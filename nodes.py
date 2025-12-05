import os
from typing import List, Tuple
from nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
import numpy as np
from PIL import Image
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
    
