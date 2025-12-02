from .nodes import TaggerMix
from .nodes import ListImagesNode
from .nodes import MaskFillNode
from .nodes import PathCleaner

from .SequentialDirectory import SequentialDirectoryNode

from .fix_pose_keypoints import FixPoseKeypoints
from .fix_pose_keypoints import DebugPose

NODE_CLASS_MAPPINGS = {
    "TaggerMix": TaggerMix,
    "ListImagesNode": ListImagesNode,
    "MaskFillNode": MaskFillNode,
    "SequentialDirectoryNode": SequentialDirectoryNode,
    "PathCleaner": PathCleaner,
    "FixPoseKeypoints": FixPoseKeypoints,
    "DebugPose": DebugPose,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TaggerMix": "Tagger Extract and Mix",
    "ListImagesNode": "List Images from Directory",
    "MaskFillNode": "Mask Fill with Color",
    "SequentialDirectoryNode": "Sequential Directory Generator",
    "PathCleaner": "Path Cleaner",
    "FixPoseKeypoints": "Fix Pose Keypoints (BODY25 Pad)",
    "DebugPose": "Debug PoseKeypoint",
}



__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']