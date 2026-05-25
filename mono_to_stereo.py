import torch

class MonoToStereo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "convert"
    CATEGORY = "audio/converters"

    def convert(self, audio):
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]
        
        # waveform形状: [Batch, Channels, Samples] を想定
        # 多くのComfyUIオーディオ実装は3次元(B, C, S)か2次元(C, S)です
        
        if waveform.ndim == 3:
            if waveform.shape[1] == 1: # モノラルなら
                # チャンネル次元(dim=1)で複製して結合
                waveform = torch.cat((waveform, waveform), dim=1)
        elif waveform.ndim == 2:
            if waveform.shape[0] == 1: # モノラルなら
                waveform = torch.cat((waveform, waveform), dim=0)

        return ({"waveform": waveform, "sample_rate": sample_rate},)