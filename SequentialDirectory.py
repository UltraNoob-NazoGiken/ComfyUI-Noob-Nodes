import os
import time

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
            try:
                # ディレクトリを新規作成します。
                # exist_ok=True は、もしディレクトリが既に存在してもエラーにしないようにします
                # (ただし、今回は if not os.path.exists でチェックしているので不要ですが、一般的には安全です)。
                # parents=True は、必要な親ディレクトリもすべて作成します。
                os.makedirs(input_directory, exist_ok=True)
                print(f"ディレクトリを新規作成しました: {input_directory}")
            except OSError as e:
                # ディレクトリ作成に失敗した場合（権限がないなど）のエラーハンドリング
                return (f"エラー: ディレクトリの作成に失敗しました: {input_directory}. 詳細: {e}",)

        
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
