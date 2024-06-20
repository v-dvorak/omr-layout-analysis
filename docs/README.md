# User Documentation

This documentation goes over repository structure and contents, setting up and using the scripts for dataset transformation and creation.

Links to important parts and other docs:

- [Dataset creation](#build-the-final-dataset) - how to create the dataset on which the model was trained
- TODO [Technical documentation]() - deep dive into the inner workings of this app
- [Model usage](https://docs.ultralytics.com/modes/predict/) - how to make predictions using the provided model, official YOLO docs
- [Model training](https://docs.ultralytics.com/modes/train/) - official YOLO docs

## Build the final dataset

How to create the dataset on which the model was trained.

:warning: This part requires a reliable internet connection and will take multiple hours to finish.

### Download repository and create a virtual env

```
# create new virtual environment
python -m venv /path/
# activate the environment
source /path/bin/activate
# install required modules from requirements.txt
pip install -r requirements.txt
```

### Build dataset

Make sure you have the virtual env activated than use this script that can be run from any directory:

```
path_to_repo/scripts/buíld
```

The final dataset can be found afterwards at `/datasets`.

(For smooth usage, please, use Linux or PowerShell if on Windows.)

### Model training

See [official YOLO docs](https://docs.ultralytics.com/modes/train/).

## Datasets download

Download datasets on which the model was trained.

:warning: This part requires a reliable internet connection.

### Download repository and create a virtual env

```
# create new virtual environment
python -m venv /path/
# activate the environment
source /path/bin/activate
# install required modules from requirements.txt
pip install -r requirements.txt
```

### Download datasets

Make sure you have the virtual env activated than use this script that can be run from any directory:

```
path_to_repo/scripts/download
```

## Build custom dataset

- [How to work with other datasets than those provided by default](../app/DatasetClasses/README.md#work-with-other-datasets-than-those-provided-by-default)

Given paths to datasets, which can be both provided by default
or added by user, creates a file system for training the YOLOv8 model, including a config `.yaml` file.

### Options

- `-c COUNT, --count COUNT`
    - How many files from each dataset will be processed. Default is all.
- `--split SPLIT`
  - Train test split ratio.
- `-l [LABELS ...], --labels [LABELS ...]`
  - List of labels to process: `0 : system_measures, 1 : stave_measures, 2 : staves, 3 : systems, 4 : grand staff`.
- `--deduplicate`
  - Checks for possible duplicates in labels and removes them. May affect performance.
- `--tag`
  - Tags generated files with dataset nickname. Example: `"al2_filename"`.
  - Default is all.
- `--stad [STAD ...]`
  - Paths to standard COCO dataset to be processed.
- `--al2`, `--mpp`, etc.
  - Includes the dataset into final dataset.
  - These are loaded automatically from their respective classes.
  - The selection can be expanded by user, for that see [this](#work-with-other-datasets-than-those-provided-by-default).

### Example usage
```
python3 -m app my_test --split 0.8 --al2 --mpp --stad my_standard_dataset -l 0 2
```

This will take records from the `AudioLabs v2`, `Muscima++` and user specified standard dataset
and divide them in the ratio of `0.8`, using only labels `0` and `2`. I will create this file structure:

```
Test
├─ images
│  ├─ train
│  ├─ val
├─ labels
│  ├─ train
│  ├─ val
├─ config.yaml
```

If the `--split` option is not used the file structure looks like this:

```
Test
├─ images
├─ labels
├─ config.yaml
```

## Annotations

- [What is (not) annotated and why?](annot_reference)
- [PianoMaker](../app/PianoMaker/README.md) - a small app that allows grand staff and staff system labels to be added into an already existing dataset

### YOLO format

- `*.txt` file
- one row per object
- `class x_center y_center width height` format, relative to width and height
- in this project, all numbers are rounded up to exactly 6 decimal places


> **From the YOLO docs**: Labels for this format should be exported to YOLO format with one *.txt file per image. If there are no objects in an image, no *.txt file is required.

Even though YOLO does not need annotation files for empty (negative) sample images, they are included in final datasets, for simplicity.

#### Example

```
0	0.578523	0.894962	0.131544	0.082700
0	0.717450	0.894962	0.140940	0.082700
0	0.869128	0.894962	0.159732	0.082700
1	0.153691	0.098859	0.208054	0.028517
1	0.324161	0.098859	0.130201	0.028517
1	0.461074	0.098859	0.138255	0.028517
```

For more see [official YOLO docs](https://docs.ultralytics.com/datasets/detect/).

### COCO format

- `*.json` file
- `left top width height` format in absolute numbers, `top left` are the `x y` coordinates from the top left corner of the uppermost leftmost corner of the bounding box

#### Example

```json
{
    "width": 745,
    "height": 1053,
    "system_measures": [
    {
        "left": 44,
        "top": 76,
        "width": 107,
        "height": 101
    },
    {
        "left": 153,
        "top": 76,
        "width": 76,
        "height": 101
    }, 
    ...
}
```

For more see [COCO dataset format](https://cocodataset.org/#format-data).

## Get MuseScore

Download [MuseScore](https://musescore.org) and replace the path in `app/Utils/Setting.py`:

```python
# TODO: path to a Musescore exe on you computer
MUSESCORE_PATH = "F:/Programy/Musescore3/bin/MuseScore3.exe"
```

If on Linux try this:

```
xvfb-run -a ./MuseScore-version.AppImage --appimage-extract-and-run
```