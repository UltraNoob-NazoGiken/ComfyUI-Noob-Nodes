import os
import comfy.sd
import folder_paths

class AnywhereLoraLoader:
    @classmethod
    def INPUT_TYPES(s):
        # UI上でLoRAリストを「参考」として表示させるためのテクニック
        # これにより、STRING型でありながらLoRA名を入力しやすくします
        return {
            "required": {
                "model": ("MODEL",),
                "lora_name": ("STRING", {"default": "", "multiline": False}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "load_lora_anywhere"
    CATEGORY = "loaders/anywhere"

    def load_lora_anywhere(self, model, lora_name, strength_model):
        if strength_model == 0 or not lora_name:
            return (model,)

        # 1. パス解決ロジック（ここがこのノードの生命線）
        all_loras = folder_paths.get_filename_list("loras")
        target_filename = os.path.basename(lora_name)
        resolved_path = None

        # 全ディレクトリをスキャンして一致するファイル名を探す
        for p in all_loras:
            if os.path.basename(p) == target_filename:
                resolved_path = p
                break

        # ヒットしなかった場合は、入力されたパスそのままで試行（フォールバック）
        if resolved_path is None:
            resolved_path = lora_name

        full_path = folder_paths.get_full_path("loras", resolved_path)
        
        if full_path is None or not os.path.exists(full_path):
            # ここで止まるのは「本当にファイルがPC内に存在しない時」だけ
            raise FileNotFoundError(f"AnywhereLoader: LoRA not found anywhere in your models/loras/ directory: {target_filename}")

        # 2. ロード処理
        print(f"[AnywhereLoader] Searching for: {target_filename}")
        print(f"[AnywhereLoader] Found and Loading: {resolved_path}")
        
        lora_data = comfy.utils.load_torch_file(full_path)
        model_lora, _ = comfy.sd.load_lora_for_models(model, None, lora_data, strength_model, 0)
        
        return (model_lora,)
