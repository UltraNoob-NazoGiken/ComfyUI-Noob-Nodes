import os
import time
from server import PromptServer

class ComfyUICounterWithReset:
    _node_states = {}

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "reset_switch": ("BOOLEAN", {"default": True}),
                "initial_value": ("INT", {"default": 0, "min": 0, "max": 1000000, "step": 1}),
                # ✨ 新機能：カウントアップさせるかどうかのスイッチを追加
                "count_up": ("BOOLEAN", {"default": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("INT",)
    FUNCTION = "do_count"
    CATEGORY = "CustomUtils"

    @classmethod
    def IS_CHANGED(s, reset_switch, initial_value, count_up, unique_id=None):
        # 毎実行時にキャッシュを無効化
        return time.time()

    def do_count(self, reset_switch, initial_value, count_up, unique_id):
        # --------------------------------------------------
        # ✨ 新機能：count_up が OFF の場合は、固定値としてそのまま出力
        # --------------------------------------------------
        if not count_up:
            return (initial_value,)

        # ⬇️ 以下は count_up が ON のとき（これまでのカウントアップ挙動）
        if reset_switch or (unique_id not in self._node_states):
            current_value = initial_value
            self._node_states[unique_id] = current_value
            
            PromptServer.instance.send_sync("counter_node_reset_trigger", {
                "node_id": unique_id
            })
        else:
            self._node_states[unique_id] += 1
            current_value = self._node_states[unique_id]

        return (current_value,)