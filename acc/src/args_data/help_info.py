info_usage = """
Running the script, order and layout of input files:

1. The input is a single '*.csv' file:
    - raw data: data2cols.csv or data3cols.csv
    - confusion matrix: cross_raw.csv, cross.csv or cross_full.csv
    - binary_cross.csv

    -- `accuracy file.csv`
    -- `accuracy file.csv class_map.json`


2. Input data:
    - an image, after classification - usually of type '*.tif'
    - reference data: image/mask '*.tif' or vector data e.g. '*.shp', '*.gpkg'

    -- `accuracy raster.tif`
    -- `accuracy raster.tif class_map.json`

    -- `accuracy raster.tif reference_raster.tif`
    -- `accuracy raster.tif reference_raster.tif class_map.json`

    -- `accuracy raster.tif reference_vector.shp`
    -- `accuracy raster.tif reference_vector.shp class_map.json`
"""


info_metrics = """
1. The definitions of the metrics are mainly based on the binary \
error matrix with the following symbols:
  - TP true positive
  - TN true negative
  - FP false positive
  - FN false negative.

2. Accuracy metrics classically used in remote sensing:
  - OA (overall_accuracy):
   -- OA = sum(TP) / (TP + TN + FP + FN)

  -  PA (producer_accuracy):
   -- PA = TP / (TP + FN)

  -  UA (user_accuracy)
     -- UA = TP / (TP + FP)

  -  OME (omission errors / errors_of_omission):
     -- OME = FN / (TP + FN)

  -  CME (errors_of_commision):
     -- CME = FP / (TP + FP)

  -  NPV (negative predictive value):
     -- NPV = TN/(TN + FN) = 1 − FOR

3. Classification accuracy metrics found in contemporary scientific \
publications (some metrics overlap with some of the metrics mentioned in \
point 1).

These metrics can be conventionally divided into simple metrics \
(calculated directly from the TP, TN, FP and FN values) and complex metrics \
(calculated using simple metrics).

3.1. Simple metrics:

   -   ACC (accuracy):
      -- ACC = (TP+TN)/(P+N) = (TP+TN)/(TP+TN+FP+FN)

   -  PPV (precision or positive predictive value):
      -- PPV = TP / (TP + FP)

   -  PPV (precision or positive predictive):
      -- PPV = TP / (TP + FP)

   -  TPR (sensitivity, recall, hit rate, or true positive rate):
      -- TPR = TP/P = TP/(TP + FN) = 1 − FNR

   -  TNR (specificity, selectivity or true negative rate):
      -- TNR = TN/N = TN/(TN + FP) = 1 − FPR

   -  NPV (negative predictive value):
      -- NPV = TN/(TN + FN) = 1 − FOR

   -  FNR (miss rate or false negative rate):
      -- FNR = FN/P = FN/(FN + TP) = 1 − TPR

   -  FPR (fall-out or false positive rate):
      -- FPR = FP/N = FP/(FP + TN) = 1 − TNR

   -  FDR (false discovery rate):
      -- FDR = FP/(FP + TP) = 1 − PPV

   -  FOR (false omission rate):
      -- FOR = FN/(FN + TN) = 1 − NPV

   -  TS / CSI (Threat score (TS) or critical success index (CSI)):
      -- TS = TP/(TP + FN + FP)

   -  MCC (Matthews correlation coefficient):
      -- mcc = (TP*TN - FP*FN) / [(TP+FP) * (TP+FN) * (TN+FP) * (TN+FN)]^0.5

3.2. Complex metrics:
   - PT (Prevalence Threshold):
     -- PT = [(TPR*(1 − TNR))^0.5 + TNR − 1] / (TPR + TNR − 1)

   - BA (Balanced accuracy):
     -- ba = (TPR + TNR)/2

   - F1 score (is the harmonic mean of precision and sensitivity):
     -- f1 = 2*(PPV*TPR)/(PPV+TPR) = (2*TP)/(2*TP+FP+FN)

   - FM (Fowlkes–Mallows index):
     -- fm = [(TP/(TP+FP))*(TP/(TP+FN))]^0.5 = (PPV * TPR)^0.5

   - BM (informedness or Fowlkes–Mallows index):
     -- bm = TPR + TNR - 1

   - MK (markedness (MK) or deltaP):
     -- mk = PPV + NPV - 1
"""


info_data = """
1. Raw data:
Stores classification results in a table (*.csv) with 2 or 3 columns:

   - 2 columns:

             |    true   | predicted |
             |-----------+-----------|
             |    int    |    int    |
             |    ...    |    ...    |

   - 3 columns:

             |    true   | predicted |  lables  |
             |-----------+-----------+----------|
             |    int    |    int    |    str   |
             |    ...    |    ...    |    ...   |

   Where:
       - first column: true values (actual classes)
       - second column: predicted values (predicted classes)
       - third column: short names of classes e.g. water, wheat etc.

    Input:
        - columns must be in order [true_values, predicted]
        - column names do not matter (eg. true, true_values, etc)


2. Raw - cross matrix:
Confusion matrix for multi-class classification:
  - contains only numbers: no column or row descriptions, no summaries
  - is square: classes in columns must correspond to classes in rows, even if \
  there are zeros in some class

  Default layout is:
    - rows: True classes (true labels).
    - columns: Predicted classes (predicted labels)

       |   21  |    5   |   7   | ...
       |    6  |   31   |   2   | ...
       |    0  |    1   |  22   | ...
       |  ...  |   ...  |  ...  | ...


3. Cross - cross matrix:
Confusion matrix for multi-class classification:
  - contains numbers and descriptions of columns and rows (class names), \
    without summaries
  - does not have to be square:

  Default layout is:
    - rows: True classes (true labels).
    - columns: Predicted classes (predicted labels)
  

       |            | water | forest | urban | ...
       |------------+-------+--------+-------+-----
       |   water    |   21  |    5   |   7   | ...
       |   forest   |    6  |   31   |   2   | ...
       |   urban    |    0  |    1   |  22   | ...
       |    ...     |  ...  |   ...  |  ...  | ...

  
4. Full - cross matrix:
Full confusion matrix for multi-class classification:
  - contains numbers, column and row descriptions (class names) and row and \
    column summaries
  - does not have to be square:

  Default layout is:
    - rows: True classes (true labels).
    - columns: Predicted classes (predicted labels)


       |            | water | forest | urban | ... |  sums  |
       |------------+-------+--------+-------+-----|--------|
       |   water    |   21  |    5   |   7   | ... |   ...  |
       |   forest   |    6  |   31   |   2   | ... |   ...  |
       |   urban    |    0  |    1   |  22   | ... |   ...  |
       |    ...     |  ...  |   ...  |  ...  | ... |   ...  | 
       |------------+-------+--------+-------+-----|--------|
       |    sums    |  ...  |   ...  |  ...  | ... |   ...  |


5. Binary - cross matrix:
Confusion matrix for multi-class classification.

                      |    | water | forest | ... |
                      |----+-------+--------+-----|
                      | TP |    1  |   55   | ... |
                      | TN |   15  |   99   | ... |
                      | FP |    5  |    3   | ... |
                      | FN |   33  |   46   | ... |

    where:
  - columns: represent the classes in the dataset
  - rows: represent different types of classification outcomes for each class:
  - TP (True Positives): the number of samples correctly classified as a given class
  - TN (True Negatives): the number of samples that do not belong to a given class and were correctly identified as not belonging.
  - FP (False Positives): the number of samples incorrectly classified as a given class
  - FN (False Negatives): the number of samples of a given class that were incorrectly classified as not belonging to that class


6. Raster data
The input data can also be raster images and vector data. You can use:
 - two raster images: classification result and reference image (mask)
 - raster image and vector data

Raster images should be in `*.tif` format, georeferenced. Different file extensions are accepted:
 - '*.tif', '*.tiff', '*.TIF', '*.TIFF'

Vector data: two popular formats are accepted:
 - `*.shp` EERI shapefile spatial data format
 - `*.gpkg` the GeoPackage (GPKG)


6.1 Tip:
If the reference data file has the same name as the classification result file with an additional
suffix `_ref`, then you just need to provide the image file address (classification result) as input
and the script will search for the reference data, e.g.:

Instead of typing:
 - accuracy my_classification.tif my_classification_ref.tif
 - accuracy my_classification.tif my_classification_ref.shp

You can:
 - accuracy my_classification.tif
 - accuracy my_classification.tif


"""

info_formula = """
You can define your own calculation formula:

 - The calculations use the binary_cross matrix table.
 - The formula must follow Python's arithmetic syntax.
 - Use the following labels: TP, TN, FP, and FN.
 - The formula should consist of a left-hand side and a right-hand side: `metric = mathematical operations`. Example:
   -- mcc=(TP*TN-FP*FN)/((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))**0.5
 - Do not use whitespace (e.g., spaces) in the formula or metric name.
 - The metric name should be a short string, such as OA, f1, etc.
 - The pattern entered into the script must be surrounded by quotation marks (single `'` or double `"`).

Example of use:

 - `accuracy input_path -f "mcc=(TP*TN-FP*FN)/((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))**0.5"
 - `accuracy input_path --formula "mcc=(TP*TN-FP*FN)/((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))**0.5"

"""
