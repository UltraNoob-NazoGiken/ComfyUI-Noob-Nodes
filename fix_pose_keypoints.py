import numpy as np
import json

class FixPoseKeypoints:
    """
    Fix DWpose Estimator pose_keypoint into OpenPose-compatible BODY25 (75 values).
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pose_keypoint": ("POSE_KEYPOINT",),
            }
        }

    RETURN_TYPES = ("POSE_KEYPOINT",)
    FUNCTION = "fix"
    CATEGORY = "Pose/Utilities"

    def fix(self, pose_keypoint):

        # pose_keypoint は ComfyUI 内部の PoseKeypoint オブジェクト
        # 中には pose_keypoints（ndarray）が存在する
        arr = pose_keypoint["pose_keypoints"]

        REQUIRED = 75

        # numpy 配列として処理
        arr = np.array(arr, dtype=np.float32)

        if arr.size < REQUIRED:
            padding = np.zeros(REQUIRED - arr.size, dtype=np.float32)
            arr = np.concatenate([arr, padding], axis=0)
        elif arr.size > REQUIRED:
            arr = arr[:REQUIRED]

        # 元と同じ構造で返す（ココが重要）
        new_obj = pose_keypoint.copy()
        new_obj["pose_keypoints"] = arr

        return (new_obj,)
    

class DebugPose:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"x": ("POSE_KEYPOINT",)}}

    # ★ 文字列として返す
    RETURN_TYPES = ("STRING",)
    FUNCTION = "dbg"
    CATEGORY = "Pose/Debug"

    def dbg(self, x):
        log = []

        # TYPE
        try:
            log.append(f"TYPE: {type(x)}")
        except:
            log.append("TYPE: (error)")

        # JSON dump
        try:
            dump = json.dumps(x)[:1000]
            log.append("CONTENT (first 1000 chars):")
            log.append(dump)
        except:
            log.append("CONTENT: (json dump failed)")
            log.append(str(x)[:1000])

        # numpy shape
        try:
            arr = np.array(x)
            log.append(f"AS NUMPY SHAPE: {arr.shape}")
        except:
            log.append("AS NUMPY: (conversion failed)")

        # 改行で結合して返す
        output_text = "\n".join(log)

        return (output_text,)
