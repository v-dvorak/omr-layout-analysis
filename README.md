# Analysis of music notation documents using the YOLO system

:warning: **WIP**

## About this project

Optical Music Recognition (OMR) is a task that aims to automatically recognize the musical content of a document from a photo or scan of music notation for further processing (search, printing, editing, musicological analysis). For processing existing archival materials in libraries, however, it is first necessary to distinguish whether a given page contains musical notation, or what kind of notation (modern, mensural, choral, printed, written). At the moment, the best recognition models work at the level of individual lines of notation, so it is also necessary to identify individual lines during the analysis of a document so that the music can be well processed by the recognition models.

The aim of this project is to create a music notation page analyzer that will serve as a first stage in the automatic recognition of music notation pages. The analysis will be designed as an image object detection task, where the main goal will be to train (retrain) the state-of-the-art model YOLOv8. The focus of the work lies in the preparation of the training data, as it will be necessary to harmonize a number of existing datasets into a unified format with the possible inclusion of synthetic data. At the same time, it will be necessary to decide what parameters of musical notation to analyse - a compromise must be found between what we need to know and what we are able to learn from the available datasets.

## Setup

```
# create new virtual environment
python -m venv /path/
# activate the environment
source /path/bin/activate
# install required modules from requirements.txt
pip install -r requirements.txt
```

## Main App

Given paths to datasets which can be both provided by default
or added by user creates a file system for training the YOLOv8 model,
including config `.yaml` file.

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

## Example usage
```
python3 -m app ../Test --split 0.8 --al2 --mpp --stad my_standard_dataset -l 0 2
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

## Other useful documentation

- [How to work with other datasets than those provided by default](app/DatasetClasses/README.md)
- [PianoMaker](app/PianoMaker/README.md), a small app that allow other labels to be added into an already existing dataset
- [What is (not) annotated and why?](docs/README.md)
- [Extracting annotations from OSLiC](app/Synthetic/README.md)

## Acknowledgement

- ### Staves and staff systems extraction from SVG

  - by @Kristyna-Harvanova , the project can be found [here](https://github.com/Kristyna-Harvanova/Bachelor-Thesis)

- ### Grand staff extraction from SVG

  - by @Jirka-Mayer , the project can be found [here](https://github.com/ufal/olimpic-icdar24)

## References

Images displayed are the part of the AudioLabs v2 dataset accompanying the following paper:

```
Frank Zalkow, Angel Villar Corrales, TJ Tsai, Vlora Arifi-Müller, and Meinard Müller
Tools for Semi-Automatic Bounding Box Annotation of Musical Measures in Sheet Music
In Demos and Late Breaking News of the International Society for Music Information Retrieval Conference (ISMIR), 2019.
```
