# What is (not) annotated and why?

A documents in which all labels are described to hopefully avoid any confusion why some objects are annotated the way they are and some are not.

In this dataset we distinguish between five musical objects:

## Staff

- has five parallel lines that are all the same length
- has to be associated with any notes, music
- music does not have to be included through the whole length of the staff

### Examples

- ✅ this is a valid staff in its whole length, even though there is no music at the end:

![](/docs/examples/valid_staff.png)

- ❌ all of these are not valid staves, there is no music associated with them:

![](/docs/examples/invalid_staff.png)

## Staff Measure

- is a one measure of a staff
- is between two bar lines
- the first measure starts at the start (left) of the staff, last measure ends by last bar line or by the end of the staff[^1]
- there has to be music in the measure

[^1] Even thought scores from OsLiC that are missing ending bar lines are ruled out for the sake of keeping the code relatively simple.

### Examples

- ✅ this is a valid staff measure, there is music at the start:

![](/docs/examples/valid_staff_measure.png)

- ❌ this is and invalid staff measure, there is no music:

![](/docs/examples/invalid_staff_measure.png)

## System Measure

- is a unification of staff measures that are played at the same time

### Examples

- ✅ this is a valid system measure, all and only the music highlighted is played at the same time

![](/docs/examples/valid_system_measure.png)

- ❌ this is an invalid system measure, staff measures played at different times are included:

![](/docs/examples/invalid_system_measure.png)

## System

- includes every system measure on at the same height on the page
- is a unification of staves

### Examples

- ✅ this is a valid system, staves have to included in their whole length:

![](/docs/examples/valid_system.png)

- ❌ this is an invalid system, music that does not play at the same time is included:

![](/docs/examples/invalid_system.png)

- ❌ this is an invalid system, music that plays at the same time is not included:

![](/docs/examples/invalid_system2.png)

## Grand Staff

- is a unification of staves that are connected together by a single brace at the start of these staves
- the staves inside grand staff aare inseparable in the means of an instruments with which this grand staff is associated
- other brackets and configurations are no considered because:
  - other brackets are usually unions of instruments that need only one staff to be played fully[^2]
  - knowing which staff belongs to which instrument is an information that is outside the scope of this project, identifying piano (and similar instruments) is necessary because of the inseparability

[^2] Consider a string quartet, you can play these instruments individually, but you can't play the piano fully if given a one staff.


### Brace Example

- brace SVG signatures can be found in [this code file](../app/Synthetic/AnnotExtraction/FindGrandStaff.py)

- ❌ ✅ here is an example of both valid and invalid braces, note that the invalid one (the first one) has a slightly different shape and is not associated with a score for piano

### Examples

- ❌ ✅ first object is not a grand staff because it is not connected by the correct brace/bracket

![](/docs/examples/grand_staff.png)
