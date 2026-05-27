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
from .anywhere_lora_loader import AnywhereLoraLoader
from .anywhere_model_loader import AnywhereModelLoader
from .anywhere_model_loader import AnywhereModelNameSelector
from .mono_to_stereo import MonoToStereo
from .image_cache_node import ImageCacheNode
from .counter_node import ComfyUICounterWithReset


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
    "AnywhereLoraLoader": AnywhereLoraLoader,
    "AnywhereModelLoader": AnywhereModelLoader,
    "AnywhereModelNameSelector": AnywhereModelNameSelector,
    "MonoToStereo": MonoToStereo,
    "ImageCacheNode": ImageCacheNode,
    "ComfyUICounterWithReset": ComfyUICounterWithReset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TaggerMix": "Tagger Extract and Mix",
    "ListImagesNode": "List Images from Directory - Noob Nodes",
    "MaskFillNode": "Mask Fill with Color - Noob Nodes",
    "SequentialDirectoryNode": "Sequential Directory Generator - Noob Nodes",
    "PathCleaner": "Path Cleaner - Noob Nodes",
    "ZeroPadNode": "Zero Pad (INT → 0000) - Noob Nodes",
    "CreateFoldersFromPath": "Create Folders From Path - Noob Nodes",
    "SquareBBoxFromMask": "Square BBox From Mask - Noob Nodes",
    "StringToLoraName": "String to LoRA Name - Noob Nodes",
    "PixelColorPicker": "Pixel Color Picker (HEX) - Noob Nodes",
    "ModelPathResolver": "Model Path Resolver - Noob Nodes",
    "MultiStringSplitter": "Multi-String Splitter (Max 6) - Noob Nodes",
    "SeedanceBytePlusNode": "Seedance 2.0 (Official API) - Noob Nodes",
    "SimpleTextDisplay": "Simple Text Display (Nodes 2.0) - Noob Nodes",
    "RemapValueRange": "Remap Value Range - Noob Nodes",
    "AnywhereLoraLoader": "🔍 Anywhere LoRA Loader - Noob Nodes",
    "AnywhereModelLoader": "🔍 Anywhere Model Loader - Noob Nodes",
    "AnywhereModelNameSelector": "Anywhere Diffusion Model Names - Noob Nodes",
    "MonoToStereo": "Mono to Stereo Audio - Noob Nodes",
    "ImageCacheNode": "🔄 Image Cache - Noob Nodes",
    "ComfyUICounterWithReset": "Counter Widget w/ Reset Switch - Noob Nodes"

}