from .nodes import TaggerMix
from .nodes import ListImagesNode
from .nodes import PathCleaner

# webフォルダをComfyUIに認識させるための宣言
WEB_DIRECTORY = "./web"

from .SequentialDirectory import SequentialDirectoryNode
from .MaskFill import MaskFillNode
from .zero_pad_node import ZeroPadNode
from .create_folders_from_path import CreateFoldersFromPath
from .square_bbox_from_mask import SquareBBoxFromMask
from .string_lora_name import StringToLoraName
from .pixel_color_picker import PixelColorPicker
from .model_path_resolver import ModelPathResolver
from .multi_split_node import MultiStringSplitter
from .seedance_byteplus import SeedanceBytePlusNode
from .simple_text_display import SimpleTextDisplay
from .remap_value_range import RemapValueRange


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
    "ModelPathResolver": ModelPathResolver,
    "MultiStringSplitter": MultiStringSplitter,
    "SeedanceBytePlusNode": SeedanceBytePlusNode,
    "SimpleTextDisplay": SimpleTextDisplay,
    "RemapValueRange": RemapValueRange,
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
    "ModelPathResolver": "Model Path Resolver",
    "MultiStringSplitter": "Multi-String Splitter (Max 6)",
    "SeedanceBytePlusNode": "Seedance 2.0 (Official API) - Noob Nodes",
    "SimpleTextDisplay": "Simple Text Display (Nodes 2.0)",
    "RemapValueRange": "Remap Value Range"

}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']