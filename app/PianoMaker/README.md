# PianoMaker

Is a small app that allow other labels to be added into an already existing dataset.
It is mainly ment to be used to add `grand_staff` labels.
The dataset is loaded using methods defined in classes derived from `Dataset_OMR`,
then a file with additional labels in loaded and when completed the final product
is saved to the beforehand specified output path.

TODO:

**this module needs to be reworked to support newly defined grand staff annotation. at this current state it does not work.**

## Usage

```
# to run the script
python3 -m app.PianoMaker dataset_path additional_labels_path output_path --dataset_format
```

````
usage: OMR Dataset Utils [-h] [-v] [-o OFFSET] [-l GRAND_LIMIT] [--al2] [--mpp] [--stand]
                         dataset_path piano_path output_path

Given a dataset and a file with additional labels makes a JSON combining both current dataset labels and the new ones.

positional arguments:
  dataset_path          Path to dataset to be processed.
  piano_path            Path to grand staff annotations.
  output_path           Path to store the final dataset at.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Make script verbose.
  -o OFFSET, --offset OFFSET
                        How far apart two coordinates can be to still be considered the same, in pixels. Default is
                        10.
  -l GRAND_LIMIT, --grand_limit GRAND_LIMIT
                        Minimal amount of staves to consider multiple staves linked together to be a grand staff.
                        Default is 1.
  --al2                 The AudioLabs_v2 dataset will be processed.
  --mpp                 The Muscima++ dataset will be processed.
  --stand               The Standard Dataset dataset will be processed.
````

### How to use the Windows app

Is a small, simple and most-of-the-time-working annotation app built to make annotating existing datasets easier.

![](/docs/piano_annotator.png)

Type in annotation in desired format and hit the `Enter` key or `Submit`.

## Additional labels format

At this point in time only `grand_staff` addition is supported
(`systems` can be derived from already existing labels in AudioLabs v2 and Muscima++ datasets).
Let's say we want to add `grand_staff` for this image:

![](/docs/annot_example.png)

Its record in a file would look like this:

```
file_name
2-2 1-2 1-2
```

Where a numeral means how many staves there are in a grand staff
and `a-b-c-...-x` means that all these grand staves and inside one system.

:warning: Even if you don't consider single (or any other count) staff as a grand staff,
make sure to include it in a description, the script counts through all staves in the given picture
from top to bottom and not including some staves will mess up the process.
Minimal number of staves for it to be considered can be specified before running the script using the `-l` flag. 
