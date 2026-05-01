class RemapValueRange:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_value": ("FLOAT", {"default": 0.0, "step": 0.001, "display": "number"}),
                "input_low": ("FLOAT", {"default": 0.0, "step": 0.001}),
                "input_high": ("FLOAT", {"default": 1.0, "step": 0.001}),
                "target_low": ("FLOAT", {"default": 0.0, "step": 0.001}),
                "target_high": ("FLOAT", {"default": 1.0, "step": 0.001}),
                "clamp": ("BOOLEAN", {"default": True}),
                "interp_type": (["linear", "smoothstep", "smootherstep"], {"default": "linear"}),
            },
        }

    RETURN_TYPES = ("FLOAT", "INT")
    RETURN_NAMES = ("FLOAT_VALUE", "INT_VALUE")
    FUNCTION = "remap"
    CATEGORY = "math/utils"

    def remap(self, input_value, input_low, input_high, target_low, target_high, clamp, interp_type):
        # 1. ゼロ除算の安全対策
        if abs(input_high - input_low) < 1e-7:
            # 入力範囲が0なら、入力値に関わらずtarget_lowを返す
            return (float(target_low), int(round(target_low)))

        # 2. 正規化 (0.0 - 1.0 の割合を出す)
        t = (input_value - input_low) / (input_high - input_low)
        
        # 3. クランプ処理 (範囲外の数値を丸める)
        if clamp:
            t = max(0.0, min(1.0, t))

        # 4. 補間処理 (カーブの適用)
        if interp_type == "smoothstep":
            t = t * t * (3 - 2 * t)
        elif interp_type == "smootherstep":
            t = t * t * t * (t * (t * 6 - 15) + 10)

        # 5. ターゲット範囲へマッピング
        result = target_low + t * (target_high - target_low)

        # FLOATとINT両方の型で出力
        return (float(result), int(round(result)))