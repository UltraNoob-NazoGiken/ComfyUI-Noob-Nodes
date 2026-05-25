import torch

class ImageCacheNode:
    # 🌟 単一の変数ではなく、辞書型（dict）にしてノードごとに管理する
    _stored_images = {}

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "use_cache": ("BOOLEAN", {"default": False}),
            },
            # 💡 ComfyUIからこのノードの固有ID（unique_id）を自動で受け取る魔法の設定
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "custom_cache"

    # 💡 引数に unique_id を追加します
    def process(self, image, use_cache, unique_id):
        # このノード固有のキャッシュが存在するかチェック
        has_cache = unique_id in ImageCacheNode._stored_images

        if use_cache:
            # 【スイッチON】自分のノードIDのキャッシュがあればそれを出力
            if has_cache:
                print(f"[ImageCache-{unique_id}] キャッシュされた前回の画像を出力します。")
                return (ImageCacheNode._stored_images[unique_id],)
            else:
                print(f"[ImageCache-{unique_id}] 警告: キャッシュが空のため、現在の画像を出力します。")
                ImageCacheNode._stored_images[unique_id] = image
                return (image,)
        else:
            # 【スイッチOFF】現在の入力を自分のノードID専用のロッカーに保存してスルー出力
            print(f"[ImageCache-{unique_id}] 新しい画像をキャッシュに保存しました。")
            ImageCacheNode._stored_images[unique_id] = image
            return (image,)

    @classmethod
    def IS_CHANGED(s, image, use_cache, unique_id):
        # 引数の数を process と合わせる必要があります
        return float("nan")