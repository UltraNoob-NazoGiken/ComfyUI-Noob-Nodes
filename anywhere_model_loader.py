import os
import comfy.sd
import folder_paths

class AnywhereModelLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # UNET/Diffusionモデル用のファイル名（パスを含む文字列）
                "model_name": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "load_model_anywhere"
    CATEGORY = "loaders/anywhere"

    def load_model_anywhere(self, model_name):
        if not model_name:
            raise ValueError("AnywhereModelLoader: model_name is empty.")

        # 1. 現在の環境の全UNETモデルリストを取得
        # folder_paths.get_filename_list("unet") は models/unet 内を指します
        all_models = folder_paths.get_filename_list("diffusion_models")
        
        target_filename = os.path.basename(model_name)
        resolved_path = None

        # 2. 階層を無視してファイル名一致を検索
        for p in all_models:
            if os.path.basename(p) == target_filename:
                resolved_path = p
                break

        # ヒットしなかった場合のフォールバック
        if resolved_path is None:
            resolved_path = model_name

        full_path = folder_paths.get_full_path("diffusion_models", resolved_path)
        
        if full_path is None or not os.path.exists(full_path):
            raise FileNotFoundError(f"AnywhereModelLoader: Model file not found: {target_filename}")

        # 3. モデルのロード処理
        print(f"[AnywhereLoader] Model Resolved: {model_name} -> {resolved_path}")
        
        # comfy.sd のコア関数を使用してロード
        model = comfy.sd.load_diffusion_model(full_path)
        
        return (model,)
    
class AnywhereModelNameSelector:
    @classmethod
    def INPUT_TYPES(s):
        # diffusion_models フォルダのみからリストを取得
        diff_list = folder_paths.get_filename_list("diffusion_models")
        return {
            "required": {
                "model_name": (sorted(diff_list), ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_name",)
    FUNCTION = "get_name"
    CATEGORY = "loaders/anywhere"

    def get_name(self, model_name):
        return (model_name,)