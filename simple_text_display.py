# vue対応 テスト用ノードです 
# web/js/display_text.jsとともに削除してもOK
# initのところのweb_directoryを追記してますが、そのままでいい

from server import PromptServer

class SimpleTextDisplay:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text_input": ("STRING", {"forceInput": True})}}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "custom_test"

    def process(self, text_input):
        from server import PromptServer
        
        # ノードのインスタンスIDを取得
        node_id = id(self) 
        
        # UI側にカスタムメッセージを送信
        PromptServer.instance.send_sync("noob-text-update", {
            "node_id": node_id, 
            "text": text_input
        })
        
        return (text_input,)