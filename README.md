# Analysis of music notation documents using YOLO system

:warning: **WIP**

## About this project

Optical Music Recognition (OMR) is a task that aims to automatically recognize the musical content of a document from a photo or scan of music notation for further processing (search, printing, editing, musicological analysis). For processing existing archival materials in libraries, however, it is first necessary to distinguish whether a given page contains musical notation, or what kind of notation (modern, mensural, choral, printed, written). At the moment, the best recognition models work at the level of individual lines of notation, so it is also necessary to identify individual lines during the analysis of a document so that the music can be well processed by the recognition models.

The aim of this project is to create a music notation page analyzer that will serve as a first stage in the automatic recognition of music notation pages. The analysis will be designed as an image object detection task, where the main goal will be to train (retrain) the state of the art model YOLOv8. The focus of the work lies in the preparation of the training data, as it will be necessary to harmonize a number of existing datasets into a unified format with the possible inclusion of synthetic data. At the same time, it will be necessary to decide what parameters of musical notation to analyse - a compromise must be found between what we need to know and what we are able to learn from the available datasets

## Setup

```
# create new virtual environment
python -m venv /path/
# activate the environment
source /path/bin/activate
# install required modules from requirements.txt
pip install -r requirements.txt
```

## Usage

```
Compiles chosen OMR datasets into a big one for future use for training the YOLOv8 model.

positional arguments:
  output                Path to store the final dataset at.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Make script verbose
  -t, --train           Create "train" subfolders
  -c COUNT, --count COUNT
                        How many files from each dataset will be processed. Default is all.
  --tag                 Tags generated files with dataset nickname. Example: "al2_filename".
  -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        Which labels to process. 0 : system_measures, 1 : stave_measures, 2 : staves. Default is all.
  -s, --dontsort        DONT sort labels by default numerical tags. Labels are sorted in ascending order by default.
  --al2                 Includes the AudioLabs_v2 dataset into final dataset.
  --mpp                 Includes the MusicmaPlusPlus dataset into final dataset.
```