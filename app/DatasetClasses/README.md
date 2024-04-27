# Datasets

This module contains all classes needed to work with OMR datasets. These are currently supported by default:

- AudioLabs v2
- MUSCIMA++
- OSLiC
- any standard COCO dataset

## What is a "standard COCO dataset"?

Our standard dataset contains a (preferably) PNG of a score and its annotations in a COCO format inside a JSON file. Where `"left"` and `"right"` are `(x,y)` coordinates of the upper left corner of the annotation box in pixels.

```
# Standard COCO format:
{
    "width": 2977,
    "height": 4208,
    "staves": [
        {
            "left": 184,
            "top": 227,
            "width": 2650,
            "height": 82
        },
        ...
    ],
    "stave_measures": [
        ...
    ],
    "systems": [
        ...
    ],
    ...
}
```

## Work with other datasets than those provided by default

Create a new class derived from `Dataset_OMR` and implement necessary methods
to fit your dataset format:

```python
class MyDataset(Dataset_OMR):
    name = "My Dataset"
    nickname = "mydat"

    # necessary
    def _get_coco_format(self, record: dict) -> list[int]:
        """
        Given a single record from loaded JSON returns label in COCO format.
        """
    
    # optional
    def _download_proc(self, download_path: Path):
        """
        Downloads dataset to given path.
        """
        
    # optional
    def process_image(self, img_path: Path, output_path: Path):
        """
        Given a path to an image this method loads it,
        does all necessary preprocessing and saves it to given `output_path`.
        """
```

Dataset classes are loaded automatically - you only need to import it to
`Datasets/Import.py`

```python
# DatasetClasses/Import.py
from .DatasetOMR import Dataset_OMR
...
from .MyDatset import MyDataset
```
