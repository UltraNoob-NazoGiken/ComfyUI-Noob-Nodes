from .nodes import TaggerMix
from .nodes import ListImagesNode
from .nodes import PathCleaner

from .SequentialDirectory import SequentialDirectoryNode

from .MaskFill import MaskFillNode

from .zero_pad_node import ZeroPadNode

from .create_folders_from_path import CreateFoldersFromPath

from .square_bbox_from_mask import SquareBBoxFromMask

from .string_lora_name import StringToLoraName

from .pixel_color_picker import PixelColorPicker


NODE_CLASS_MAPPINGS = {
    "TaggerMix": TaggerMix,
    "ListImagesNode": ListImagesNode,
    "MaskFillNode": MaskFillNode,
    "SequentialDirectoryNode": SequentialDirectoryNode,
    "PathCleaner": PathCleaner,
    "ZeroPadNode": ZeroPadNode,
    "CreateFoldersFromPath": CreateFoldersFromPath,
    "SquareBBoxFromMask": SquareBBoxFromMask,
    "StringToLoraName": StringToLoraName,
    "PixelColorPicker": PixelColorPicker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TaggerMix": "Tagger Extract and Mix",
    "ListImagesNode": "List Images from Directory",
    "MaskFillNode": "Mask Fill with Color",
    "SequentialDirectoryNode": "Sequential Directory Generator",
    "PathCleaner": "Path Cleaner",
    "ZeroPadNode": "Zero Pad (INT → 0000)",
    "CreateFoldersFromPath": "Create Folders From Path",
    "SquareBBoxFromMask": "Square BBox From Mask",
    "StringToLoraName": "String to LoRA Name",
    "PixelColorPicker": "Pixel Color Picker (HEX)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']