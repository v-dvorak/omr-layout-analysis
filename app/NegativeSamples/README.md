# Negative samples (Background images)

## From the YOLO docs

> **Background images**. Background images are images with no objects that are added to a dataset to reduce False
> Positives (FP). We recommend about 0-10% background images to help reduce FPs (COCO has 1000 background images for
> reference, 1% of the total). No labels are required for background images.

The final dataset will consist of approximately ten thousand images, that means that we'll need around one thousand
background images.

## Where do we get the images from?

From Moravská zemská knihovna - MZK.

Using
the [MZK search engine](https://www.digitalniknihovna.cz/mzk/search?access=open&licences=public&doctypes=sheetmusic) we
can search specifically for open and public sheet music, there are thousands of them. MZK implements the really nice and
convenient to use [IIIF API](https://iiif.io/api/image/3.0/). There are only two problems with it:

- I was not able to find any documentation on how to use this api to search for documents using filters. (Like "give me
  IDs to all sheet music documents".)

- Page labelling is not consistent and some page IDs end up raising 4xx or 5xx errors.

### [How does MZKScraper work?](https://github.com/v-dvorak/mzkscraper/blob/main/docs/README.md)

## Numbers of representative images

The number of representative images for each label was counted as $\left\lceil\frac{\text{\# samples of label} \:
\cdot \: \text{\# images wanted}}{\text{\# samples in total}}\right\rceil$, this ensures that the number of
representative images in total is around the value we want (1000 images).

For quick image overview see [image grids](./docs/README.md).

| Label                    |  Count   |
|:-------------------------|:--------:|
| back cover               |    43    |        
| back end paper           |    20    |
| back end sheet           |    43    |
| blank                    |   556    |
| fragments of bookbinding |    1     |
| front cover              |    45    |
| front end_paper          |    21    |
| front end sheet          |    45    |
| illustration             |    1     |
| index                    |    12    |
| table of contents        |    7     |
| title page               |   212    |
| **Total**                | **1006** |

## Labels provided by MZK

### Accepted labels

#### Blank

![](https://api.kramerius.mzk.cz/search/iiif/uuid:b12f3c58-cf2a-4d6c-8838-01acda789e88/full/%5E!640,640/0/default.jpg)

#### Illustration

![](https://api.kramerius.mzk.cz/search/iiif/uuid:8537ecf9-e8b9-4147-aacc-1710ecd0f753/full/%5E!640,640/0/default.jpg)

#### Front cover

![](https://api.kramerius.mzk.cz/search/iiif/uuid:e41d0133-33b6-4d3b-aef2-f62fc9419d4a/full/%5E!640,640/0/default.jpg)

#### Front end sheet

![](https://api.kramerius.mzk.cz/search/iiif/uuid:1dc331dd-bbd9-46d2-9def-8f69bffcfc5a/full/%5E!640,640/0/default.jpg)

#### Back end sheet

![](https://api.kramerius.mzk.cz/search/iiif/uuid:8b0cc1fc-0204-471d-96b9-ab6d8ae54d62/full/%5E!640,640/0/default.jpg)

#### Back cover

![](https://api.kramerius.mzk.cz/search/iiif/uuid:906dca8d-5710-4ea7-b1b9-c9cd7975889f/full/%5E!640,640/0/default.jpg)

#### Title page

![](https://api.kramerius.mzk.cz/search/iiif/uuid:b185a013-b494-4f79-8cfc-d09cdfb502d3/full/%5E!640,640/0/default.jpg)

#### Back end paper

![](https://api.kramerius.mzk.cz/search/iiif/uuid:c26b4828-279f-4bdd-b8c9-a904e15170a4/full/%5E!640,640/0/default.jpg)

#### Back end paper

![](https://api.kramerius.mzk.cz/search/iiif/uuid:83170c1a-2914-498a-b571-e4496cd6c87a/full/%5E!640,640/0/default.jpg)

#### Index

![](https://api.kramerius.mzk.cz/search/iiif/uuid:aa4ce04a-9c37-49fe-827a-f09d3a2b2e81/full/%5E!640,640/0/default.jpg)

#### Fragments of bookbinding

- fun fact: in all the search results this is the only "fragments of bookbinding" picture

![](https://api.kramerius.mzk.cz/search/iiif/uuid:29e3938f-bc72-4ec1-aeec-d54d908a99b0/full/%5E!640,640/0/default.jpg)

### Rejected labels

#### Spine

![](https://api.kramerius.mzk.cz/search/iiif/uuid:b57d0175-adf7-4c86-bb52-0c3e02aa35ee/full/%5E!640,640/0/default.jpg)

#### Edge

![](https://api.kramerius.mzk.cz/search/iiif/uuid:97df2260-d12c-4fe1-9b41-d511744366d5/full/%5E!640,640/0/default.jpg)

#### Cover

![](https://api.kramerius.mzk.cz/search/iiif/uuid:37c18f61-cb2e-4d49-90c4-a25df0b00850/full/%5E!640,640/0/default.jpg)

#### SheetMusic

![](https://api.kramerius.mzk.cz/search/iiif/uuid:5117409d-9583-4c08-a4c8-134ac885853e/full/%5E!640,640/0/default.jpg)

#### CalibrationTable

![](https://api.kramerius.mzk.cz/search/iiif/uuid:81d2c5a2-0d2e-4f62-9322-274fbc5042ad/full/%5E!640,640/0/default.jpg)

#### NormalPage

- Normal pages are not consistent enough for us to write a single and simple definition. They may or may not include
  music notations and for simplicity were dropped from the final dataset.

![](https://api.kramerius.mzk.cz/search/iiif/uuid:de0a93a8-4fb9-4236-8c10-3652e55b432e/full/%5E!640,640/0/default.jpg)

#### FlyLeaf

- Random papers inserted to books, they are not consistent enough.

![](https://api.kramerius.mzk.cz/search/iiif/uuid:b7df9b52-5789-44d3-b6df-9a06a22c74ba/full/%5E!640,640/0/default.jpg)

#### and others

- Random tags and book page numbers that do not correspond to anything specific.

