import os
import folder_paths

class ModelPathResolver:
    @classmethod
    def INPUT_TYPES(s):
        try:
            folder_types = sorted(list(folder_paths.folder_names_and_paths.keys()))
        except Exception:
            folder_types = ["controlnet", "checkpoints", "loras", "upscale_models", "vae"]

        return {
            "required": {
                "path_string": ("STRING", {"default": "", "multiline": False}),
                "folder_type": (folder_types, {"default": "controlnet" if "controlnet" in folder_types else folder_types[0]}),
            },
        }

    # 出力を2つに増やしました：解決したパスと、実行ステータス
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("path", "status")
    FUNCTION = "resolve_path"
    CATEGORY = "CustomNodes/PathUtils"

    def resolve_path(self, path_string, folder_type):
        base_dirs = folder_paths.get_folder_paths(folder_type)
        path_string = path_string.strip()
        
        if not path_string:
            raise Exception(f"[{folder_type}] Input string is empty.")
        
        # 1. 直接チェック
        for base in base_dirs:
            full_path = os.path.normpath(os.path.join(base, path_string))
            if os.path.isfile(full_path):
                status = "✅ Direct match found."
                print(f"[Resolver] {status} ({path_string})")
                return (path_string, status)

        # 2. 再帰探索（ファイル名のみで検索）
        filename_only = os.path.basename(path_string)
        found_matches = []

        for base in base_dirs:
            if not os.path.exists(base):
                continue
                
            for root, _, files in os.walk(base):
                if filename_only in files:
                    found_full_path = os.path.join(root, filename_only)
                    relative_path = os.path.relpath(found_full_path, base)
                    relative_path = relative_path.replace("\\", "/")
                    found_matches.append(relative_path)

        # 3. 検索結果の判定
        if len(found_matches) == 0:
            # 見つからなかった場合
            error_msg = f"❌ Model Not Found: {filename_only} (Type: {folder_type})"
            raise Exception(error_msg)
            
        elif len(found_matches) > 1:
            # 【新規追加】 複数見つかった場合（重複エラー）
            matches_list = "\n".join([f"- {p}" for p in found_matches])
            error_msg = (
                f"⚠️ Multiple models found with the same name!\n"
                f"Please specify the path more accurately to avoid mistakes.\n\n"
                f"Found paths:\n{matches_list}"
            )
            print(f"[Resolver] ERROR: Multiple matches for {filename_only}")
            raise Exception(error_msg)
            
        else:
            # 1つだけ見つかった場合（正常な補正）
            corrected_path = found_matches[0]
            status = f"🔄 Path corrected: {corrected_path}"
            print(f"[Resolver] {status}")
            return (corrected_path, status)