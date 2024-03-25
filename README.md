# omr-layout-analysis

**WIP**

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