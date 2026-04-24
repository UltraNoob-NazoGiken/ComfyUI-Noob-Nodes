class MultiStringSplitter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "stringA": ("STRING", {"default": "aaaa-bbbb-cccc-dddd", "multiline": True}),
                "charB": ("STRING", {"default": "-"}),
            },
        }

    # 出力ポートをあらかじめ多め（例として6つ）に用意します
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("text_1", "text_2", "text_3", "text_4", "text_5", "text_6")
    
    FUNCTION = "split_text_multi"
    CATEGORY = "MyCustomNodes/Text"

    def split_text_multi(self, stringA, charB):
        if not stringA:
            return ("", "", "", "", "", "")
        
        # 指定した文字で分割（個数制限なし）
        # 引数に何も入れない split() だと空白で分割されますが、charBを指定すればその文字で分けます
        parts = stringA.split(charB)
        
        # 出力用のリストを作成（初期値はすべて空文字）
        results = [""] * 6
        
        # 分割されたデータを順番に入れていく（最大6つまで）
        for i in range(min(len(parts), 6)):
            results[i] = parts[i]
            
        # タプルに変換して返す
        return tuple(results)