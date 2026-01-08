import torch
import numpy as np

class SquareBBoxFromMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("x", "y", "w", "h")
    FUNCTION = "get_square_bbox"
    CATEGORY = "image/mask"

    def get_square_bbox(self, mask):
        # mask: (1, H, W) or (H, W)
        if len(mask.shape) == 3:
            mask_np = mask[0].cpu().numpy()
        else:
            mask_np = mask.cpu().numpy()

        H, W = mask_np.shape

        ys, xs = np.where(mask_np > 0.5)

        if len(xs) == 0 or len(ys) == 0:
            # マスクが空の場合は全体
            return (0, 0, W, H)

        x0 = int(xs.min())
        x1 = int(xs.max())
        y0 = int(ys.min())
        y1 = int(ys.max())

        bw = x1 - x0 + 1
        bh = y1 - y0 + 1

        # 中心
        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2

        # 正方形サイズ（長辺基準）
        size = max(bw, bh)

        # 正方形bboxを中心基準で作る
        half = size // 2

        new_x0 = cx - half
        new_y0 = cy - half

        # 偶数奇数ズレ補正
        new_x1 = new_x0 + size
        new_y1 = new_y0 + size

        # 画像外にはみ出ないように補正
        if new_x0 < 0:
            new_x1 -= new_x0
            new_x0 = 0
        if new_y0 < 0:
            new_y1 -= new_y0
            new_y0 = 0

        if new_x1 > W:
            diff = new_x1 - W
            new_x0 -= diff
            new_x1 = W
        if new_y1 > H:
            diff = new_y1 - H
            new_y0 -= diff
            new_y1 = H

        # 最終クランプ
        new_x0 = max(0, new_x0)
        new_y0 = max(0, new_y0)
        new_x1 = min(W, new_x1)
        new_y1 = min(H, new_y1)

        final_w = int(new_x1 - new_x0)
        final_h = int(new_y1 - new_y0)

        return (int(new_x0), int(new_y0), final_w, final_h)


