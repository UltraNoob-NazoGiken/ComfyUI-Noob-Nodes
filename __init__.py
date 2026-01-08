from .nodes import TaggerMix
from .nodes import ListImagesNode
from .nodes import PathCleaner

from .SequentialDirectory import SequentialDirectoryNode

from .MaskFill import MaskFillNode

from .fix_pose_keypoints import FixPoseKeypoints
from .fix_pose_keypoints import DebugPose

from .zero_pad_node import ZeroPadNode

from .create_folders_from_path import CreateFoldersFromPath

from .square_bbox_from_mask import SquareBBoxFromMask


NODE_CLASS_MAPPINGS = {
    "TaggerMix": TaggerMix,
    "ListImagesNode": ListImagesNode,
    "MaskFillNode": MaskFillNode,
    "SequentialDirectoryNode": SequentialDirectoryNode,
    "PathCleaner": PathCleaner,
    "FixPoseKeypoints": FixPoseKeypoints,
    "DebugPose": DebugPose,
    "ZeroPadNode": ZeroPadNode,
    "CreateFoldersFromPath": CreateFoldersFromPath,
    "SquareBBoxFromMask": SquareBBoxFromMask
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TaggerMix": "Tagger Extract and Mix",
    "ListImagesNode": "List Images from Directory",
    "MaskFillNode": "Mask Fill with Color",
    "SequentialDirectoryNode": "Sequential Directory Generator",
    "PathCleaner": "Path Cleaner",
    "FixPoseKeypoints": "Fix Pose Keypoints (BODY25 Pad)",
    "DebugPose": "Debug PoseKeypoint",
    "ZeroPadNode": "Zero Pad (INT → 0000)",
    "CreateFoldersFromPath": "Create Folders From Path",
    "SquareBBoxFromMask": "Square BBox From Mask"
}



__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']