import os

class CreateFoldersFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path_string": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("created_folder_path",)
    FUNCTION = "create_folders"
    CATEGORY = "utils/filesystem"

    def create_folders(self, path_string):
        # 正規化
        path = os.path.normpath(path_string)

        # 末尾がファイルかどうかを判定
        # 拡張子があればファイルとみなす
        base, ext = os.path.splitext(path)
        if ext:
            folder_path = os.path.dirname(path)
        else:
            folder_path = path

        # フォルダ作成（途中が無くてもOK）
        if folder_path:
            os.makedirs(folder_path, exist_ok=True)

        return (folder_path,)